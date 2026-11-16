"""Fases 6-7: baselines, modelos y comparación.

Tarea principal: entre las personas que crecieron en el 20% más pobre (Q1 de origen),
predecir si siguen en el 20% más pobre de adultos (`sigue_q1`). Sólo se usan
circunstancias de origen y características dadas (no elegidas) para evitar *leakage*.
"""
import time

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.dummy import DummyClassifier
from sklearn.ensemble import HistGradientBoostingClassifier, RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (balanced_accuracy_score, brier_score_loss, f1_score,
                             roc_auc_score)
from sklearn.model_selection import StratifiedKFold, cross_val_predict, cross_validate, train_test_split
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
        t0 = time.perf_counter()
        model.fit(tr[num + cat], tr[target])
        t_fit = time.perf_counter() - t0
        p = model.predict_proba(te[num + cat])[:, 1]
        r = {"Modelo": name, "AUC CV (media)": s["test_roc_auc"].mean(), "AUC CV (desv.)": s["test_roc_auc"].std(),
             **{f"{k} prueba": v for k, v in evaluate(te[target], p).items()},
             "Tiempo de entrenamiento (s)": t_fit}
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


def oof_predictions(model, df, num, cat, target="sigue_q1"):
    """Predicciones fuera de muestra (CV de 5 particiones) para TODAS las personas de Q1.
    Corrección de auditoría C-01: el desempeño por subgrupo no debe medirse en una sola
    partición de prueba pequeña (n = 114 en tono oscuro produjo una brecha espuria)."""
    d = df[df[target].notna()].copy()
    d[target] = d[target].astype(int)
    cv = StratifiedKFold(5, shuffle=True, random_state=SEED)
    d["_p"] = cross_val_predict(model, d[num + cat], d[target], cv=cv, method="predict_proba")[:, 1]
    return d


def subgroup_performance(model, df, num, cat, target="sigue_q1", B=500):
    d = oof_predictions(model, df, num, cat, target)
    rng = np.random.default_rng(SEED)
    rows = []
    for col, lab in [("mujer", {0: "Hombre", 1: "Mujer"}), ("tono_piel", None), ("region_14", None),
                     ("lengua_indigena", {0: "No habla lengua indígena", 1: "Habla lengua indígena"}),
                     ("localidad_14", None)]:
        for k, g in d.groupby(col):
            if g[target].nunique() < 2 or len(g) < 30:
                continue
            y, p = g[target].values, g["_p"].values
            gaps = []
            for _ in range(B):
                i = rng.integers(0, len(g), len(g))
                gaps.append((y[i].mean() - p[i].mean()) * 100)
            rows.append({"Variable": col, "Grupo": lab[k] if lab else k, "n": len(g),
                         "Tasa real sigue Q1": y.mean(), "Tasa predicha": p.mean(),
                         "Brecha (pts)": (y.mean() - p.mean()) * 100,
                         "IC 95% inf": np.percentile(gaps, 2.5), "IC 95% sup": np.percentile(gaps, 97.5),
                         "AUC": roc_auc_score(y, p)})
    return pd.DataFrame(rows).round(3)
