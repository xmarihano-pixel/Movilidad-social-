"""Rutas y constantes del proyecto."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
INTERIM = ROOT / "data" / "interim"
PROCESSED = ROOT / "data" / "processed"
FIGURES = ROOT / "reports" / "figures"
TABLES = ROOT / "reports" / "tables"
MODELS = ROOT / "models"

EMOVI = RAW / "esru_emovi" / "Data" / "entrevistado_2023.dta"
EMOVI_DICT = RAW / "esru_emovi" / "Diccionario ESRU EMOVI 2023.xlsx"
CONEVAL = RAW / "coneval" / "pobreza_22.dta"
ENIGH = RAW / "enigh"
ENOE = RAW / "enoe"

SEED = 42

ENTIDADES = {
    1: "Aguascalientes", 2: "Baja California", 3: "Baja California Sur", 4: "Campeche",
    5: "Coahuila", 6: "Colima", 7: "Chiapas", 8: "Chihuahua", 9: "Ciudad de México",
    10: "Durango", 11: "Guanajuato", 12: "Guerrero", 13: "Hidalgo", 14: "Jalisco",
    15: "México", 16: "Michoacán", 17: "Morelos", 18: "Nayarit", 19: "Nuevo León",
    20: "Oaxaca", 21: "Puebla", 22: "Querétaro", 23: "Quintana Roo", 24: "San Luis Potosí",
    25: "Sinaloa", 26: "Sonora", 27: "Tabasco", 28: "Tamaulipas", 29: "Tlaxcala",
    30: "Veracruz", 31: "Yucatán", 32: "Zacatecas",
}
REGIONES = {1: "Norte", 2: "Norte-occidente", 3: "Centro-norte", 4: "Centro", 5: "Sur"}

for p in (INTERIM, PROCESSED, FIGURES, TABLES, MODELS):
    p.mkdir(parents=True, exist_ok=True)
