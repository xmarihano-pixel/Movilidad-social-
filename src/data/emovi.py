"""Carga y limpieza de la ESRU-EMOVI 2023 (archivo de entrevistados).

Reglas: los datos originales no se modifican; los códigos "No sabe" (8, 98, 999)
se convierten en faltantes explícitos y se documentan; no se imputa en esta etapa.
"""
import warnings

import numpy as np
import pandas as pd

warnings.filterwarnings("ignore", category=pd.errors.PerformanceWarning)

from src.config import EMOVI, ENTIDADES, REGIONES

# Activos del hogar a los 14 años (origen) y actuales (destino). Sí=1, No=2, NS=8.
ORIGEN_SI_NO = [f"p26{c}" for c in "abcde"] + [f"p29{c}" for c in "abcdefg"] + \
               [f"p31{c}" for c in "abcdefghijklmno"] + [f"p32{c}" for c in "abcdefghijklmno"]
DESTINO_SI_NO = [f"p94{c}" for c in "abcdefg"] + [f"p95{c}" for c in "abcde"] + \
                [f"p96{c}" for c in "abcdefghijklmnopqr"] + [f"p97{c}" for c in "abcdefghijklmn"]

EDUC = {1: "Primaria o menos", 2: "Secundaria", 3: "Preparatoria", 4: "Profesional"}
CLASE = {1: "Agrícola", 2: "Manual baja calif.", 3: "Manual alta calif.", 4: "Comercio",
         5: "No manual baja calif.", 6: "No manual alta calif."}
TAM_LOCALIDAD = {1: "Metrópoli", 2: "Ciudad grande", 3: "Ciudad mediana", 4: "Ciudad chica", 5: "Pueblo (<2,500)"}


def load_raw() -> pd.DataFrame:
    return pd.read_stata(EMOVI, convert_categoricals=False)


def _si_no(s: pd.Series) -> pd.Series:
    return s.map({1: 1.0, 2: 0.0})  # 8 (NS) -> NaN


def clean(raw: pd.DataFrame) -> pd.DataFrame:
    e = raw.copy()
    out = pd.DataFrame(index=e.index)
    out["id"] = e["index"]
    out["factor"] = e["factor"]
    out["upm"] = e["upm_muestra"]
    out["estrato"] = e["est"]

    # Persona
    out["mujer"] = (e["sexo"] == 2).astype(int)
    out["edad"] = e["edad"]
    out["cohorte"] = e["cohorte"].map({1: "25-34", 2: "35-44", 3: "45-54", 4: "55-64"})
    out["lengua_indigena"] = (e["p111"] == 1).astype(int)
    out["autoadscripcion"] = e["p110"].map({1: "Negra", 2: "Indígena", 3: "Blanca", 4: "Mestiza", 5: "Ninguna"})
    # Tono de piel: escala PERLA autopercibida (A=más oscuro ... K=más claro) agrupada.
    out["tono_piel"] = e["p112"].map(lambda x: "Oscuro (A-E)" if x in list("ABCDE")
                                     else "Medio (F-G)" if x in list("FG") else "Claro (H-K)")
    out["luminosidad_piel"] = e["p113dL"]  # colorímetro CIELab L*; mayor = más claro

    # Origen (a los 14 años)
    out["entidad_14"] = e["p19"].map(ENTIDADES)
    out["region_14"] = e["region_14"].map(REGIONES)
    out["localidad_14"] = e["p21"].map(TAM_LOCALIDAD)
    out["personas_hogar_14"] = e["p22"].where(e["p22"] < 999)
    out["cuartos_14"] = e["p23"]
    out["hacinamiento_14"] = out["personas_hogar_14"] / e["p24"].clip(lower=1)
    out["piso_tierra_14"] = (e["p25"] == 1).astype(int)
    out["autos_14"] = e["p30"].clip(upper=5)
    out["vivia_ambos_padres"] = (e["p39"] == 3).astype(int)
    out["sosten_madre"] = (e["p40"] == 2).astype(int)
    # Educación y ocupación de los padres: el faltante se conserva como categoría propia
    # porque suele indicar padre/madre ausente o desconocido (no es aleatorio).
    out["educ_padre"] = e["educp"].map(EDUC).fillna("No sabe / ausente")
    out["educ_madre"] = e["educm"].map(EDUC).fillna("No sabe / ausente")
    out["clase_padre"] = e["clasep"].map(CLASE).fillna("No sabe / no trabajaba")
    out["madre_trabajaba"] = (e["p51"] == 1).astype(int)
    out["hermanos"] = (e["p57"].where(e["p57"] < 98) - 1).clip(lower=0)
    out["orden_nacimiento"] = e["p58"]
    out["escalera_origen_subj"] = e["p104"]
    for c in ORIGEN_SI_NO:
        out[f"o_{c}"] = _si_no(e[c])
    for c in [f"p33{x}" for x in "abcdefgh"]:
        out[f"o_{c}"] = _si_no(e[c])

    # Destino (hoy)
    out["entidad"] = e["entidad"].map(ENTIDADES)
    out["entidad_cve"] = e["entidad"]
    out["entidad_14_cve"] = e["p19"]
    out["region"] = e["region"].map(REGIONES)
    out["rural"] = (e["rururb"] == 2).astype(int)
    out["educ"] = e["educ"].map(EDUC)
    out["clase"] = e["clase"].map(CLASE)
    out["ingreso_pc"] = e["ingc_pc"]
    out["piso_tierra"] = (e["p88"] == 1).astype(int)
    out["autos"] = e["p99"].clip(upper=5)
    out["hacinamiento"] = e["tamhog"] / e["p89"].clip(lower=1)
    out["escalera_actual_subj"] = e["p103"]
    for c in DESTINO_SI_NO:
        out[f"d_{c}"] = _si_no(e[c])
    out["migro_entidad"] = (e["p19"] != e["entidad"]).astype(int)
    # Empleo actual: formal = ocupado con seguridad social por su trabajo (IMSS, ISSSTE u otra).
    out["empleo"] = np.select([e["ocup"] != 1, e["p68"].isin([1, 2, 3])],
                              ["No ocupado", "Formal"], "Informal")
    # Movilidad educativa respecto al padre o madre con más escolaridad (escala 1-4).
    educ_padres = pd.concat([e["educp"], e["educm"]], axis=1).max(axis=1)
    out["educ_padres_max"] = educ_padres
    out["supero_educ_padres"] = np.where(e["educ"].notna() & educ_padres.notna(),
                                         (e["educ"] > educ_padres).astype(float), np.nan)
    return out.copy()


def missing_report(raw: pd.DataFrame) -> pd.DataFrame:
    """Faltantes y códigos 'No sabe' por variable del archivo original."""
    rep = pd.DataFrame({
        "faltante_pct": raw.isna().mean() * 100,
        "codigo_ns_pct": raw.isin([8, 98, 999, 999998, 999999]).mean() * 100,
    })
    return rep.round(2).sort_values("faltante_pct", ascending=False)
