# Auditoría integral y plan de acción
## ¿Qué tan pegajosa es la pobreza? Movilidad social en México

| Campo | Valor |
|---|---|
| Repositorio auditado | `xmarihano-pixel/Movilidad-social-`, rama `main` |
| Versión congelada | commit `10533d74290c15c92b4ad017963e48f4c7eee086` |
| Fecha | 2026-11-15 |
| Modo | **Solo lectura.** No se modificó ningún archivo del repositorio. Las verificaciones se ejecutaron en una copia aislada fuera de él |
| Entorno de verificación | Python 3.13.18 · pandas 3.0.5 · scikit-learn 1.9.1 · statsmodels 0.15.0 · shap 0.54.1 · numpy 2.5.3 |
| Conflicto de interés | El análisis auditado lo construyó el mismo asistente que hace esta auditoría. Por eso se buscó activamente refutar los resultados, con pruebas independientes y no solo releyendo el código |

---

## 1. Resumen ejecutivo

**Dictamen: APROBADO CON CAMBIOS.**

El núcleo del proyecto es sólido y defendible. La ESRU-EMOVI 2023 sí permite medir **movilidad intergeneracional relativa** (riqueza del hogar a los 14 años frente a la actual). El hallazgo central se sostiene con varias definiciones: **≈ 1 de cada 2 personas que crecen en el 20% más pobre sigue ahí de adulta** (51.1%, IC 95% por conglomerados 46–55%). También son robustos, con pesos y sin pesos, el gradiente territorial (Sur frente a Norte), la asociación con hablar lengua indígena y la acumulación de desventajas.

Hay que corregir antes de redactar el reporte y el cartel:

1. **Un hallazgo titular es falso (CRÍTICO para la narrativa).** El "sesgo de 11 puntos del modelo contra las personas de tono oscuro" viene de **una sola partición de prueba** con 114 personas. Con predicciones fuera de muestra para las 2,674 personas, la brecha es **0.0 puntos (IC 95%: −4.2 a +3.6)**. Hay que retirarlo de 7 documentos.
2. **El intervalo de confianza titular está subestimado.** El README dice 48–55%, pero un bootstrap que respeta el diseño muestral (conglomerados) da **46.3–55.4%**.
3. **El análisis por estado no es defendible como resultado.** La EMOVI no está diseñada para ser representativa por estado; el tamaño efectivo de muestra mediano por estado es **31** (Ciudad de México: 18). La correlación r = 0.56 con la pobreza de CONEVAL debe quedar como exploratoria o retirarse del cartel.
4. **El "efecto Simpson" por tono de piel y región no es significativo.** Las celdas tienen entre 24 y 50 personas, con intervalos que se traslapan ampliamente.
5. **Las cifras por subgrupo carecen de intervalos.** Con los factores de expansión, el tamaño efectivo de muestra de Q1 es 815 (no 2,674); en el Norte es 44.

También hay hallazgos favorables nuevos: los errores estándar del modelo explicativo se verificaron con un cálculo manual independiente (coinciden al 100%), y la hipótesis de que el "efecto cohorte" fuera un artefacto de los bienes modernos se **refutó**: el efecto persiste sin esos bienes.

---

## 2. Alcance y metodología de la auditoría

| Paso | Qué se hizo |
|---|---|
| Congelamiento | Se registró el commit, el entorno y una copia de las 30 tablas originales (`tablas_originales/`) |
| Reproducción | Se ejecutaron los 9 notebooks desde cero en una copia aislada y se compararon las tablas con las originales (sección 4.3) |
| Verificación independiente | 3 scripts nuevos (`checks1.py`, `checks2.py`, `checks3.py`) prueban empates en los quintiles, tamaño efectivo de muestra, IC por conglomerados, calibración fuera de muestra, sensibilidad a los pesos, multicolinealidad, errores estándar, artefactos de cohorte y variables de medición actual |
| Revisión documental | README, roadmap v1.1, bitácora, registro de experimentos, fundamentos matemáticos, auditoría previa y referencias |

**No verificado:**
- La rúbrica oficial ("Contenido esperado del reporte" y "Rúbrica de Evaluación de Proyectos Finales — Póster 2025B"). **No está en el repositorio** (`docs/rubric/` está vacío).
- Las referencias bibliográficas contra sus fuentes originales.
- La cifra de persistencia que publica el CEEY.
- La definición de informalidad de la ENOE contra la tasa oficial TIL1 de INEGI.

---

## 3. Inventario del repositorio

| Ruta | Contenido | Observación |
|---|---|---|
| `roadmap.md` | Roadmap maestro v1.1 con las secciones 9–14 llenas | Todas las fases en estado PROPUESTA: **no hay aprobación humana registrada** |
| `README.md` | Resumen, resultados, hipótesis | Contiene 3 afirmaciones a corregir (sección 13) |
| `data/*.zip` | EMOVI 2023 y 7 tablas de la ENIGH 2022 (zips originales) | Preservados ✅ |
| Releases `base-datos-Coneval` y `Enoe-INEGI` | `pobreza_22.dta`; ENOE T1–T4 2022 | Se descargan a mano: reproducibilidad parcial |
| `data/raw`, `data/processed` | Ignorados por Git | Se regeneran con los notebooks 01–02 |
| `src/` | 9 módulos: config, data (emovi, context, build_dataset), features (indices), models (train, diagnostics), evaluation (interpret, extra), visualization (plots) | Modular ✅ |
| `notebooks/00–08` | 9 notebooks ejecutados con salidas | Sin errores |
| `reports/figures` (18), `reports/tables` (30) | Se generan desde el código | ✅ |
| `docs/` | base_de_datos, variables, bitácora (D01–D24), registro de experimentos (E001–E013), fundamentos matemáticos, auditoría previa, referencias | `docs/rubric/` y `docs/references/` vacíos |
| `models/` | Vacío | Los modelos no se guardan; se reentrenan (deterministas con semilla 42) |
| `tests/` | Vacío | `pytest` está en requirements, pero no hay pruebas |
| `requirements.txt` | 14 paquetes **sin versiones fijas** | Riesgo de reproducibilidad a futuro |

### 3.1 Mapa de dependencias

```text
data/esru_emovi.zip ─► src/data/emovi.py ─► src/features/indices.py ─► data/processed/emovi_movilidad.parquet
                          (01, 02)                 (02)                         │
Releases CONEVAL/ENOE ─► src/data/context.py ─► contexto_estatal_2022.csv       │
                          (01)                         │                        │
                                                       ▼                        ▼
                                                   03_eda ◄─────────────────────┤
                                                                                ├─► 04_baselines ─┐
                       src/models/train.py, diagnostics.py ─────────────────────┤                 │
                                                                                ├─► 05_modeling ◄─┘
                       src/evaluation/interpret.py, extra.py ───────────────────┼─► 06_interpretability
                                                                                ├─► 07_scenarios
                                                                                └─► 08_final_validation
```

El notebook 02 debe correr antes que 03–08. Del 04 al 08 cada notebook reentrena su modelo, en lugar de cargar uno guardado.

---

## 4. Reconstrucción del flujo de trabajo

### 4.1 Resumen por notebook

| NB | Objetivo | Entradas | Salidas | Métodos |
|---|---|---|---|---|
| 00 | Constitución, preguntas, hipótesis (Fases 0–2) | — | — | Solo texto |
| 01 | Auditoría de datos y puerta 🟢 | EMOVI cruda, CONEVAL, ENOE | `auditoria_faltantes.csv`, `contexto_estatal_2022.csv` | Faltantes, validación contra CONEVAL |
| 02 | Índices y target | EMOVI cruda | parquet, cargas, `validacion_indices.csv` | PCA, quintiles ponderados por cohorte |
| 03 | EDA | parquet, contexto | 9 figuras, 9 tablas | Tasas ponderadas, Simpson, faltantes por grupo |
| 04 | Baselines y métricas | parquet | `metricas_completas.csv`, calibración, class weight | Dummy ×2, logística, árbol, RF, GB |
| 05 | Comparación | parquet | comparación, mediación, semillas, curva de aprendizaje, matriz de decisión | CV de 5 particiones, 10 semillas |
| 06 | Interpretación | parquet | razones de momios, permutación, SHAP, H003, H005, errores, K-Means | GLM ponderado con errores por UPM |
| 07 | Escenarios | parquet | `escenarios*.csv` | Contrafactuales + bootstrap |
| 08 | Robustez y red team | parquet | `robustez.csv`, `desempeno_subgrupos.csv` | Bootstrap simple, subgrupos en la partición de prueba |

### 4.2 Inconsistencias entre código, salidas y documentación

| ID | Inconsistencia | Dónde |
|---|---|---|
| I-1 | El texto dice "45 bienes y servicios a los 14 años **más** piso, autos y cuartos". El código usa **42** ítems + 3 = 45 en total | NB 02, celda de texto |
| I-2 | El texto del NB 07 (primera parte) habla de "Tono de piel claro: +1.5 pts" con el modelo principal, mientras el NB 06 dice "no significativo". Es consistente, pero el escenario no debería mostrarse sin IC | NB 07 |
| I-3 | "Brecha por tono ≈ 11 pts" aparece como hallazgo validado en 7 lugares, pero se calculó con una partición de n = 114 | README, NB 05, 06, 08, bitácora D18, experimentos E003/E005, roadmap R009 |
| I-4 | IC 95% "48–55%" (README) vs. "47.6–54.5" (NB 08, bootstrap simple). Ninguno respeta el diseño | README, NB 08 |

### 4.3 Reproducción completa

Los 9 notebooks se ejecutaron desde cero en una copia aislada, sin errores. **Las 29 tablas CSV regeneradas son idénticas a las originales** (diferencia numérica máxima = 0). Los resultados guardados corresponden al código actual: no hay salidas viejas. Detalle en el Anexo A.

---

## 5. Auditoría conceptual

| Tema | Evaluación | Estado |
|---|---|---|
| Definición de movilidad | **Intergeneracional relativa**: el rango del hogar actual frente al rango del hogar a los 14 años, dentro de la propia cohorte | ✅ Correcta y declarada |
| Intergeneracional vs. intrageneracional | La EMOVI tiene información del primer empleo (p77–p87), pero no se usó. El proyecto **no** mide movilidad intrageneracional | ✅ Declarar explícitamente en el cartel |
| Pobreza vs. riqueza | El target mide **posición en la distribución de bienes**, no pobreza oficial (CONEVAL). "Seguir en el 20% más pobre" ≠ "seguir en pobreza" | ⚠️ **Riesgo de lenguaje.** El título dice "pobreza"; el cartel debe aclarar que se usa "20% más pobre en bienes del hogar" |
| Absoluta vs. relativa | Solo relativa. Alguien puede tener más bienes que sus padres y seguir en Q1 | ⚠️ Declararlo |
| Origen y destino | Origen = 42 bienes y servicios + piso, autos y cuartos a los 14 años (retrospectivo). Destino = 44 bienes y servicios + piso y autos. Ítems distintos, pero se comparan rangos, no niveles | ✅ |
| Unidad de observación | Persona de 25–64 años; el hogar se usa para medir la riqueza | ✅ |
| Población representada | 60.0 millones (suma de factores) | ✅ |
| Cohortes | Los quintiles por cohorte evitan comparar a jóvenes con mayores | ✅ |

---

## 6. Auditoría de datos

| Revisión | Resultado | Evidencia | Estado |
|---|---|---|---|
| Duplicados | 0 folios duplicados | NB 01 | ✅ |
| Validación externa | CONEVAL: 36.3% de pobreza y 7.1% extrema, igual a las cifras oficiales | NB 01 | ✅ |
| Empates en los índices | 15,739 valores únicos de 17,843. En el corte de Q1 solo hay **1 empate** (cohorte 55–64, 2 filas en Q1/Q2) | `checks1` | ✅ Sin efecto |
| Q1 ponderado | 19.9% de la población en Q1 de origen y 19.9% en Q1 de destino | `checks1` | ✅ |
| Concentración de pesos | Factor máximo = 81 veces la mediana; el 1% de las filas concentra el **11.6%** del peso | `checks1` | ⚠️ |
| **Tamaño efectivo (Kish)** | Total: 5,071 de 17,843. **Q1: 815 de 2,674.** Norte: 44, Norte-occidente: 67, Centro-norte: 79 | `checks1` | ⚠️ **Las tasas ponderadas por subgrupo son mucho más inciertas de lo que sugiere la n** |
| Faltantes | Escolaridad del padre 19% y de la madre 10%, no aleatorios (60% vs 48% sigue en Q1). Se tratan como categoría | NB 03 | ✅ |
| "No sabe" en bienes | < 5% por ítem; imputado con la media solo para el índice | NB 02 | ✅ |
| Escala de tono de piel | Dirección verificada con colorímetro: oscuro 47.1, medio 49.8, claro 53.9 (L*) | `checks1` | ✅ |
| Ingreso | `ingc_pc` está **imputado** por el CEEY (dice el diccionario). Solo se usa en la robustez | Diccionario | ⚠️ Declarar |
| Variables medidas hoy usadas como "dadas" | `autoadscripcion` (cómo se identifica hoy), `tono_piel` (autopercibido hoy) y `lengua_indigena` (habla hoy) | Código | ⚠️ Ver H-08 |
| Retrospectividad | El origen depende de la memoria. Validación débil: r = 0.50 con la escalera subjetiva | NB 02 | ⚠️ Limitación estructural |
| Compatibilidad de fuentes | Sin llaves comunes; solo integración por estado | NB 01 | ✅ Bien tratado; pero ver H-04 |
| Representatividad estatal | La EMOVI se diseña para el nivel nacional y regional. ESS mediana por estado: **31** | `checks3` | ❌ Ver H-04 |

---

## 7. Matriz: ¿para qué NO sirven nuestros datos?

| Pregunta | Clasificación | Razón | Riesgo de responder mal | Información necesaria |
|---|---|---|---|---|
| Persistencia en el 20% más pobre (Q1 → Q1) | **RESPONDIBLE DIRECTAMENTE** | Origen y destino para la misma persona, con pesos | Confundir "20% más pobre en bienes" con "pobreza oficial" | — |
| Movilidad intergeneracional relativa (matriz de transición) | **RESPONDIBLE DIRECTAMENTE** | Ídem | Leerla como absoluta | — |
| Movilidad intergeneracional absoluta (¿vive mejor que sus padres?) | **RESPONDIBLE CON RESTRICCIONES** | Los ítems de origen y destino son distintos; habría que construir un índice común | Afirmar mejoras de nivel con quintiles | Índice con ítems comunes, mismas cargas |
| Movilidad intrageneracional | **NO RESPONDIBLE (no se intentó)** | Solo hay primer empleo y empleo actual; no hay trayectoria de riqueza | — | Panel o historia laboral |
| Efecto causal de la educación | **NO RESPONDIBLE** | Diseño transversal; educación medida junto con el destino; variables omitidas | Recomendar políticas educativas como si fueran efectos | Experimento natural, variables instrumentales, panel |
| Impacto de políticas públicas | **NO RESPONDIBLE** | No hay variables de exposición a programas | Atribuir cambios a programas | Registros administrativos |
| Desigualdad territorial por región (5 regiones) | **RESPONDIBLE CON RESTRICCIONES** | La EMOVI es representativa por región; región de origen retrospectiva | Atribuir la brecha a la "cultura" regional | — |
| Desigualdad por estado | **SOLO EXPLORATORIA** | No es representativa por estado; ESS ≈ 31 | Ranking de estados y falacia ecológica | Muestra estatal o estimación de áreas pequeñas |
| Diferencias por lengua indígena | **RESPONDIBLE CON RESTRICCIONES** | ESS = 192 entre quienes hablan lengua; la lengua se mide hoy | Causalidad; "perder la lengua" puede ser consecuencia de migrar o subir | Lengua de los padres / en la infancia |
| Diferencias por tono de piel | **SOLO EXPLORATORIA** | Brecha no significativa (IC traslapados); tono autopercibido hoy | Afirmar discriminación o su ausencia | Colorímetro (sí existe: `p113dL`), más muestra |
| Interacción tono × región | **SOLO EXPLORATORIA** | Celdas de 24–50 personas | Efecto Simpson falso | Más muestra |
| Cambio de la movilidad en el tiempo | **NO RESPONDIBLE con una sola encuesta** | Las cohortes no son seguimientos; efecto de ciclo de vida | "La movilidad empeoró" | EMOVI 2011/2017 con la misma metodología |
| Predicción individual de quién sale | **RESPONDIBLE CON RESTRICCIONES** | AUC ≈ 0.70 | Usarla para focalizar personas | — |
| Papel del empleo formal | **SOLO EXPLORATORIA** | Empleo actual = parte del destino (causalidad inversa) | Leerlo como palanca causal | Empleo en una fecha anterior al destino |

---

## 8. Auditoría estadística

### 8.1 Modelo explicativo (`interpret.logit_explicativo`)

| Aspecto | Evaluación |
|---|---|
| Especificación | GLM binomial con `var_weights` (pesos normalizados) y errores agrupados por UPM |
| Errores estándar | statsmodels advierte "cov_type not fully supported with var_weights". **Se verificó con un sandwich manual de pseudo-verosimilitud: los errores coinciden exactamente (razón 1.000)** ✅ |
| Estratos | No se usan (`est`). Con conglomerados suele ser ligeramente conservador. Riesgo BAJO |
| Sensibilidad a los pesos | Sin pesos, las conclusiones principales se mantienen: Sur (1.63, p < 0.001), Norte (0.56), lengua (1.77), cohortes e índice de origen ✅. **Cambian la localidad y el tono:** tono claro pasa de 1.03 (ponderado) a 0.80 (sin pesos, p = 0.07) |
| Categoría de referencia | **Metrópoli tiene solo 82 casos en Q1** y el VIF de "Pueblo" es 7.9. Las razones de momios de localidad son inestables (ponderadas < 1, sin pesos ≈ 1–1.5) ❌ |
| Separación | Se resolvió agrupando la escolaridad de los padres (D16). Decisión tomada después de ver resultados, pero justificada por n = 2 |
| Interacciones | Se probaron (H003, H005) con pruebas de Wald conjuntas ✅ |
| Magnitud vs. significancia | Bien reportadas con IC |

### 8.2 Inferencia descriptiva

| Cifra | Reportado | Verificado (bootstrap por UPM, 1,000 réplicas) | Estado |
|---|---|---|---|
| Sigue en Q1 | 51% (IC 48–55) | 51.1% (**46.3–55.4**) | ⚠️ Corregir el IC |
| Q5 → Q5 | 55% | 54.9% (51.8–58.2) | ✅ |
| Sur | 64% | 64.1% (59.0–68.6) | ✅ |
| Norte | 23% | 22.8% (**12.2–37.4**) | ✅ Diferencia clara con el Sur, pero el IC es amplio |
| Lengua indígena: sí / no | 69% / 47% | 68.9 (60.3–76.9) / 46.8 (42.0–51.6) | ✅ |
| Escolaridad primaria / profesional | 56% / 18% | 56.2 (48.8–62.4) / 18.2 (8.0–29.8) | ✅ (n = 85 en profesional) |
| 0 / 3 desventajas | 30% / 82% | 30.1 (22.1–37.6) / 82.0 (73.8–87.9) | ✅ |
| Tono oscuro / claro | 56% / 49% | 55.7 (46.9–62.8) / 49.4 (40.7–57.5) | ⚠️ **IC traslapados: no hay brecha nacional demostrada** |
| Norte: oscuro / claro | 33% / 15% | 32.9 (17.3–53.2) / 14.7 (1.9–34.2), n = 50 / 24 | ❌ No significativo |
| Norte-occidente: oscuro / claro | 54% / 19% | 53.7 (17.3–71.8) / 18.6 (5.5–37.4), n = 48 / 45 | ❌ No significativo |

---

## 9. Auditoría de Machine Learning

| Aspecto | Evaluación | Estado |
|---|---|---|
| Partición | 80/20 estratificada + CV de 5 particiones; semilla 42 | ✅ |
| Leakage | No se usan variables de destino; la imputación y el escalamiento van dentro del pipeline | ✅ |
| Leakage "suave" | `autoadscripcion` y `tono_piel` se miden hoy. Sin ellas (y con colorímetro) el AUC queda en 0.701 vs. 0.699: **sin efecto en el desempeño**, pero la autoadscripción ocupa el 4.º lugar en importancia y no debería interpretarse como circunstancia de origen | ⚠️ H-08 |
| Ponderadores | Entrenamiento sin pesos (D14), declarado | ✅ |
| Baselines | Mayoritaria, estratificada y logística con un predictor | ✅ |
| Métricas | AUC, PR-AUC, log loss, Brier, F1, matriz de confusión, calibración | ✅ |
| Estabilidad | 10 semillas: logística 0.701 ± 0.002, RF 0.697 ± 0.003, GB 0.689 ± 0.004 | ✅ |
| Selección | Logística, por una regla congelada antes de ver resultados | ✅ |
| Curva de aprendizaje | Se satura cerca de 0.70; el límite es la información disponible | ✅ |
| Stress test del target | Mismo AUC por ingreso, pero **solo 71% de acuerdo individual** entre definiciones | ⚠️ La tasa es robusta; la clasificación individual no tanto |
| **Desempeño por subgrupo** | Se calculó solo en la partición de prueba (n = 535; tono oscuro n = 114). **Fuera de muestra con las 2,674 personas, la calibración por tono es perfecta:** oscuro 54.5 real vs. 54.5 predicho (brecha 0.0, IC −4.2 a +3.6) | ❌ **H-01** |
| Explicación de la brecha falsa | En la partición de prueba, la tasa real del tono oscuro fue 61.4%; en entrenamiento, 52.8%. Variación muestral de una partición pequeña. La regresión logística con dummies de tono está calibrada por construcción en el promedio de cada categoría | — |
| Matriz de decisión | La columna "Brecha de calibración por tono" hereda el error H-01 (los 4 modelos "≈11 pts" por la misma partición) | ❌ |
| Escenarios | Predicciones en la misma muestra, **sin pesos** (51.8% vs. 51.1% ponderado); IC por bootstrap simple (no por conglomerados). "+1 nivel" no cambia a los 85 profesionistas; "empleo formal" no cambia a los 960 no ocupados | ⚠️ Declararlo |
| K-Means | k = 4 elegido sin criterio (sin silueta ni codo) | ⚠️ BAJO |
| Pruebas automáticas | No existen | ⚠️ BAJO |

---

## 10. Auditoría de interpretabilidad

| Variable | ¿Asociación? | ¿Importancia predictiva? | ¿Estable entre modelos? | ¿Estable entre subgrupos y pesos? | ¿Proxy? | ¿Causalidad inversa? | Afirmación permitida | Afirmación incorrecta |
|---|---|---|---|---|---|---|---|---|
| Región de origen (Sur) | ✅ RM 1.9 (1.3–2.7) | ✅ n.º 1 (permutación y SHAP) | ✅ | ✅ con y sin pesos | Sí: mercados laborales, servicios, pobreza estructural | No (es de origen) | "Crecer en el Sur se asocia con mayor persistencia" | "Vivir en el Sur causa pobreza" |
| Cohorte | ✅ RM 0.18–0.46 | ✅ n.º 2 | ✅ | ✅ | Ciclo de vida, cambios del mercado | No | "Las cohortes jóvenes muestran mayor persistencia relativa en esta encuesta" | "La movilidad empeoró". **El artefacto de bienes modernos se refutó:** 59.4% vs. 59.6% sin esos bienes; queda abierto el ciclo de vida |
| Índice de origen (dentro de Q1) | ✅ RM 0.65 | ✅ n.º 3 | ✅ | ✅ | — | No | "Aun dentro del 20% más pobre, tener algo más se asocia con salir" | — |
| Lengua indígena | ✅ RM 1.9 (1.2–2.9) | ✅ moderada | ✅ | ✅ (1.77 sin pesos) | Discriminación, territorio, servicios | **Posible:** se mide si la habla *hoy* | "Hablar lengua indígena se asocia con casi el doble de momios de seguir en Q1, aun con la misma región" | "Por ser indígena…" |
| Autoadscripción | — (no está en el logit) | ✅ n.º 4 | ? | — | Identidad actual, correlacionada con el destino (21% indígena en Q1 de destino vs. 3.6% en Q5) | **Sí** | Ninguna como circunstancia de origen | Interpretarla como factor de origen |
| Tono de piel | ❌ no significativo (RM 1.31, p = 0.14); cambia sin pesos | Baja | — | ❌ | Región, lengua | Posible (autopercepción) | "No encontramos una brecha significativa por tono de piel con estos datos" | "No hay discriminación por tono" / "El modelo discrimina por tono" |
| Escolaridad de la madre | ❌ | Baja | ✅ | — | — | — | "No hay variación suficiente dentro de Q1 para evaluarla" | "La educación de la madre no importa" |
| Padre ausente / sin dato | ✅ RM 1.57 (p = 0.03) | Baja-moderada | — | ✅ | Hogar monoparental | No | "No tener el dato del padre se asocia con mayor persistencia" | — |
| Localidad de origen | ❌ inestable | Moderada | — | ❌ cambia de signo sin pesos | Región | No | Solo descriptiva (pueblo 55% vs. ciudades 40–46%) | Razones de momios de localidad |
| Escolaridad propia (mediación) | ✅ 56% → 18% | ↑ AUC 0.70 → 0.74 | — | ⚠️ H003 sin evidencia de variación regional | Recursos no observados | **Sí** (se mide junto con el destino) | "Es la característica más asociada con haber salido" | "La educación es la salida" (causal) |
| Empleo formal | ✅ 25% vs. 53% | En los escenarios | — | — | Destino | **Sí** | Descriptivo | Palanca causal |

**Convergencia:** el modelo interpretable (logit, permutación) y el complejo (SHAP en gradient boosting) coinciden en las 3 variables principales. No hay contradicciones entre modelos, solo entre ponderado y sin pesos para la localidad y el tono.

---

## 11. Sesgos y robustez

| Riesgo | Evaluación |
|---|---|
| Sesgo de recuerdo | Estructural; mitigado con bienes en lugar de ingreso |
| Sesgo de supervivencia | Estructural; quienes murieron o emigraron no están |
| Representatividad de subgrupos | ESS bajo (ver sección 6); las cifras necesitan IC |
| Sesgo del modelo por subgrupo | **Retirado** (H-01): no hay sesgo de calibración por tono fuera de muestra |
| Robustez del target | La tasa es estable (47–51%) con 3 definiciones; el acuerdo individual es de 71% |
| Robustez a los pesos | Hallazgos principales estables; localidad y tono no |
| Falacia ecológica | El análisis estatal es frágil (ESS ≈ 31) |

---

## 12. Hallazgos priorizados

| ID | Hallazgo | Evidencia | Archivo | Severidad | Tipo | ¿Corregible? | Acción |
|---|---|---|---|---|---|---|---|
| **H-01** | La "brecha de calibración de ≈11 pts por tono oscuro" es un artefacto de una partición de prueba con n = 114. Fuera de muestra (n = 2,674), la brecha es 0.0 (IC −4.2 a +3.6) | `checks2.py` | README L35; NB 05, 06, 08; bitácora D18; E003/E005; roadmap R009; auditoría previa P4 | **CRÍTICO** (invalida un hallazgo titular) | ERROR ESTADÍSTICO + INTERPRETACIÓN | Sí | **RETIRAR** el hallazgo y reemplazar el desempeño por subgrupo con predicciones fuera de muestra e IC |
| **H-02** | El IC 95% de la persistencia ignora el diseño muestral | `checks1.py`: 46.3–55.4 vs. 48–55 reportado | README L28; NB 08 | ALTO | ERROR ESTADÍSTICO | Sí | **CORREGIR** con bootstrap por UPM |
| **H-03** | Las cifras por subgrupo se presentan sin IC; ESS de Q1 = 815, del Norte = 44 | `checks1.py`, `checks2.py` | NB 03; figuras 02–04, 13; README | ALTO | ERROR ESTADÍSTICO | Sí | **REANALIZAR**: agregar IC por conglomerados a las tablas y figuras de subgrupos |
| **H-04** | Correlación estatal r = 0.56 con ESS mediana de 31 por estado; la EMOVI no es representativa por estado; anacronismo 2022 vs. infancia | `checks3.py` | NB 03, fig. 09, README L33 | ALTO | LIMITACIÓN DE DATOS + INTERPRETACIÓN | No (estructural) | **CONSERVAR CON RESTRICCIONES** como exploratorio y **retirar del cartel** (o mostrarla con la advertencia de ESS) |
| **H-05** | El "efecto Simpson" tono × región no es significativo (celdas de 24–50 personas, IC traslapados) | `checks2.py` | NB 03, 06 (errores), README L37 | ALTO | INTERPRETACIÓN | Sí | **REFORMULAR** como exploratorio; quitar "El promedio engaña" del README |
| H-06 | Las RM de localidad son inestables (referencia Metrópoli n = 82; VIF 7.9; cambian de signo sin pesos) | `checks3.py` | NB 06, `razones_momios.csv` | MEDIO | ERROR ESTADÍSTICO | Sí | **REANALIZAR** con referencia "Ciudad" (agrupando metrópoli y ciudades) y reportar la sensibilidad a los pesos |
| H-07 | "Seguir en el 20% más pobre" se presenta como "pobreza", pero es posición relativa en bienes | Título, README | Global | MEDIO | INTERPRETACIÓN | Sí | **REFORMULAR** el lenguaje (ver la sección 14) |
| H-08 | `autoadscripcion` y `tono_piel` (autopercibido) se miden hoy y se tratan como dadas; la autoadscripción ocupa el 4.º lugar en importancia | `checks2.py` | `train.py` CAT | MEDIO | RIESGO DE SESGO | Sí | **DECISIÓN DEL EQUIPO:** quitar la autoadscripción y usar el colorímetro (`p113dL`); el AUC no cambia (0.701) |
| H-09 | Lengua indígena medida hoy (posible causalidad inversa por migración o asimilación) | Diccionario p111 | — | MEDIO | LIMITACIÓN DE DATOS | No | **CONSERVAR CON RESTRICCIONES** y declararlo |
| H-10 | Escenarios sin pesos, con IC no agrupado; "+1 nivel" no afecta a 85 profesionistas; "empleo formal" no afecta a 960 no ocupados | Código `extra.py` | NB 07 | MEDIO | LIMITACIÓN DEL MODELO | Sí | **CONSERVAR CON RESTRICCIONES**; documentar y ponderar los promedios |
| H-11 | Ningún hito tiene aprobación humana (todas las fases en PROPUESTA) | roadmap 6.1 | roadmap | MEDIO | DOCUMENTACIÓN / PROCESO | Sí | Aprobación del equipo (sección 19) |
| H-12 | La rúbrica oficial no está en el repositorio; la auditoría previa se hizo contra el resumen del roadmap | `docs/rubric/` vacío | — | MEDIO | ASPECTO NO VERIFICABLE | Sí | **AMPLIAR EVIDENCIA**: subir ambas rúbricas |
| H-13 | Referencias sin verificar; la comparación con el CEEY no tiene cifra | `referencias.md` | — | MEDIO | NO VERIFICABLE | Sí | **AMPLIAR EVIDENCIA** |
| H-14 | `requirements.txt` sin versiones; los datos de los Releases se descargan a mano | — | — | BAJO | OPORTUNIDAD DE MEJORA | Sí | Fijar versiones; script de descarga |
| H-15 | Texto "45 bienes … más piso, autos y cuartos" (son 42 + 3) | NB 02 | — | BAJO | DOCUMENTACIÓN | Sí | **CORREGIR** |
| H-16 | K-Means k = 4 sin criterio de selección | NB 06 | — | BAJO | OPORTUNIDAD DE MEJORA | Sí | Silueta para k = 2..6 |
| H-17 | `tests/` vacío | — | — | BAJO | OPORTUNIDAD DE MEJORA | Sí | Pruebas mínimas (rangos, quintiles al 20%) |
| H-18 | Acuerdo individual del 71% entre target por bienes y por ingreso | NB 05 | — | BAJO | RESULTADO CONTRADICTORIO | — | **CONSERVAR COMO HALLAZGO**: la tasa es robusta; la clasificación individual, menos |
| H-19 | Hipótesis "efecto cohorte = artefacto de bienes modernos" **refutada** | `checks2.py` | NB 08 red team #4 | — | RESULTADO CONTRADICTORIO | — | **CONSERVAR COMO HALLAZGO NEGATIVO**: actualizar el texto (queda abierto el ciclo de vida) |
| H-20 | Tono de piel: sin brecha significativa | NB 06, `checks2` | — | — | RESULTADO CONTRADICTORIO | — | **CONSERVAR COMO HALLAZGO NEGATIVO** (H4 del equipo) |

---

## 13. Tratamiento recomendado de los resultados existentes

| Hallazgo | Resultado original | Evaluación | Decisión | Acción requerida | Validación |
|---|---|---|---|---|---|
| H-01 | "El modelo subestima ≈11 pts al tono oscuro" | Falso (variación de la partición) | **D. RETIRAR** | Reemplazar `subgroup_performance` con predicciones fuera de muestra (CV) + IC bootstrap; actualizar los 7 documentos; registrar en la bitácora por qué se retira | Brecha por tono con IC que incluya 0 |
| H-02 | IC 48–55% | Demasiado estrecho | **A. CORREGIR** | Bootstrap por UPM en el NB 08 | IC ≈ 46–55 |
| H-03 | Tasas por subgrupo | Sin incertidumbre | **B. REANALIZAR** | Función `cboot` en `extra.py`; barras de error en las figuras 02–04 y 13 | Cada cifra del cartel con su IC |
| H-04 | r = 0.56 por estado | Frágil | **C. CONSERVAR CON RESTRICCIONES** | Etiquetar como exploratorio; agregar ESS a la figura 09; fuera del cartel | — |
| H-05 | "La brecha por tono solo existe fuera del Sur" | No significativo | **E. REFORMULAR** | "Exploratorio: las diferencias por tono parecen variar por región, pero la muestra no permite confirmarlo" | IC en la tabla `tono_por_region` |
| H-06 | RM de localidad | Inestables | **B. REANALIZAR** | Cambiar la referencia; tabla con y sin pesos | RM estables en signo |
| H-07 | "Pobreza pegajosa" | Ambiguo | **E. REFORMULAR** | Definir "20% más pobre en bienes del hogar" en todos los textos | — |
| H-08 | Autoadscripción y tono autopercibido como predictores | Riesgo de medición actual | **Decisión del equipo** (recomendado: B) | Variante sin autoadscripción y con colorímetro; comparar | AUC similar; ranking sin autoadscripción |
| H-10 | Escenarios | Válidos como asociación | **C. CONSERVAR CON RESTRICCIONES** | Ponderar los promedios; IC por UPM; declarar a quién no afecta cada escenario | — |
| H-18 | Stress test | — | **G. HALLAZGO NEGATIVO** | Reportar el 71% | — |
| H-19 | Red team #4 | Hipótesis refutada | **G. HALLAZGO NEGATIVO** | Actualizar el texto del NB 08 | — |
| Persistencia 51% | 51.1% | ✅ | **Conservar** | Solo cambiar el IC | — |
| Sur vs. Norte, lengua, desventajas acumuladas, cohortes, índice de origen | ✅ robustos | ✅ | **Conservar** | Agregar IC | — |
| Selección de la regresión logística | ✅ | ✅ | **Conservar** | Quitar la columna de brecha por tono de la matriz de decisión | — |

### 13.1 Efecto sobre las conclusiones

| Conclusión actual | Afectada por | ¿Sigue válida? |
|---|---|---|
| "1 de cada 2 sigue en el 20% más pobre" | H-02, H-07 | ✅ Sí, con IC 46–55 y la definición precisa |
| "La región pesa más que todo" | H-03 | ✅ Sí (IC del Sur 59–69 vs. Norte 12–37) |
| "Lengua indígena: casi el doble de momios" | H-09 | ✅ Con la restricción de que se mide hoy |
| "La educación propia es la salida" | Ya marcada como la más atacable | ⚠️ Reformular: "la característica más asociada con haber salido" |
| "Los estados más pobres tienen pobreza más pegajosa" | H-04 | ⚠️ Solo exploratoria |
| "El modelo subestima al tono oscuro" | H-01 | ❌ **Retirar** |
| "El promedio engaña: brecha por tono solo fuera del Sur" | H-05 | ❌ Retirar como hallazgo; dejar como pregunta abierta |
| "Las desventajas se acumulan (30% → 82%)" | H-03 | ✅ IC 22–38 vs. 74–88 |

---

## 14. Matriz de conclusiones defendibles

| Nivel | Afirmación exacta | Evidencia | Método | Lenguaje recomendado | Lenguaje a evitar |
|---|---|---|---|---|---|
| **A** | Cerca de la mitad (51%; IC 95% 46–55%) de quienes crecieron en el 20% de hogares con menos bienes sigue en ese 20% de adulta | Matriz de transición; robustez con 3 definiciones | Quintiles ponderados por cohorte; bootstrap por UPM | "Persistencia en la base de la distribución" | "La mitad de los pobres nunca sale de la pobreza" |
| **A** | La persistencia es simétrica en los extremos: 55% de quienes crecen en el 20% más rico sigue ahí; solo 2% pasa del 20% más pobre al más rico | Matriz de transición | Ídem | "Los extremos son los más pegajosos" | — |
| **A** | Quienes crecieron en el Sur tienen mayor persistencia (64% vs. 23% en el Norte), aun con el mismo origen, cohorte, lengua y sexo (RM 1.9) | EDA + logit (con y sin pesos) + permutación + SHAP | Varios | "Se asocia con" | "Causa" |
| **B** | Hablar lengua indígena se asocia con casi el doble de momios de seguir en Q1, aun con la misma región | Logit (1.9; 1.77 sin pesos) | GLM ponderado | "…se asocia con…, medida como lengua que se habla hoy" | "Por ser indígena" |
| **B** | Las desventajas de origen se acumulan: de 30% sin ninguna a 82% con Sur + pueblo + lengua indígena, de forma aditiva | EDA + Wald (p = 0.20 sin sinergia) | Tasas con IC + logit | "Se suman" | "Se multiplican" |
| **B** | Las circunstancias observadas de origen predicen solo de forma moderada quién sale (AUC ≈ 0.70); más datos no lo mejoran | 6 modelos, 10 semillas, curva de aprendizaje | CV | "Buena parte del destino no la explican las circunstancias observadas" | "El resto es mérito individual" |
| **B** | La escolaridad propia es la característica más asociada con haber salido (56% → 18%) | EDA + modelo de mediación | Descriptivo | "Mediadora", "asociada" | "La educación es la solución" |
| **B** | Superar la escolaridad de los padres no garantiza salir: el 43% de quienes lo lograron sigue en Q1 | H004 | Descriptivo | — | — |
| **C** | Las cohortes jóvenes muestran mayor persistencia relativa | Logit; no es artefacto de bienes modernos | — | "En esta encuesta…" | "La movilidad empeoró" |
| **C** | Los estados con más pobreza en 2022 tienden a tener mayor persistencia | r = 0.56, ESS ≈ 31 | Ecológico | "Exploratorio" | Rankings de estados |
| **C** | Las diferencias por tono de piel podrían variar por región | Celdas pequeñas | — | "Pregunta abierta" | "El promedio oculta…" |
| **C** | Bajo los escenarios hipotéticos, educación + empleo formal se asocian con −17 pts | Modelo de mediación | Contrafactual | "Bajo el escenario hipotético… y manteniendo las relaciones estimadas" | "Una política educativa reduciría…" |
| **D** | El modelo subestima la persistencia del tono oscuro | Retirado (H-01) | — | — | — |
| **D** | Hay (o no hay) discriminación por tono de piel | Sin significancia; tono autopercibido | — | "No encontramos brecha significativa" | Ambas afirmaciones |
| **D** | Cualquier afirmación causal o de impacto de políticas | Diseño transversal | — | — | — |
| **Negativo** | La escolaridad de la madre no se asocia con salir **dentro** de Q1 | Sin variación (31 madres con prepa o más) | — | "No evaluable dentro de Q1" | "No importa" |
| **Negativo** | El efecto de la educación no varía significativamente por región (H003) | Wald p = 0.26 | — | "Sin evidencia" | — |

---

## 15. Plan de correcciones

Ordenado por dependencias.

| ID | Hallazgo | Prioridad | Acción | Archivos | Dependencias | Método | Validación | Riesgo residual | Estado |
|---|---|---|---|---|---|---|---|---|---|
| C-01 | H-01 | **P0** | Desempeño por subgrupo con predicciones fuera de muestra + IC | `src/models/train.py` (`subgroup_performance`), `diagnostics.py` (`tone_gap`) | — | `cross_val_predict` sobre las 2,674 personas + bootstrap | Brecha por tono con IC que incluye 0 | — | Pendiente |
| C-02 | H-01 | **P0** | Retirar la afirmación en los documentos y registrar la retirada | README, NB 05/06/08 (texto), bitácora (nueva D25, sin borrar D18), `registro_experimentos.md` (nueva fila E014), roadmap R009 → Cerrado, `auditoria_final.md` | C-01 | Edición | `grep "11 p"` sin resultados vigentes | — | Pendiente |
| C-03 | H-02, H-03 | **P0** | Función de bootstrap por UPM y su uso en la cifra titular y en los subgrupos | `src/evaluation/extra.py`, NB 03 y 08 | — | Remuestreo de UPM | IC ≈ 46–55 | — | Pendiente |
| C-04 | H-03 | P1 | Barras de error en las figuras de subgrupos | `src/visualization/plots.py` | C-03 | — | Figuras con IC | — | Pendiente |
| C-05 | H-05 | P1 | Reformular la tabla tono × región con IC; quitar del README | NB 03, 06; README | C-03 | — | — | — | Pendiente |
| C-06 | H-04 | P1 | Etiquetar el análisis estatal como exploratorio y mostrar el ESS en la figura 09 | NB 03, `plots.py`, README | — | — | — | Falacia ecológica (estructural) | Pendiente |
| C-07 | H-06 | P1 | Logit con referencia "Ciudad" y tabla de sensibilidad con y sin pesos | `interpret.py`, NB 06 | — | — | Signos estables | — | Pendiente |
| C-08 | H-08 | P1 | **(Requiere aprobación)** Variante sin autoadscripción y con colorímetro | `train.py`, NB 05, 06 | Aprobación | — | AUC ≈ 0.70 | — | Requiere aprobación |
| C-09 | H-07 | P1 | Lenguaje: "20% más pobre en bienes del hogar" | README, NB 00, docs | — | — | — | — | Pendiente |
| C-10 | H-10 | P2 | Ponderar los promedios de los escenarios; IC por UPM; declarar a quién no afectan | `extra.py`, NB 07 | C-03 | — | — | Causalidad inversa (estructural) | Pendiente |
| C-11 | H-19 | P2 | Actualizar el red team #4 con la prueba de bienes modernos | NB 08 | — | — | — | Ciclo de vida | Pendiente |
| C-12 | H-12, H-13 | P2 | Subir las rúbricas; verificar las referencias y la cifra del CEEY | `docs/rubric/`, `referencias.md` | **El equipo** | — | — | — | Requiere al equipo |
| C-13 | H-15 | P3 | Corregir "45 bienes" | NB 02 | — | — | — | — | Pendiente |
| C-14 | H-14, H-17 | P3 | Fijar versiones; pruebas mínimas | `requirements.txt`, `tests/` | — | — | `pytest` pasa | — | Pendiente |
| C-15 | H-16 | P3 | Silueta para k | NB 06 | — | — | — | — | Opcional |
| C-16 | H-11 | P0 (proceso) | Registrar la aprobación de las fases | roadmap 6.1 | Equipo | — | — | — | Requiere al equipo |

**Indispensables:** C-01, C-02, C-03, C-09, C-16. **Recomendadas:** C-04 a C-07, C-10, C-11. **Opcionales:** C-13 a C-15. **No corregibles (estructurales):** recuerdo retrospectivo, supervivencia, diseño transversal, ausencia de representatividad estatal y lengua medida hoy. **Requieren aprobación:** C-08, C-12, C-16 y el cambio de lenguaje del título (C-09).

---

## 16. Procedimiento de implementación

1. El equipo aprueba o modifica las decisiones de la sección 19.
2. Se congela la versión original: etiqueta `auditoria-v1` sobre `10533d7`, con las tablas originales preservadas.
3. Se trabaja en una **rama nueva** `correcciones-auditoria`, nunca directamente en `main`.
4. Cada corrección se hace en un commit separado que cita su ID (C-01…), y se recalculan solo los notebooks afectados.
5. Validación posterior: se reproducen los notebooks 01–08 desde cero, se comparan contra las tablas originales y se repite el `grep` de afirmaciones retiradas.
6. Se actualizan la bitácora (nuevas filas, sin borrar), el registro de hipótesis, el registro de experimentos y el README.
7. Se hace la fusión a `main` con aprobación del equipo y **solo entonces** se redacta el Proyecto Integrador y el cartel.

---

## 17. Matriz de trazabilidad antes y después (plantilla)

| Elemento | Estado original | Hallazgo | Cambio aprobado | Estado posterior | Diferencia | Efecto en conclusiones |
|---|---|---|---|---|---|---|
| IC de la persistencia | 48–55 (README) / 47.6–54.5 (NB 08) | H-02 | C-03 | *Esperado: 46.3–55.4* | Más amplio | Ninguno en la conclusión central |
| Brecha por tono oscuro | +11.2 pts (prueba, n = 114) | H-01 | C-01 | *Esperado: ≈0 (IC −4 a +4)* | Desaparece | Se retira un hallazgo titular |
| Matriz de decisión (columna tono) | 10.5–11.5 pts para los 4 modelos | H-01 | C-01 | *Por calcular* | — | Ninguno en la selección |
| RM de localidad | < 1 (ponderadas) | H-06 | C-07 | *Por calcular* | — | No se reportan como hallazgo |
| AUC del modelo principal | 0.696 (CV) | H-08 | C-08 | *Esperado: ≈0.70* | — | Ninguno |
| Tasas por subgrupo | Sin IC | H-03 | C-03/C-04 | *Con IC* | — | Tono y estados pasan a nivel C |
| Escenarios | Sin ponderar | H-10 | C-10 | *Por calcular* | — | — |

> Advertencia: las cifras "esperadas" vienen de las verificaciones de esta auditoría (`checks*.py`) y deben confirmarse en la implementación.

---

## 18. Insumos para el Proyecto Integrador

| Apartado | Evidencia disponible | Estado | Acción necesaria | Fuente | Dependencia |
|---|---|---|---|---|---|
| 1. Introducción y planteamiento | NB 00, roadmap | Listo | Reformular el lenguaje de "pobreza" (C-09) | NB 00 | C-09 |
| 2. Descripción de datos | NB 01, `base_de_datos.md` | Listo | Agregar ESS y la nota de representatividad | NB 01 | — |
| 3. Limpieza y preparación | NB 02, bitácora | Listo | Corregir "45 bienes" | NB 02 | C-13 |
| 4. EDA | NB 03 | Requiere corrección | IC en los subgrupos; estatal exploratorio | NB 03 | C-03..C-06 |
| 5. Modelado | NB 04–05 | Listo | — | — | — |
| 6. Comparación y selección | NB 05 | Requiere corrección | Quitar la columna de tono de la matriz de decisión | NB 05 | C-01 |
| 7. Desarrollo matemático | `fundamentos_matematicos.md` | Listo | Corregir la fila "Brier… calibración no uniforme por tono" | docs | C-02 |
| 8. Resultados y discusión | NB 06–08 | Requiere corrección | Retirar H-01, reformular H-05 | NB 06–08 | C-01..C-05 |
| 9. Conclusiones y trabajo futuro | README, `auditoria_final.md` | Parcial | Usar la sección 14 de este documento | — | Todas |
| 10. Referencias | `referencias.md` | Parcial | Verificar | — | C-12 |

**Para la defensa oral:** por qué bienes y no ingreso; qué significa un AUC de 0.70; por qué se retiró el sesgo por tono (es una muestra de rigor); quintiles por cohorte; diferencia entre relativa y absoluta; por qué la educación no es "la causa".

---

## 19. Decisiones que el equipo debe aprobar antes de intervenir el repositorio

| # | Decisión | Recomendación de la auditoría |
|---|---|---|
| 1 | ¿Se aprueba el dictamen APROBADO CON CAMBIOS? | Sí |
| 2 | ¿Se **retira** el hallazgo del sesgo por tono (H-01) en todos los documentos, conservando su historia en la bitácora? | Sí |
| 3 | ¿Se cambia el lenguaje "pobreza" por "20% de hogares con menos bienes" en los textos técnicos, manteniendo "pobreza" solo en el título con una aclaración? | Sí. Título sugerido: *"¿Qué tan pegajosa es la pobreza? Persistencia en la base de la distribución de bienes en México"* |
| 4 | ¿Se quita la **autoadscripción** del modelo y se reemplaza el tono autopercibido por el colorímetro (C-08)? | Sí (el AUC no cambia y la interpretación queda más limpia) |
| 5 | ¿El análisis estatal sale del cartel (queda solo en el reporte como exploratorio)? | Sí |
| 6 | ¿Se cambia la referencia de localidad a "Ciudad" en el logit? | Sí |
| 7 | ¿Se trabaja en la rama `correcciones-auditoria` y se fusiona a `main` tras la validación? | Sí |
| 8 | ¿Quién sube las rúbricas oficiales y verifica las referencias y la cifra del CEEY? | Asignar responsable |
| 9 | ¿Se registran las fases 0–11 como APROBADA CON CAMBIOS en el roadmap (6.1) tras implementar? | Sí, después de la validación |

---

## 20. Dictamen final: **APROBADO CON CAMBIOS**

**Justificación.** La pregunta central es respondible con los datos y la respuesta es robusta. El pipeline no tiene leakage, es reproducible (ver el Anexo A) y los errores estándar del modelo explicativo están verificados de forma independiente. Los problemas encontrados afectan **hallazgos secundarios** y **la forma de reportar la incertidumbre**, no la conclusión central.

**Hallazgos determinantes:** H-01 (retirar), H-02 y H-03 (incertidumbre), H-04 y H-05 (reclasificar como exploratorios).

**Riesgos residuales (estructurales):** recuerdo retrospectivo, supervivencia, diseño transversal (sin causalidad), lengua y tono medidos hoy, falta de representatividad estatal.

**Acciones obligatorias antes del cartel:** C-01, C-02, C-03, C-09 y la aprobación del equipo (C-16).

**Acciones recomendadas:** C-04 a C-08, C-10, C-11.

**Condiciones para avanzar al cartel:** decisiones 1–5 aprobadas, correcciones P0 implementadas y validadas, y ninguna cifra del cartel sin IC o sin fuente rastreable en `reports/tables/`.

---

## Anexo A. Reproducción completa (sección 4.3)

| Revisión | Resultado |
|---|---|
| Notebooks ejecutados desde cero | 9 de 9, sin errores |
| Tablas comparadas | 29 CSV de `reports/tables/` |
| Idénticas | **29 de 29** (diferencia numérica máxima 0; columnas de texto iguales) |
| Datos regenerados | `emovi_movilidad.parquet` y `contexto_estatal_2022.csv`, reconstruidos desde los zips y los Releases |
| Repositorio original | Sin cambios (`git status` limpio en `10533d7`) |
| Limitación | Se reprodujo con el mismo entorno (las mismas versiones de las librerías). Con `requirements.txt` sin versiones fijas, otra máquina podría obtener diferencias menores (H-14) |

## Anexo B. Scripts de verificación

Se entregan junto con este documento: `checks1.py` (empates, ESS, IC por conglomerado), `checks2.py` (IC de subgrupos, calibración fuera de muestra, autoadscripción, efecto cohorte), `checks3.py` (sensibilidad a pesos, VIF, sandwich manual, ESS estatal). Leen los datos del repositorio sin modificarlos.
