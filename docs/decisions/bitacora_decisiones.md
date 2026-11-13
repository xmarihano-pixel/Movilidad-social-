# Bitácora de decisiones

Cada decisión indica qué se decidió, por qué y qué consecuencias tiene. No se borran filas: si algo cambia, se agrega una fila nueva.

| # | Fase | Decisión | Por qué | Consecuencia |
|---|---|---|---|---|
| D01 | 3 | **ESRU-EMOVI 2023** es la fuente principal | Es la única de las fuentes recibidas que tiene origen (hogar a los 14 años) y destino para la misma persona | Se puede medir movilidad intergeneracional |
| D02 | 3 | CONEVAL 2022 y ENOE 2022 se usan solo como **contexto estatal** | No comparten identificadores con la EMOVI | Las conclusiones territoriales son agregadas, no individuales |
| D03 | 3 | La ENIGH 2022 **no se procesa por separado** | La medición de pobreza de CONEVAL ya se construye con la ENIGH 2022 | Se evita duplicar la misma fuente |
| D04 | 3 | Puerta de datos: 🟢 **VERDE** | Hay origen, destino, ponderadores y diseño muestral | Ruta: clasificación más análisis de transiciones |
| D05 | 2 | Posición socioeconómica = **índice de bienes (PCA)**, no ingreso | La EMOVI no pregunta el ingreso de los padres; es la práctica del CEEY | Se mide riqueza del hogar, no ingreso corriente |
| D06 | 2 | Quintiles **ponderados y dentro de cada cohorte** | Comparar a cada persona con su propia generación | Reduce el sesgo de ciclo de vida y de bienes nuevos (celular, internet) |
| D07 | 2 | Objetivo principal: `sigue_q1` (nació en Q1 y sigue en Q1) | Responde directamente a "¿qué tan pegajosa es la pobreza?" | Muestra de modelado: 2,674 personas |
| D08 | 2 | Objetivo secundario: movilidad en 3 clases | Pedido en el roadmap; es útil como descripción | Se reporta, pero no es el centro (es mecánico en los extremos) |
| D09 | 4 | Los faltantes en la escolaridad u ocupación de los padres se conservan como **categoría "No sabe / ausente"** | No son aleatorios: suelen indicar padre o madre ausente (principio 7) | Sin imputación ciega |
| D10 | 4 | "No sabe" en bienes (< 5%) se reemplaza por la media **solo para construir el índice** | El efecto es mínimo y evita perder casos | Documentado en la auditoría |
| D11 | 4 | La escolaridad propia, la ocupación, el ingreso y los bienes actuales **no** son predictores del modelo principal | Son parte del destino (*leakage*) o mediadoras | La escolaridad propia se analiza en un modelo de mediación aparte |
| D12 | 4 | Partición 80/20 estratificada, validación cruzada de 5 particiones, semilla 42 | Reproducibilidad | — |
| D13 | 6 | Métrica principal: **AUC**; también exactitud balanceada, F1 y Brier | Las clases están casi balanceadas (52/48); importa ordenar el riesgo y calibrar | — |
| D14 | 7 | Los modelos se entrenan **sin ponderar**; los resultados descriptivos sí se ponderan | Los factores van de 4 a 144,889 y desestabilizan el entrenamiento | Las predicciones son para la muestra; las tasas, para la población |
| D15 | 7 | Se elige la **regresión logística** | Tiene el mayor AUC en CV (0.70), es estable e interpretable; RF y GB no la superan por más de 0.01 | Regla congelada antes de ver resultados |
| D16 | 8 | En el logit explicativo, la escolaridad de los padres se agrupa en "Secundaria o más" | Dentro de Q1, solo 2 madres son profesionistas: causaban separación perfecta (RM = 6×10⁸) | Pérdida sustantiva mínima; documentado |
| D17 | 10 | Se elimina el escenario "madre con preparatoria" | Solo 29 casos en Q1; el modelo agrupa esa categoría como poco frecuente | Se conserva el escenario "madre con secundaria" |
| D18 | 11 | Se reporta el sesgo del modelo con el tono de piel oscuro | Subestima la persistencia en ≈11 puntos | El modelo no debe usarse para focalizar sin corrección |
| D19 | 5 | Empleo formal = ocupado con seguridad social por su trabajo (IMSS, ISSSTE u otra; p68) | Es la definición de informalidad más cercana a la de INEGI que permite la EMOVI | Solo para la descripción y la mediación (riesgo de causalidad inversa) |
| D20 | 10 | Los escenarios de la Fase 10 usan el **modelo de mediación** (origen + escolaridad + empleo), con IC de 100 remuestreos bootstrap | Los escenarios educativos y laborales del roadmap requieren esas variables | Se presentan como asociaciones, con lenguaje condicional |
| D21 | 10 | Se **rechaza** el escenario de "choque adverso" | La EMOVI no mide choques; sería extrapolar (regla del roadmap) | Queda como trabajo futuro |
| D22 | 9 | Perfiles con K-Means (k = 4) sobre 7 circunstancias de origen | Ilustrativo, no sustituye al target (roadmap, Fase 7.6) | No se usan como prueba |
| D23 | 9 | SHAP sobre gradient boosting (modelo complejo) para contrastarlo con la logística | Convergencia de evidencia entre los dos tipos de modelo | Coinciden en las 3 variables principales |
| D24 | 0 | **Todas las fases quedan como PROPUESTA** hasta la revisión humana | Regla de avance del roadmap: no se avanza solo porque una IA produjo una respuesta | El equipo debe marcar APROBADA / APROBADA CON CAMBIOS / REABRIR |
