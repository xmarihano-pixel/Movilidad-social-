"""Pruebas mínimas de integridad (auditoría C-14).

Requieren haber construido `data/processed/emovi_movilidad.parquet` (notebook 02 o
`python -m src.data.build_dataset`). Si no existe, se omiten.
"""
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "processed" / "emovi_movilidad.parquet"
pytestmark = pytest.mark.skipif(not DATA.exists(), reason="Falta el dataset procesado")


@pytest.fixture(scope="module")
def df():
    return pd.read_parquet(DATA)


def test_filas_y_folios(df):
    assert len(df) == 17843
    assert df["id"].is_unique


def test_quintiles_ponderados_al_20(df):
    w = df["factor"]
    for q in ["q_origen", "q_destino"]:
        shares = df.groupby(q)["factor"].sum() / w.sum()
        assert set(df[q].unique()) == {1, 2, 3, 4, 5}
        assert np.allclose(shares.values, 0.2, atol=0.01)


def test_target_solo_en_q1(df):
    assert df.loc[df.q_origen != 1, "sigue_q1"].isna().all()
    assert set(df.loc[df.q_origen == 1, "sigue_q1"].unique()) <= {0.0, 1.0}


def test_sin_leakage_en_predictores():
    from src.models import train as T
    destino = {"indice_destino", "q_destino", "educ", "clase", "ingreso_pc", "empleo", "movilidad", "sigue_q1"}
    assert not destino & set(T.NUM + T.CAT)


def test_cifra_titular(df):
    from src.evaluation.extra import cboot
    r = cboot(df[df.sigue_q1.notna()], B=200)
    assert 49 < r["%"] < 53
    assert r["IC 95% inf"] < r["%"] < r["IC 95% sup"]
