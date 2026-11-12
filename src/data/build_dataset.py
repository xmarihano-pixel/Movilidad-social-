"""Construye la tabla analítica final: limpieza + índices + variable objetivo."""
from src.config import PROCESSED, TABLES
from src.data import emovi
from src.features import indices


def main():
    raw = emovi.load_raw()
    emovi.missing_report(raw).to_csv(TABLES / "auditoria_faltantes.csv")
    df, cargas = indices.build(emovi.clean(raw))
    df.to_parquet(PROCESSED / "emovi_movilidad.parquet")
    for k, v in cargas.items():
        v.sort_values(ascending=False).round(3).to_csv(TABLES / f"{k}.csv", header=["carga"])
    return df


if __name__ == "__main__":
    main()
