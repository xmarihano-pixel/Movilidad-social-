"""Diagnósticos de las Fases 6-8: métricas completas, calibración, estabilidad y matriz de decisión."""
import numpy as np
import pandas as pd
from sklearn.base import clone
from sklearn.calibration import calibration_curve
from sklearn.dummy import DummyClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (average_precision_score, classification_report, confusion_matrix,
                             log_loss, roc_auc_score)
from sklearn.model_selection import StratifiedKFold, cross_val_score, learning_curve
from sklearn.pipeline import Pipeline

from src.config import SEED
from src.models import train as T


def full_metrics(models: dict, te, num, cat, target="sigue_q1"):
    rows, reports, cms = [], {}, {}
    for name, m in models.items():
        p = m.predict_proba(te[num + cat])[:, 1]
        pred = (p >= 0.5).astype(int)
        rep = classification_report(te[target], pred, output_dict=True, zero_division=0)
        rows.append({"Modelo": name, "AUC": roc_auc_score(te[target], p),
                     "PR-AUC": average_precision_score(te[target], p),
                     "Log loss": log_loss(te[target], np.clip(p, 1e-6, 1 - 1e-6)),
                     "Precisión (sigue Q1)": rep["1"]["precision"], "Recall (sigue Q1)": rep["1"]["recall"],
                     "Precisión (sale)": rep["0"]["precision"], "Recall (sale)": rep["0"]["recall"],
                     "Macro F1": rep["macro avg"]["f1-score"]})
        cms[name] = pd.DataFrame(confusion_matrix(te[target], pred), index=["Real: sale", "Real: sigue"],
                                 columns=["Pred: sale", "Pred: sigue"])
    return pd.DataFrame(rows).round(3), cms


def stratified_baseline(tr, te, num, cat, target="sigue_q1"):
    m = Pipeline([("p", T.preprocessor(num, cat)), ("m", DummyClassifier(strategy="stratified", random_state=SEED))])
    m.fit(tr[num + cat], tr[target])
    return m


def calibration_table(models: dict, te, num, cat, target="sigue_q1", bins=8):
    out = {}
    for name, m in models.items():
        p = m.predict_proba(te[num + cat])[:, 1]
        frac, mean = calibration_curve(te[target], p, n_bins=bins, strategy="quantile")
        out[name] = pd.DataFrame({"Prob. predicha": mean, "Frecuencia real": frac})
    return out


def class_weight_check(tr, num, cat, target="sigue_q1"):
    cv = StratifiedKFold(5, shuffle=True, random_state=SEED)
    res = {}
    for cw in [None, "balanced"]:
        m = Pipeline([("p", T.preprocessor(num, cat)), ("m", LogisticRegression(C=0.5, max_iter=5000, class_weight=cw))])
        res["Sin pesos" if cw is None else "class_weight='balanced'"] = {
            "AUC CV": cross_val_score(m, tr[num + cat], tr[target], cv=cv, scoring="roc_auc").mean(),
            "Exactitud balanceada CV": cross_val_score(m, tr[num + cat], tr[target], cv=cv, scoring="balanced_accuracy").mean()}
    return pd.DataFrame(res).T.round(3)


def seed_sensitivity(df, num, cat, names=("Regresión logística", "Random forest", "Gradient boosting"), seeds=range(10)):
    rows = []
    d = df[df.sigue_q1.notna()].copy()
    d["sigue_q1"] = d["sigue_q1"].astype(int)
    for s in seeds:
        cv = StratifiedKFold(5, shuffle=True, random_state=s)
        for n in names:
            m = T.candidates(num, cat)[n]
            if "m__random_state" in m.get_params():
                m.set_params(m__random_state=s)
            rows.append({"Semilla": s, "Modelo": n,
                         "AUC": cross_val_score(m, d[num + cat], d["sigue_q1"], cv=cv, scoring="roc_auc").mean()})
    r = pd.DataFrame(rows)
    return r.groupby("Modelo")["AUC"].agg(["mean", "std", "min", "max"]).round(3), r


def learning(model, tr, num, cat, target="sigue_q1"):
    sizes, trs, vas = learning_curve(model, tr[num + cat], tr[target], cv=StratifiedKFold(5, shuffle=True, random_state=SEED),
                                     scoring="roc_auc", train_sizes=np.linspace(0.15, 1.0, 6), n_jobs=-1)
    return pd.DataFrame({"n entrenamiento": sizes, "AUC entrenamiento": trs.mean(1), "AUC validación": vas.mean(1)}).round(3)


def target_stress(df, num, cat):
    """¿El modelo y su ranking de variables sobreviven a otra definición del objetivo?
    Alternativa: destino medido con quintiles de ingreso per cápita (por cohorte)."""
    from src.features.indices import weighted_quintile
    d = df.copy()
    qi = pd.Series(0, index=d.index)
    for _, g in d.groupby("cohorte"):
        qi[g.index] = weighted_quintile(g["ingreso_pc"], g["factor"])
    d["sigue_q1_ingreso"] = np.where(d.q_origen == 1, (qi == 1).astype(float), np.nan)
    d = d[d.sigue_q1_ingreso.notna()]
    cv = StratifiedKFold(5, shuffle=True, random_state=SEED)
    m = T.candidates(num, cat)["Regresión logística"]
    auc = cross_val_score(m, d[num + cat], d["sigue_q1_ingreso"].astype(int), cv=cv, scoring="roc_auc").mean()
    acuerdo = (d["sigue_q1"] == d["sigue_q1_ingreso"]).mean()
    return {"AUC CV (objetivo por ingreso)": round(auc, 3), "Acuerdo entre definiciones": round(acuerdo, 3)}


def decision_matrix(tabla, seeds_summary, subgroups: dict):
    """Matriz multicriterio de la Fase 7 (1 = peor, 5 = mejor). Las calificaciones de
    interpretabilidad y complejidad son juicios fijos declarados; las demás salen de los datos."""
    fijos = {"Regresión logística": (5, 5, 5), "Árbol de decisión": (4, 4, 3),
             "Random forest": (2, 2, 3), "Gradient boosting": (1, 2, 3)}
    t = tabla.set_index("Modelo")
    rows = []
    for n, (interp, compl, ciencia) in fijos.items():
        auc = t.loc[n, "AUC CV (media)"]
        std = seeds_summary.loc[n, "std"] if n in seeds_summary.index else t.loc[n, "AUC CV (desv.)"]
        gap = subgroups.get(n, np.nan)
        rows.append({"Modelo": n, "AUC CV": auc, "Desv. entre semillas/folds": std,
                     "Brecha máx. de calibración por tono (pts)": gap,
                     "Interpretabilidad (1-5)": interp, "Simplicidad (1-5)": compl, "Adecuación científica (1-5)": ciencia})
    return pd.DataFrame(rows).round(3)


def tone_gap(model, te, num, cat):
    p = model.predict_proba(te[num + cat])[:, 1]
    g = te.assign(_p=p).groupby("tono_piel").apply(lambda x: abs(x.sigue_q1.mean() - x._p.mean()))
    return round(g.max() * 100, 1)
