"""Fases 6-7: baselines, modelos y comparación.

Tarea principal: entre las personas que crecieron en el 20% más pobre (Q1 de origen),
predecir si siguen en el 20% más pobre de adultos (`sigue_q1`). Sólo se usan
circunstancias de origen y características dadas (no elegidas) para evitar *leakage*.
"""
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.dummy import DummyClassifier
from sklearn.ensemble import HistGradientBoostingClassifier, RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (balanced_accuracy_score, brier_score_loss, f1_score,
                             roc_auc_score)
from sklearn.model_selection import StratifiedKFold, cross_validate, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.tree import DecisionTreeClassifier

from src.config import SEED

NUM = ["indice_origen", "hermanos", "orden_nacimiento", "hacinamiento_14", "personas_hogar_14",
       "mujer", "lengua_indigena", "madre_trabajaba", "vivia_ambos_padres", "sosten_madre"] + \
      [f"o_p33{c}" for c in "abcdefgh"]
CAT = ["educ_padre", "educ_madre", "clase_padre", "localidad_14", "region_14", "cohorte",
       "tono_piel", "autoadscripcion"]
# Variables de "trayectoria" (no son circunstancias de origen): sólo en el modelo de mediación.
MEDIADORAS_CAT = ["educ"]
MEDIADORAS_NUM = ["migro_entidad"]


def preprocessor(num, cat, scale=True):
    num_steps = [("imp", SimpleImputer(strategy="median"))] + ([("sc", StandardScaler())] if scale else [])
    return ColumnTransformer([
        ("num", Pipeline(num_steps), num),
        ("cat", OneHotEncoder(handle_unknown="ignore", min_frequency=30), cat),
    ])


def candidates(num, cat):
    return {
        "Base: siempre la clase mayoritaria": Pipeline([("p", preprocessor(num, cat)), ("m", DummyClassifier(strategy="prior"))]),
        "Base: sólo índice de origen": Pipeline([("p", preprocessor(["indice_origen"], [])),
                                                 ("m", LogisticRegression(max_iter=2000))]),
        "Regresión logística": Pipeline([("p", preprocessor(num, cat)),
                                         ("m", LogisticRegression(C=0.5, max_iter=5000))]),
        "Árbol de decisión": Pipeline([("p", preprocessor(num, cat, scale=False)),
                                       ("m", DecisionTreeClassifier(max_depth=4, min_samples_leaf=50, random_state=SEED))]),
        "Random forest": Pipeline([("p", preprocessor(num, cat, scale=False)),
                                   ("m", RandomForestClassifier(n_estimators=400, min_samples_leaf=20,
                                                                max_features="sqrt", n_jobs=-1, random_state=SEED))]),
        "Gradient boosting": Pipeline([("p", preprocessor(num, cat, scale=False)),
                                       ("m", HistGradientBoostingClassifier(max_depth=3, learning_rate=0.05,
                                                                            max_iter=300, l2_regularization=1.0,
                                                                            random_state=SEED))]),
    }


def evaluate(y, p, thr=0.5):
    pred = (p >= thr).astype(int)
    return {"AUC": roc_auc_score(y, p), "Exactitud balanceada": balanced_accuracy_score(y, pred),
            "F1": f1_score(y, pred), "Brier": brier_score_loss(y, p)}


def split(df, target="sigue_q1"):
    d = df[df[target].notna()].copy()
    d[target] = d[target].astype(int)
    tr, te = train_test_split(d, test_size=0.2, stratify=d[target], random_state=SEED)
    return tr, te


def compare(tr, te, num, cat, target="sigue_q1"):
    cv = StratifiedKFold(5, shuffle=True, random_state=SEED)
    rows, fitted = [], {}
    for name, model in candidates(num, cat).items():
        s = cross_validate(model, tr[num + cat], tr[target], cv=cv, scoring=["roc_auc", "balanced_accuracy"])
        model.fit(tr[num + cat], tr[target])
        p = model.predict_proba(te[num + cat])[:, 1]
        r = {"Modelo": name, "AUC CV (media)": s["test_roc_auc"].mean(), "AUC CV (desv.)": s["test_roc_auc"].std(),
             **{f"{k} prueba": v for k, v in evaluate(te[target], p).items()}}
        rows.append(r)
        fitted[name] = model
    return pd.DataFrame(rows).round(3), fitted


def choose(table, tol=0.01):
    """Regla del roadmap: no elegir automáticamente la métrica más alta. Si un modelo
    interpretable está a menos de `tol` de AUC del mejor, se prefiere el interpretable."""
    t = table[~table["Modelo"].str.startswith("Base")].set_index("Modelo")
    best = t["AUC CV (media)"].idxmax()
    if t.loc["Regresión logística", "AUC CV (media)"] >= t.loc[best, "AUC CV (media)"] - tol:
        return "Regresión logística", best
    return best, best


def subgroup_performance(model, te, num, cat, target="sigue_q1"):
    p = model.predict_proba(te[num + cat])[:, 1]
    te = te.assign(_p=p)
    rows = []
    for col, lab in [("mujer", {0: "Hombre", 1: "Mujer"}), ("tono_piel", None), ("region_14", None),
                     ("lengua_indigena", {0: "No habla lengua indígena", 1: "Habla lengua indígena"}),
                     ("localidad_14", None)]:
        for k, g in te.groupby(col):
            if g[target].nunique() < 2 or len(g) < 30:
                continue
            rows.append({"Variable": col, "Grupo": lab[k] if lab else k, "n": len(g),
                         "Tasa real sigue Q1": g[target].mean(), "Tasa predicha": g["_p"].mean(),
                         "AUC": roc_auc_score(g[target], g["_p"])})
    return pd.DataFrame(rows).round(3)
