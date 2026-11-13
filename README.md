# ¿Qué tan pegajosa es la pobreza?

Proyecto de Machine Learning sobre movilidad social en México.

> ¿En qué medida las condiciones socioeconómicas de origen están asociadas con la posición económica alcanzada en la edad adulta en México, y qué factores individuales, familiares, territoriales y estructurales aumentan o reducen la probabilidad de movilidad social ascendente, permanencia o descenso?

El documento maestro con fases, prompts, bitácoras y reglas metodológicas está en [`roadmap.md`](roadmap.md).

## ¿Cómo funciona el proyecto?

```mermaid
flowchart LR
    A["👶 Origen<br/>¿cómo vivía a los 14 años?"] --> C{"📈 Movilidad<br/>¿subió, se quedó o bajó?"}
    B["🧑 Destino<br/>¿cómo vive hoy?"] --> C
    D["🌎 Contexto<br/>sexo, región, lengua, etc."] --> C
    C --> E["🤖 Modelos de Machine Learning"]
    E --> F["📊 Resultados y reporte"]
```

## Resultados principales

> Fuente: ESRU-EMOVI 2023 (17,843 personas de 25 a 64 años, que representan a 60 millones). Todo es **asociación, no causalidad**.

![Matriz de transición](reports/figures/01_matriz_transicion.png)

| Hallazgo | Dato |
|---|---|
| 🔒 **La pobreza es pegajosa** | **51%** de quienes crecen en el 20% más pobre siguen ahí de adultos (IC 95%: 48–55%). Solo **2%** llega al 20% más rico |
| 🔒 **La riqueza también** | 55% de quienes crecen en el 20% más rico siguen ahí |
| 🧭 **La región pesa más que todo** | Seguir en el 20% más pobre: **64%** si creció en el Sur vs **23%** en el Norte |
| 🗣️ **Lengua indígena** | **69%** vs 47%. Casi el doble de momios, aun comparando personas de la misma región y con un origen similar |
| 🎓 **La educación propia es la salida** | 56% sigue en Q1 con primaria o menos vs **18%** con estudios profesionales (mediadora, no es origen) |
| 🗺️ **Contexto estatal** | Los estados con más pobreza en 2022 (CONEVAL) tienen pobreza más pegajosa (r = 0.56) |
| 🤖 **Modelo** | La regresión logística (AUC 0.70) iguala a random forest y gradient boosting, y se eligió por ser interpretable |
| ⚠️ **Sesgo detectado** | El modelo subestima en ≈11 puntos la persistencia de las personas de tono de piel oscuro |
| ✅ **Robusto** | Entre 47% y 51% con tres definiciones distintas de riqueza |
| ➕ **Desventajas acumuladas** | Sur + pueblo + lengua indígena: 82% sigue en Q1 (vs 30% sin ninguna) |
| 🔀 **El promedio engaña** | La brecha por tono de piel no existe en el Sur, pero es grande en el Norte |

### Hipótesis del roadmap (H001–H005)
| # | Hipótesis | Estado |
|---|---|---|
| H001 | El origen se asocia con la posición adulta | ✅ Apoyada provisionalmente |
| H002 | La educación modera la persistencia | ✅ Apoyada provisionalmente (mediadora) |
| H003 | El efecto de la educación varía por región | ⚪ Sin evidencia (p ≈ 0.26) |
| H004 | Movilidad educativa sin movilidad económica equivalente | ✅ Apoyada: 43% de quienes superaron a sus padres sigue en Q1 |
| H005 | Las desventajas combinadas informan más | ✅ Se acumulan (30% → 82%), ⚪ pero sin sinergia |

### Hipótesis del equipo
| # | Hipótesis | Veredicto |
|---|---|---|
| H1 | Más de 40% de quienes nacen en Q1 siguen en Q1 | ✅ Se confirma (51%) |
| H2 | Crecer en el Sur o en zona rural aumenta la persistencia | ✅ Sur · ⚠️ Rural solo en la descripción |
| H3 | La escolaridad de la madre reduce la persistencia | ❌ No se observa dentro de Q1 (casi no hay variación) |
| H4 | Lengua indígena y tono oscuro aumentan la persistencia | ✅ Lengua · ⚠️ Tono: no significativo al controlar región y lengua |
| H5 | Los modelos complejos no superan a la logística | ✅ Se confirma |

## Notebooks (ejecutados, se pueden ver directo en GitHub)

| # | Notebook | Fase del roadmap |
|---|---|---|
| 00 | [Contexto, preguntas e hipótesis](notebooks/00_context_and_scope.ipynb) | 0, 1, 2 |
| 01 | [Auditoría de datos](notebooks/01_data_audit.ipynb) | 3 |
| 02 | [Preparación e índices](notebooks/02_data_preparation.ipynb) | 4 |
| 03 | [Análisis exploratorio](notebooks/03_eda.ipynb) | 5 |
| 04 | [Baselines](notebooks/04_baselines.ipynb) | 6 |
| 05 | [Modelos y comparación](notebooks/05_modeling.ipynb) | 7 |
| 06 | [Interpretación](notebooks/06_interpretability.ipynb) | 8, 9 |
| 07 | [Escenarios](notebooks/07_scenarios.ipynb) | 10 |
| 08 | [Validación, sesgos y robustez](notebooks/08_final_validation.ipynb) | 11, 13 |

Más documentos: [decisiones](docs/decisions/bitacora_decisiones.md) · [experimentos](docs/registro_experimentos.md) · [fundamentos matemáticos](docs/report/fundamentos_matematicos.md) · [auditoría final](docs/report/auditoria_final.md) · [referencias](docs/report/referencias.md)

| Documento | Qué contiene |
|---|---|
| [`docs/base_de_datos.md`](docs/base_de_datos.md) | Qué base usaremos y qué debe tener |
| [`docs/variables.md`](docs/variables.md) | Lista de variables por sección |
| [`roadmap.md`](roadmap.md) | Plan completo por fases |

## Avance por fases

```mermaid
flowchart TD
    F0["0 · Constitución"] --> F1["1 · Preguntas e hipótesis"] --> F2["2 · Definir movilidad"] --> F3["3 · Auditar datos"]
    F3 --> G{"Puerta de datos<br/>🟢 🟡 🔴"}
    G --> F4["4 · Preparar datos"] --> F5["5 · Exploración"] --> F6["6 · Baselines"] --> F7["7 · Modelos"]
    F7 --> F8["8 · Matemáticas"] --> F9["9 · Interpretación"] --> F10["10 · Escenarios"] --> F11["11 · Sesgos"] --> F12["12 · Reporte"]
    style F12 fill:#fde68a,stroke:#b45309
```

## Estructura

- `data/` — `raw` (nunca se edita), `interim`, `processed`, `external`. No se versiona en Git.
- `docs/` — rúbrica, referencias, decisiones y reporte.
- `notebooks/` — numerados, se ejecutan en orden.
- `src/` — código reutilizable (datos, features, modelos, evaluación, visualización).
- `reports/` — figuras, tablas y reporte final generados desde código.
- `models/` — modelos guardados (con versión de datos y parámetros).
- `tests/` — pruebas.

## Reproducir

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
unzip data/esru_emovi.zip -d data/raw/esru_emovi   # ver docs/base_de_datos.md para CONEVAL y ENOE
jupyter notebook                                    # ejecutar 01 → 08 en orden
```

## Estado

Fases 0 a 11 hechas y en estado **PROPUESTA**: falta la revisión humana que pide el roadmap (ver la sección 6.1 de `roadmap.md`). Siguiente: **Fase 12 — cartel y reporte PDF**.
