"""Indicadores estatales de contexto (2022) a partir de CONEVAL y ENOE.

Decisión: no se unen a la EMOVI persona por persona (no hay identificadores
comunes). Se resumen por entidad federativa y se usan sólo como contexto territorial.
La medición de pobreza de CONEVAL ya se construye a partir de la ENIGH 2022, por lo que
la ENIGH no se procesa por separado (evita duplicar la misma fuente).
"""
import zipfile
import numpy as np
import pandas as pd

from src.config import CONEVAL, ENOE, ENTIDADES


def coneval_estatal() -> pd.DataFrame:
    c = pd.read_stata(CONEVAL, columns=["ent", "factor", "pobreza", "pobreza_e", "ictpc"],
                      convert_categoricals=False)
    c = c.dropna(subset=["pobreza"])  # CONEVAL deja fuera a quienes no entran al cálculo
    c["ent"] = c["ent"].astype(int)
    g = c.groupby("ent")
    out = pd.DataFrame({
        "pobreza_pct": g.apply(lambda d: np.average(d["pobreza"], weights=d["factor"]) * 100),
        "pobreza_extrema_pct": g.apply(lambda d: np.average(d["pobreza_e"], weights=d["factor"]) * 100),
        "ingreso_pc_mensual": g.apply(lambda d: np.average(d["ictpc"], weights=d["factor"])),
    })
    nac = {"pobreza_pct": np.average(c["pobreza"], weights=c["factor"]) * 100,
           "pobreza_extrema_pct": np.average(c["pobreza_e"], weights=c["factor"]) * 100}
    out.index.name = "entidad_cve"
    return out, nac


def enoe_informalidad() -> pd.DataFrame:
    """Tasa de informalidad laboral (TIL1) por entidad, promedio de los 4 trimestres de 2022."""
    res = []
    for z in sorted(ENOE.glob("*.zip")):
        with zipfile.ZipFile(z) as zf:
            name = [n for n in zf.namelist() if "SDEM" in n.upper()][0]
            with zf.open(name) as fh:
                cols = ["ent", "clase2", "emp_ppal", "eda", "r_def", "c_res", "fac_tri"]
                d = pd.read_stata(fh, columns=None, convert_categoricals=False)
                d.columns = d.columns.str.lower()
                d = d[[c for c in cols if c in d.columns]]
        for c in ["eda", "r_def", "c_res", "clase2", "emp_ppal", "ent", "fac_tri"]:
            d[c] = pd.to_numeric(d[c], errors="coerce")
        d = d[(d["r_def"] == 0) & (d["c_res"] != 2) & (d["eda"].between(15, 98)) & (d["clase2"] == 1)]
        t = d.groupby("ent").apply(lambda x: np.average(x["emp_ppal"] == 1, weights=x["fac_tri"]) * 100)
        res.append(t.rename(name))
        print("  ", name, "listo")
    out = pd.concat(res, axis=1).mean(axis=1).to_frame("informalidad_pct")
    out.index = out.index.astype(int)
    out.index.name = "entidad_cve"
    return out


def build() -> pd.DataFrame:
    con, nac = coneval_estatal()
    inf = enoe_informalidad()
    out = con.join(inf)
    out.insert(0, "entidad", out.index.map(ENTIDADES))
    return out.round(2), nac
