# Registro de experimentos (sección 14 del roadmap)

Dataset: `data/processed/emovi_movilidad.parquet` (ESRU-EMOVI 2023). Target: `sigue_q1`, salvo que se indique otro. Split: 80/20 estratificado, semilla 42, CV de 5 particiones. Preprocesamiento: imputación con la mediana, escalamiento y one-hot (`min_frequency = 30`) dentro del pipeline. Nunca se borra una fila: cada cambio es un experimento nuevo.

| Exp. | Fecha | Target | Modelo | Parámetros | AUC CV | AUC prueba | Subgrupos | Artefacto | Decisión |
|---|---|---|---|---|---|---|---|---|---|
| E001 | 2026-11-12 | sigue_q1 | Dummy (mayoritaria) | prior | 0.500 | 0.500 | — | `comparacion_modelos.csv` | Baseline |
| E002 | 2026-11-12 | sigue_q1 | Logística (solo índice de origen) | default | 0.531 | 0.556 | — | idem | Baseline |
| E003 | 2026-11-12 | sigue_q1 | Regresión logística | C = 0.5, L2 | 0.696 | 0.716 | Brecha por tono ≈ 11 pts | idem | **Elegido** |
| E004 | 2026-11-12 | sigue_q1 | Árbol de decisión | max_depth = 4, min_leaf = 50 | 0.652 | 0.681 | — | idem | Descartado (inestable) |
| E005 | 2026-11-12 | sigue_q1 | Random forest | 400 árboles, min_leaf = 20, sqrt | 0.690 | 0.722 | Brecha por tono ≈ 11 pts | idem | No supera a E003 |
| E006 | 2026-11-12 | sigue_q1 | Gradient boosting | depth 3, lr 0.05, 300 iter, l2 = 1 | 0.672 | 0.721 | Brecha por tono ≈ 10 pts | idem | No supera a E003; se usa para SHAP |
| E007 | 2026-11-12 | sigue_q1 | E003–E006 + escolaridad propia y migración (mediación) | igual | 0.737 (logística) | 0.737 | — | `comparacion_modelos_mediacion.csv` | Solo interpretativo |
| E008 | 2026-11-12 | movilidad (3 clases) | Logística multinomial + quintil de origen | default | — | ver notebook 05 | — | notebook 05 | Secundario |
| E009 | 2026-11-13 | sigue_q1 | Dummy estratificado | stratified | — | 0.501 | — | `metricas_completas.csv` | Baseline extra (Fase 6) |
| E010 | 2026-11-13 | sigue_q1 | Logística con class_weight = balanced | C = 0.5 | 0.696 | — | — | `class_weight.csv` | Sin cambio (clases 52/48) |
| E011 | 2026-11-13 | sigue_q1 | Logística, RF y GB con 10 semillas | igual | 0.701 / 0.697 / 0.689 | — | — | `sensibilidad_semillas.csv` | Confirma E003 |
| E012 | 2026-11-13 | sigue_q1 por **ingreso** | Regresión logística | C = 0.5 | ≈ 0.70 | — | — | notebook 05 | Stress test superado |
| E013 | 2026-11-13 | sigue_q1 | Logística de mediación (+ escolaridad y empleo), 100 bootstrap | C = 0.5 | — | — | — | `escenarios_roadmap.csv` | Escenarios de la Fase 10 |
