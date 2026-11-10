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
    style F0 fill:#fde68a,stroke:#b45309
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
jupyter notebook
```

## Estado

Fase 0 — Constitución y control del proyecto.
