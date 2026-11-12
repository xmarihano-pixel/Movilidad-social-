"""Índices de riqueza de origen y destino y variable objetivo de movilidad.

Siguiendo la práctica del CEEY, la posición socioeconómica se mide con un índice de
bienes y servicios del hogar (primer componente principal), porque la EMOVI no
pregunta el ingreso de los padres. Cada índice se convierte en quintiles ponderados
con el factor de expansión, dentro de cada cohorte de edad, para comparar a cada
persona con su propia generación.
"""
import numpy as np
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler


def wealth_index(df: pd.DataFrame, cols: list[str], weights: pd.Series) -> tuple[pd.Series, pd.Series]:
    X = df[cols].astype(float)
    X = X.fillna(X.mean())  # sólo <1-5% NS por ítem; se documenta en la auditoría
    Z = StandardScaler().fit_transform(X)
    pca = PCA(n_components=1).fit(Z)
    score = pd.Series(pca.transform(Z)[:, 0], index=df.index)
    load = pd.Series(pca.components_[0], index=cols)
    if load.sum() < 0:  # orientar: más bienes = mayor índice
        score, load = -score, -load
    print(f"  varianza explicada 1er componente: {pca.explained_variance_ratio_[0]:.1%}")
    return score, load


def weighted_quintile(x: pd.Series, w: pd.Series) -> pd.Series:
    order = x.sort_values().index
    cw = w.loc[order].cumsum() / w.sum()
    q = np.ceil(cw * 5).clip(1, 5).astype(int)
    return q.reindex(x.index)


def build(df: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    df = df.copy()
    o_cols = [c for c in df.columns if c.startswith("o_p") and not c.startswith("o_p33")] + \
             ["piso_tierra_14", "autos_14", "cuartos_14"]
    d_cols = [c for c in df.columns if c.startswith("d_p")] + ["piso_tierra", "autos"]
    df["piso_tierra_14"] = -df["piso_tierra_14"]  # tener piso de tierra resta
    df["piso_tierra"] = -df["piso_tierra"]
    print("Índice de origen:")
    df["indice_origen"], lo = wealth_index(df, o_cols, df["factor"])
    print("Índice de destino:")
    df["indice_destino"], ld = wealth_index(df, d_cols, df["factor"])
    df["piso_tierra_14"] = -df["piso_tierra_14"]
    df["piso_tierra"] = -df["piso_tierra"]

    df["q_origen"] = 0
    df["q_destino"] = 0
    for _, g in df.groupby("cohorte"):
        df.loc[g.index, "q_origen"] = weighted_quintile(g["indice_origen"], g["factor"])
        df.loc[g.index, "q_destino"] = weighted_quintile(g["indice_destino"], g["factor"])

    diff = df["q_destino"] - df["q_origen"]
    df["movilidad"] = np.select([diff > 0, diff < 0], ["Ascenso", "Descenso"], "Permanencia")
    df["salto_quintiles"] = diff
    # Objetivo principal ("pegajosidad"): entre quienes nacieron en el 20% más pobre,
    # ¿siguen en el 20% más pobre de adultos?
    df["sigue_q1"] = np.where(df["q_origen"] == 1, (df["q_destino"] == 1).astype(int), np.nan)
    return df, {"cargas_origen": lo, "cargas_destino": ld}
