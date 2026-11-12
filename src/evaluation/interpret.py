"""Fases 8-10: modelo explicativo con errores robustos, importancia y escenarios."""
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
from sklearn.inspection import permutation_importance

from src.config import SEED


def logit_explicativo(d, extra=""):
    """Logit ponderado con errores agrupados por UPM (diseño muestral). Resultados en razones de momios."""
    d = d.dropna(subset=["hermanos", "indice_origen", "sigue_q1"]).copy()
    d["w"] = d["factor"] / d["factor"].mean()
    # En Q1 de origen casi nadie tiene padres con preparatoria o más (madre: 31 casos;
    # con 2 casos "Profesional" el modelo se separa). Se agrupa "Secundaria o más" sólo aquí.
    for c in ["educ_madre", "educ_padre"]:
        d[c] = d[c].replace({"Secundaria": "Secundaria o más", "Preparatoria": "Secundaria o más",
                             "Profesional": "Secundaria o más"})
    f = ("sigue_q1 ~ indice_origen + C(educ_madre, Treatment('Primaria o menos'))"
         " + C(educ_padre, Treatment('Primaria o menos')) + C(localidad_14, Treatment('Metrópoli'))"
         " + C(region_14, Treatment('Centro')) + C(tono_piel, Treatment('Medio (F-G)'))"
         " + mujer + lengua_indigena + hermanos + C(cohorte)" + extra)
    import statsmodels.api as sm
    mod = smf.glm(f, data=d, family=sm.families.Binomial(), var_weights=d["w"])
    rows = mod.data.row_labels
    mod = smf.glm(f, data=d.loc[rows], family=sm.families.Binomial(), var_weights=d.loc[rows, "w"])
    m = mod.fit(cov_type="cluster", cov_kwds={"groups": pd.factorize(d.loc[rows, "upm"])[0]})
    ci = m.conf_int()
    out = pd.DataFrame({"Razón de momios": np.exp(m.params), "IC 95% inf": np.exp(ci[0]),
                        "IC 95% sup": np.exp(ci[1]), "p-valor": m.pvalues}).round(3)
    out.index = (out.index.str.replace(r"C\((\w+), Treatment\('[^']+'\)\)\[T\.", r"\1 = ", regex=True)
                 .str.replace(r"C\((\w+)\)\[T\.", r"\1 = ", regex=True).str.replace("]", ""))
    return out.drop(index="Intercept"), m


def importance(model, te, num, cat, target="sigue_q1"):
    r = permutation_importance(model, te[num + cat], te[target], scoring="roc_auc",
                               n_repeats=20, random_state=SEED, n_jobs=-1)
    return pd.DataFrame({"Variable": num + cat, "Pérdida de AUC": r.importances_mean,
                         "desv.": r.importances_std}).sort_values("Pérdida de AUC", ascending=False).round(4)


def scenarios(model, d, num, cat):
    """Escenarios hipotéticos: cambia una circunstancia para todas las personas de Q1 de origen
    y compara la probabilidad media predicha. Son asociaciones del modelo, NO efectos causales."""
    base = model.predict_proba(d[num + cat])[:, 1].mean()
    esc = {
        "Madre con secundaria (en vez de primaria o menos)": ("educ_madre", "Primaria o menos", "Secundaria"),
        "Crecer en ciudad mediana (en vez de pueblo)": ("localidad_14", "Pueblo (<2,500)", "Ciudad mediana"),
        "Crecer en el Norte (en vez del Sur)": ("region_14", "Sur", "Norte"),
        "Tono de piel claro (en vez de oscuro)": ("tono_piel", "Oscuro (A-E)", "Claro (H-K)"),
    }
    rows = [{"Escenario": "Situación observada", "Personas afectadas": len(d), "Prob. media de seguir en Q1": base,
             "Cambio (puntos %)": 0.0}]
    for name, (col, old, new) in esc.items():
        mask = d[col] == old
        if mask.sum() == 0:
            continue
        d2 = d.copy()
        d2.loc[mask, col] = new
        p_old = model.predict_proba(d.loc[mask, num + cat])[:, 1].mean()
        p_new = model.predict_proba(d2.loc[mask, num + cat])[:, 1].mean()
        rows.append({"Escenario": name, "Personas afectadas": int(mask.sum()),
                     "Prob. media de seguir en Q1": p_new, "Cambio (puntos %)": (p_new - p_old) * 100})
    return pd.DataFrame(rows).round(3)
