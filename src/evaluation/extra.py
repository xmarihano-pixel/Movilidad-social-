"""Análisis complementarios pedidos por el roadmap: hipótesis H001-H005, interacciones,
SHAP, análisis de errores, perfiles (K-Means) y escenarios con incertidumbre."""
import numpy as np
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf
from sklearn.cluster import KMeans
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from src.config import SEED
from src.models import train as T


def wavg(x, w):
    return float(np.average(x, weights=w))


def _logit(f, d):
    d = d.copy()
    d["w"] = d["factor"] / d["factor"].mean()
    mod = smf.glm(f, data=d, family=sm.families.Binomial(), var_weights=d["w"])
    rows = mod.data.row_labels
    mod = smf.glm(f, data=d.loc[rows], family=sm.families.Binomial(), var_weights=d.loc[rows, "w"])
    return mod.fit(cov_type="cluster", cov_kwds={"groups": pd.factorize(d.loc[rows, "upm"])[0]})


def h003_educacion_por_region(df):
    """H003: ¿la asociación de la escolaridad propia con salir de Q1 varía por región?"""
    q1 = df[df.sigue_q1.notna() & df.educ.notna()].copy()
    q1["educ_media_sup"] = q1.educ.isin(["Preparatoria", "Profesional"]).astype(int)
    tab = q1.groupby(["region_14", "educ_media_sup"]).apply(
        lambda x: pd.Series({"% sigue Q1": wavg(x.sigue_q1, x.factor) * 100, "n": len(x)})).unstack()
    tab.columns = [f"{a} | {'Prepa o más' if b else 'Secundaria o menos'}" for a, b in tab.columns]
    tab["Diferencia (pts)"] = tab["% sigue Q1 | Secundaria o menos"] - tab["% sigue Q1 | Prepa o más"]
    m0 = _logit("sigue_q1 ~ educ_media_sup + C(region_14) + indice_origen + C(cohorte)", q1)
    m1 = _logit("sigue_q1 ~ educ_media_sup * C(region_14) + indice_origen + C(cohorte)", q1)
    inter = [k for k in m1.params.index if ":" in k]
    wald = m1.wald_test(" , ".join(f"{k} = 0" for k in inter), scalar=True)
    return tab.round(1), {"p-valor conjunto de las interacciones (Wald)": round(float(wald.pvalue), 3)}


def h004_movilidad_educativa_vs_economica(df):
    """H004: ¿superar la escolaridad de los padres garantiza salir de Q1?"""
    q1 = df[df.sigue_q1.notna() & df.supero_educ_padres.notna()]
    r = q1.groupby("supero_educ_padres").apply(
        lambda x: pd.Series({"% sigue Q1": wavg(x.sigue_q1, x.factor) * 100, "n": len(x)}))
    r.index = r.index.map({0.0: "No superó a sus padres", 1.0: "Superó la escolaridad de sus padres"})
    pct_supero = wavg(q1.supero_educ_padres, q1.factor) * 100
    return r.round(1), round(pct_supero, 1)


def h005_desventajas_acumuladas(df):
    """H005: ¿las combinaciones de desventajas informan más que los factores aislados?"""
    q1 = df[df.sigue_q1.notna()].copy()
    q1["sur"] = (q1.region_14 == "Sur").astype(int)
    q1["pueblo"] = (q1.localidad_14 == "Pueblo (<2,500)").astype(int)
    q1["n_desventajas"] = q1.sur + q1.pueblo + q1.lengua_indigena
    acum = q1.groupby("n_desventajas").apply(
        lambda x: pd.Series({"% sigue Q1": wavg(x.sigue_q1, x.factor) * 100, "n": len(x)})).round(1)
    m0 = _logit("sigue_q1 ~ sur + pueblo + lengua_indigena + indice_origen + C(cohorte)", q1)
    m1 = _logit("sigue_q1 ~ sur * pueblo * lengua_indigena + indice_origen + C(cohorte)", q1)
    inter = [k for k in m1.params.index if ":" in k]
    wald = m1.wald_test(" , ".join(f"{k} = 0" for k in inter), scalar=True)
    return acum, {"p-valor conjunto de las interacciones (Wald)": round(float(wald.pvalue), 3),
                  "AIC aditivo": round(m0.aic, 1), "AIC con interacciones": round(m1.aic, 1)}


def missing_by_group(df):
    d = df.assign(educ_padre_falta=(df.educ_padre == "No sabe / ausente").astype(int))
    rows = []
    for col in ["q_origen", "region_14", "localidad_14", "cohorte"]:
        g = d.groupby(col).apply(lambda x: wavg(x.educ_padre_falta, x.factor) * 100).round(1)
        for k, v in g.items():
            rows.append({"Variable": col, "Grupo": k, "% sin dato de escolaridad del padre": v})
    sig = d[d.sigue_q1.notna()].groupby("educ_padre_falta").apply(lambda x: wavg(x.sigue_q1, x.factor) * 100).round(1)
    return pd.DataFrame(rows), sig


def simpson_check(df):
    """¿La brecha por tono de piel se mantiene dentro de cada región? (posible efecto Simpson)"""
    q1 = df[df.sigue_q1.notna()]
    t = q1.groupby(["region_14", "tono_piel"]).apply(
        lambda x: pd.Series({"pct": wavg(x.sigue_q1, x.factor) * 100, "n": len(x)})).unstack()
    out = t["pct"].round(1)
    out["n total"] = t["n"].sum(axis=1).astype(int)
    total = q1.groupby("tono_piel").apply(lambda x: wavg(x.sigue_q1, x.factor) * 100).round(1)
    out.loc["NACIONAL"] = list(total.reindex(out.columns[:-1])) + [len(q1)]
    return out


def empleo_trayectoria(df):
    d = df[df.sigue_q1.notna()]
    return d.groupby("empleo").apply(lambda x: pd.Series({"% sigue Q1": wavg(x.sigue_q1, x.factor) * 100, "n": len(x)})).round(1)


def shap_values(model, te, num, cat, n=400):
    import shap
    pre, est = model.named_steps["p"], model.named_steps["m"]
    X = pre.transform(te[num + cat].iloc[:n])
    X = X.toarray() if hasattr(X, "toarray") else X
    names = [n.split("__", 1)[1] for n in pre.get_feature_names_out()]
    sv = shap.TreeExplainer(est).shap_values(X)
    sv = sv[1] if isinstance(sv, list) else (sv[..., 1] if sv.ndim == 3 else sv)
    imp = pd.Series(np.abs(sv).mean(0), index=names)
    # agrupar columnas one-hot a su variable original
    base = {c: next((v for v in num + cat if c == v or c.startswith(v + "_")), c) for c in names}
    return imp.groupby(base).sum().sort_values(ascending=False).round(4), sv, X, names


def error_analysis(model, te, num, cat):
    p = model.predict_proba(te[num + cat])[:, 1]
    d = te.assign(p=p, error=((p >= .5).astype(int) != te.sigue_q1).astype(int))
    d["tipo"] = np.select([(d.error == 1) & (d.sigue_q1 == 1), (d.error == 1) & (d.sigue_q1 == 0)],
                          ["Falso negativo (sigue y se predijo que sale)", "Falso positivo (sale y se predijo que sigue)"], "Acierto")
    perfil = d.groupby("tipo").agg(n=("id", "size"), sur=("region_14", lambda x: (x == "Sur").mean() * 100),
                                   pueblo=("localidad_14", lambda x: (x == "Pueblo (<2,500)").mean() * 100),
                                   lengua=("lengua_indigena", "mean"), tono_oscuro=("tono_piel", lambda x: (x == "Oscuro (A-E)").mean() * 100),
                                   educ_prepa_mas=("educ", lambda x: x.isin(["Preparatoria", "Profesional"]).mean() * 100))
    perfil["lengua"] *= 100
    return perfil.round(1).rename(columns={"sur": "% Sur", "pueblo": "% pueblo", "lengua": "% lengua indígena",
                                           "tono_oscuro": "% tono oscuro", "educ_prepa_mas": "% prepa o más (no usado por el modelo)"})


def perfiles_kmeans(df, k=4):
    q1 = df[df.sigue_q1.notna()].copy()
    feats = pd.DataFrame({
        "indice_origen": q1.indice_origen, "sur": (q1.region_14 == "Sur").astype(int),
        "pueblo": (q1.localidad_14 == "Pueblo (<2,500)").astype(int), "lengua_indigena": q1.lengua_indigena,
        "padre_ausente": (q1.educ_padre == "No sabe / ausente").astype(int),
        "madre_trabajaba": q1.madre_trabajaba, "hacinamiento_14": q1.hacinamiento_14.fillna(q1.hacinamiento_14.median()),
    })
    Z = StandardScaler().fit_transform(feats)
    km = KMeans(k, n_init=20, random_state=SEED).fit(Z)
    q1["perfil"] = km.labels_
    prof = feats.assign(perfil=km.labels_).groupby("perfil").mean()
    for c in ["sur", "pueblo", "lengua_indigena", "padre_ausente", "madre_trabajaba"]:
        prof[c] = prof[c] * 100
    prof["n"] = q1.groupby("perfil").size()
    prof["% sigue Q1"] = q1.groupby("perfil").apply(lambda x: wavg(x.sigue_q1, x.factor) * 100)
    return prof.round(1).sort_values("% sigue Q1", ascending=False)


MED_NUM = T.NUM + ["migro_entidad"]
MED_CAT = T.CAT + ["educ", "empleo"]


def _fit_med(d):
    m = Pipeline([("p", T.preprocessor(MED_NUM, MED_CAT)), ("m", LogisticRegression(C=0.5, max_iter=5000))])
    return m.fit(d[MED_NUM + MED_CAT], d.sigue_q1.astype(int))


SUBIR = {"Primaria o menos": "Secundaria", "Secundaria": "Preparatoria", "Preparatoria": "Profesional", "Profesional": "Profesional"}


def _apply(d, esc):
    d = d.copy()
    if esc == "Continuidad (situación observada)":
        pass
    elif esc == "Mejora educativa (+1 nivel)":
        d["educ"] = d["educ"].map(SUBIR)
    elif esc == "Mejora educativa sin mejora laboral (todos informales)":
        d["educ"] = d["educ"].map(SUBIR)
        d.loc[d.empleo == "Formal", "empleo"] = "Informal"
    elif esc == "Mejora educativa con empleo formal":
        d["educ"] = d["educ"].map(SUBIR)
        d.loc[d.empleo == "Informal", "empleo"] = "Formal"
    elif esc == "Reducción de brecha territorial (Sur con perfil del Centro)":
        d.loc[d.region_14 == "Sur", "region_14"] = "Centro"
    return d


ESCENARIOS = ["Continuidad (situación observada)", "Mejora educativa (+1 nivel)",
              "Mejora educativa sin mejora laboral (todos informales)", "Mejora educativa con empleo formal",
              "Reducción de brecha territorial (Sur con perfil del Centro)"]


def escenarios_roadmap(df, n_boot=100):
    """Escenarios de la Fase 10 con el modelo de mediación (origen + escolaridad + empleo).
    Incertidumbre: se reestima el modelo en remuestreos bootstrap."""
    d = df[df.sigue_q1.notna() & df.educ.notna()].copy()
    rng = np.random.default_rng(SEED)
    res = {e: [] for e in ESCENARIOS}
    for b in range(n_boot + 1):
        db = d if b == 0 else d.iloc[rng.integers(0, len(d), len(d))]
        m = _fit_med(db)
        for e in ESCENARIOS:
            res[e].append(m.predict_proba(_apply(d, e)[MED_NUM + MED_CAT])[:, 1].mean() * 100)
    rows = []
    base = np.array(res[ESCENARIOS[0]])
    for e in ESCENARIOS:
        v = np.array(res[e]); dif = v - base
        rows.append({"Escenario": e, "% predicho que sigue en Q1": v[0],
                     "Cambio vs continuidad (pts)": dif[0],
                     "IC 95% inf": np.percentile(dif[1:], 2.5), "IC 95% sup": np.percentile(dif[1:], 97.5)})
    rows.append({"Escenario": "Choque adverso de empleo o ingreso", "% predicho que sigue en Q1": np.nan,
                 "Cambio vs continuidad (pts)": np.nan, "IC 95% inf": np.nan, "IC 95% sup": np.nan})
    return pd.DataFrame(rows).round(1), len(d)
