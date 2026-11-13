# Auditoría final contra la rúbrica (Fase 13)

Rúbrica: "Contenido esperado del reporte Proyecto Integrador" (según la sección 20 del roadmap).

| Requisito | Estado | Evidencia | Qué falta |
|---|---|---|---|
| Planteamiento y justificación | CUMPLIDO | notebook 00 | Redactarlo en el reporte |
| Descripción de datos | CUMPLIDO | notebook 01, `docs/base_de_datos.md` | — |
| Limpieza y preparación | CUMPLIDO | notebook 02, `src/`, bitácora | — |
| Análisis exploratorio | CUMPLIDO | notebook 03 (incluye Simpson y faltantes) | — |
| Modelos | CUMPLIDO | notebooks 04-05 (6 modelos + mediación + 3 clases) | — |
| Comparación y selección | CUMPLIDO | matriz de decisión, 10 semillas | — |
| Desarrollo matemático de 2 modelos | CUMPLIDO | `fundamentos_matematicos.md` (logística y RF, más PCA) | Pasarlo al PDF |
| Métricas | CUMPLIDO | AUC, PR-AUC, log loss, Brier, F1, matriz de confusión, calibración | — |
| Interpretación | CUMPLIDO | notebook 06 (RM, permutación, SHAP, perfiles) | — |
| Sesgos | CUMPLIDO | notebook 08 (red team + subgrupos) | — |
| Limitaciones | CUMPLIDO | notebook 08 | — |
| Conclusiones | PARCIAL | README | Redactarlas en el reporte |
| Trabajo futuro | PARCIAL | — | Ver la lista abajo |
| Referencias | PARCIAL | `referencias.md` | Verificar las marcadas con 🔎 |
| Reporte PDF | **NO CUMPLIDO** | — | Fase 12 |
| Código claro y reproducible | CUMPLIDO | notebooks ejecutados y `requirements.txt` | — |

## Trabajo futuro sugerido
1. Comparar con la EMOVI 2017 para ver cambios en el tiempo (con la misma metodología).
2. Agregar indicadores municipales de origen (p20_COD) del censo más cercano al año en que la persona tenía 14 años, en lugar de datos de 2022.
3. Evaluar la calidad educativa (no solo los años de estudio).
4. Un modelo con corrección de equidad por tono de piel.
5. Usar análisis de mediación formal para separar las vías educación → empleo → riqueza.

## Las cinco preguntas más difíciles que podría hacer un profesor
1. **"¿Por qué un índice de bienes y no el ingreso?"** → La EMOVI no tiene el ingreso de los padres; los bienes se recuerdan mejor y es la práctica del CEEY. Con el ingreso como destino, el resultado se mantiene (47% vs 51%).
2. **"Un AUC de 0.70 es bajo, ¿para qué sirve el modelo?"** → Su objetivo no es predecir personas sino medir cuánto pesan las circunstancias. Que no llegue a 0.9 es un hallazgo: la curva de aprendizaje muestra que el límite está en la información, no en el algoritmo.
3. **"¿Cómo saben que la educación causa la salida de la pobreza?"** → No lo sabemos. Es una asociación mediadora; se mide al mismo tiempo que el destino. Por eso no está en el modelo principal.
4. **"Si el tono de piel no es significativo, ¿por qué lo mencionan?"** → Porque el promedio oculta heterogeneidad: no hay brecha en el Sur, pero sí en el Norte y el Norte-occidente, y el modelo está mal calibrado para el tono oscuro. Es un hallazgo sobre los límites del modelo.
5. **"¿Los jóvenes tienen menos movilidad?"** → No podemos afirmarlo: es una sola encuesta y los bienes no son comparables entre generaciones. El efecto de cohorte puede ser un artefacto de medición.
