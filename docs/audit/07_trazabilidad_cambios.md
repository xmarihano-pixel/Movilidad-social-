# Trazabilidad antes y después de la auditoría

- **Versión original:** rama `congelado-auditoria-v1` (commit `10533d7`). Tablas originales en `docs/audit/tablas_originales/`.
- **Versión corregida:** rama `correcciones-auditoria`, fusionada a `main` tras la validación.
- **Validación posterior:** los 9 notebooks se ejecutaron sin errores; 19 tablas no cambiaron, 10 cambiaron (todas por correcciones aprobadas) y hay 2 tablas nuevas. Las pruebas de `tests/` pasan (5/5). Ninguna afirmación retirada aparece como hallazgo vigente.

| Elemento | Estado original | Hallazgo | Cambio aprobado | Estado posterior | Diferencia | Efecto en conclusiones |
|---|---|---|---|---|---|---|
| Observaciones / variables | 17,843 / 145 | — | — | 17,843 / 147 (+`empleo`, `supero_educ_padres` ya existían; sin cambios en la muestra) | Ninguna | Ninguno |
| Definición del target | `sigue_q1` | H-07 | C-09 (solo lenguaje) | Igual | Ninguna | Se describe como "20% de hogares con menos bienes" |
| Persistencia en Q1 | 51.1% (IC 48–55 README / 47.6–54.5 NB 08) | H-02 | C-03 | 51.1% (**IC 46.3–55.4**, n efectivo 815) | IC más amplio | La conclusión central se mantiene |
| Brecha por tono oscuro | +11.2 pts (partición de prueba, n = 114) | H-01 | C-01 | **−0.01 pts (IC −4.0 a +3.9)**, fuera de muestra, n = 578 | Desaparece | **Hallazgo retirado** (D25) |
| Matriz de decisión, brecha por tono | 10.5–11.5 pts en los 4 modelos | H-01 | C-01 | 0.0 / 3.9 / 3.1 / 0.2 pts (logística / árbol / RF / GB) | Desaparece | La selección (logística) no cambia |
| Tiempo de entrenamiento | No reportado | Rúbrica | C-17 | Logística 0.04 s · Árbol 0.03 s · GB 0.24 s · RF 0.87 s | Nuevo | Refuerza la elección |
| RM pueblo (ref. metrópoli → ciudad) | 0.77 (p = 0.59), inestable | H-06 | C-07 | **1.52 (IC 1.11–2.09, p = 0.009)**; sin pesos 1.46 | Cambia de signo y se vuelve significativa | **Nuevo hallazgo:** H2 rural apoyada (D36) |
| RM Sur / Norte / lengua | 1.89 / 0.40 / 1.91 | — | C-07 (cambio de especificación) | 1.84 / 0.39 / 1.88 | Mínima | Ninguno |
| Tasas por subgrupo | Sin IC | H-03 | C-03/C-04 | Con IC por UPM y n efectivo en tablas y figuras | Nuevo | Tono de piel: IC traslapados → sin evidencia |
| Tono × región ("Simpson") | Presentado como hallazgo | H-05 | C-05 | Pregunta abierta, con IC | — | Sale de los hallazgos |
| Análisis estatal | r = 0.56 como hallazgo | H-04 | C-06 | r = 0.56, **exploratorio**, con el n efectivo visible | Etiqueta | Se queda en el cartel con poco espacio (D29) |
| Escenarios (cambio vs continuidad) | −10.1 / −8.9 / −16.6 / −5.2 pts (sin pesos, bootstrap simple) | H-10 | C-10 | −9.9 / −9.0 / −16.3 / −4.7 pts (ponderado, bootstrap por UPM) | Mínima | Ninguno |
| Efecto cohorte | "Posible artefacto de medición" | H-19 | C-11 | Artefacto de bienes modernos **refutado**; queda el ciclo de vida | Interpretación | Confianza medio-baja |
| `requirements.txt` | Sin versiones | H-14 | C-14 | Versiones fijas | — | — |
| Pruebas | Ninguna | H-17 | C-14 | 5 pruebas en `tests/` | — | — |
| Selección de k (K-Means) | Sin criterio | H-16 | C-15 | Silueta reportada (k = 2..6) | — | Ninguno |
| Rúbricas | Ausentes | H-12 | — | `docs/rubric/` (reporte y póster) | — | La auditoría final ya puede evaluarse contra ellas |
| Referencias | Sin enlaces | H-13 | D35 | Con enlaces; verificación pospuesta | — | — |
| Autoadscripción y tono autopercibido | En el modelo | H-08 | **No aprobado** (D28) | Sin cambio | — | Se interpretan con la restricción de que se miden hoy |
