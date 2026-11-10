# ¿Qué tan pegajosa es la pobreza?
## Roadmap maestro para un proyecto de Machine Learning sobre movilidad social en México

**Versión:** 1.0  
**Estado:** Documento vivo  
**Propósito:** Servir como fuente permanente de contexto, control metodológico, bitácora y guía de prompts durante todo el proyecto, sin depender de que una IA conserve conversaciones anteriores.

---

## 1. Cómo utilizar este documento

Este archivo debe mantenerse actualizado durante todo el proyecto. Antes de iniciar una nueva conversación con una herramienta de IA, se recomienda compartir:

1. La sección **Contexto maestro para la IA**.
2. La fase actual del proyecto.
3. Las decisiones registradas en la **Bitácora Maestra de Decisiones**.
4. Las hipótesis activas del **Registro de Hipótesis**.
5. Los resultados y limitaciones ya validados.
6. El prompt específico de la fase.

La IA debe tratar este documento como contexto del proyecto, pero no como evidencia empírica. Cualquier conclusión sobre México deberá sustentarse posteriormente con datos, literatura o fuentes verificables.

### Regla de avance

Cada fase deberá terminar con uno de estos estados:

- **APROBADA:** puede iniciarse la siguiente fase.
- **APROBADA CON CAMBIOS:** puede continuarse después de incorporar las correcciones indicadas.
- **REABRIR:** la fase contiene problemas que afectan decisiones posteriores.
- **BLOQUEADA:** falta información crítica, datos o una decisión humana.

No se avanzará únicamente porque un modelo o una IA haya producido una respuesta.

---

## 2. Contexto maestro para la IA

> Copiar esta sección al inicio de una nueva conversación cuando sea necesario.

```text
Estamos desarrollando un proyecto académico de Machine Learning titulado provisionalmente:

“¿Qué tan pegajosa es la pobreza? Movilidad social, persistencia económica y desigualdad de oportunidades en el México actual”.

El proyecto busca estudiar la movilidad social en México sin limitarse a contabilizar cuántas personas mejoraron, permanecieron o empeoraron económicamente. Queremos investigar qué circunstancias familiares, educativas, laborales, demográficas, territoriales y estructurales están asociadas con esas trayectorias, en qué grupos sociales se concentran y bajo qué condiciones las desventajas de origen parecen fortalecerse o debilitarse.

El proyecto todavía puede cambiar cuando conozcamos la base de datos. No deben inventarse variables, observaciones, distribuciones, resultados ni capacidades del dataset. Si los datos no permiten responder la pregunta original, deberá proponerse una reformulación metodológicamente honesta, sin forzar la información.

Principios obligatorios:
1. Diferenciar hechos, resultados, hipótesis, supuestos, inferencias y recomendaciones.
2. No confundir asociación, importancia predictiva o correlación con causalidad.
3. No seleccionar resultados solamente porque apoyen la narrativa original.
4. Conservar resultados contradictorios y explicaciones alternativas.
5. Dar prioridad a la trazabilidad de decisiones y a la comprensión humana.
6. Evaluar calidad, representatividad, missingness, leakage, sesgos y desempeño por subgrupos.
7. No elegir automáticamente el modelo con la métrica más alta.
8. Comparar desempeño, interpretabilidad, robustez, complejidad y estabilidad.
9. Explicar qué permiten concluir los datos y qué no permiten concluir.
10. Someter cada fase a revisión humana antes de avanzar.

La entrega académica debe cubrir planteamiento del problema, descripción y preparación de datos, análisis exploratorio, modelos, comparación, desarrollo matemático de al menos dos modelos, resultados, sesgos, limitaciones, conclusiones, trabajo futuro y referencias. El código deberá organizarse en notebooks de Jupyter o scripts de Python, y el reporte final se preparará en PDF.
```

---

## 3. Propósito y visión del proyecto

### 3.1 Título provisional

**¿Qué tan pegajosa es la pobreza? Movilidad social, persistencia económica y desigualdad de oportunidades en el México actual**

### 3.2 Pregunta central provisional

> ¿En qué medida las condiciones socioeconómicas de origen están asociadas con la posición económica alcanzada en la edad adulta en México, y qué factores individuales, familiares, territoriales y estructurales aumentan o reducen la probabilidad de movilidad social ascendente, permanencia o descenso?

### 3.3 Objetivo general provisional

Analizar la persistencia de la posición socioeconómica y las trayectorias de movilidad social en México mediante técnicas estadísticas y de Machine Learning, identificando perfiles, asociaciones, interacciones y condiciones relacionadas con el ascenso, la permanencia o el descenso económico, sin atribuir causalidad cuando el diseño de los datos no lo permita.

### 3.4 Resultado deseado

El proyecto deberá producir:

- Una definición operativa y defendible de movilidad social.
- Una auditoría clara de la fuente de datos.
- Un análisis exploratorio orientado por preguntas.
- Modelos base, explicativos y predictivos comparables.
- Evaluación por clases y subgrupos relevantes.
- Interpretación de factores y perfiles sin exagerar causalidad.
- Escenarios hipotéticos con supuestos explícitos.
- Una narrativa atractiva, objetiva y metodológicamente auditable.
- Un reporte final, código reproducible y documentación del proceso.

---

## 4. Principios metodológicos no negociables

1. **La pregunta no debe forzarse sobre los datos.** Si la base no contiene origen y destino socioeconómico, se reformulará el alcance.
2. **La definición de movilidad debe preceder a los resultados.** Los cambios posteriores deberán documentarse.
3. **Predicción no equivale a explicación causal.**
4. **Importancia de variables no equivale a efecto causal.**
5. **El mejor modelo no es necesariamente el de mayor accuracy.**
6. **Las métricas agregadas no sustituyen la evaluación por subgrupos.**
7. **La ausencia de datos puede tener patrones socioeconómicos.** No se imputará automáticamente.
8. **Los outliers pueden representar desigualdad real.** No se eliminarán sin análisis.
9. **Las categorías pequeñas no se agruparán solamente para facilitar el modelado.** Se evaluará la pérdida sustantiva.
10. **No se ocultarán contradicciones.** Se convertirán en preguntas de investigación.
11. **La narrativa seguirá a la evidencia.** Nunca se modificarán los resultados para sostener la historia.
12. **Toda decisión deberá quedar registrada.**

---

## 5. Arquitectura general del proyecto

```text
FASE 0   Constitución y control del proyecto
   ↓
FASE 1   Preguntas de investigación e hipótesis
   ↓
FASE 2   Marco conceptual y definición de movilidad
   ↓
FASE 3   Localización, selección y auditoría de datos
   ↓
        PUERTA DE DECISIÓN DE DATOS
       ↙              ↓               ↘
 clasificación     regresión     rediseño del estudio
       ↘              ↓               ↙
FASE 4   Preparación, partición y feature engineering
   ↓
FASE 5   Análisis exploratorio y mapa de desigualdades
   ↓
FASE 6   Baselines y criterios de aceptación
   ↓
FASE 7   Modelado y comparación
   ↓
FASE 8   Fundamentos matemáticos y validación profunda
   ↓
FASE 9   Interpretabilidad, perfiles y convergencia de evidencia
   ↓
FASE 10  Escenarios futuros y simulaciones condicionadas
   ↓
FASE 11  Red team, sesgos, robustez y auditoría adversarial
   ↓
FASE 12  Síntesis, narrativa, reporte y presentación
   ↓
FASE 13  Auditoría final contra la rúbrica y reproducibilidad
```

---

# 6. Fases del proyecto y prompts reutilizables

## FASE 0. Constitución y control del proyecto

### Objetivo

Definir las reglas del estudio antes de observar resultados y establecer los límites de lo que una IA puede decidir.

### Entregables

- Constitución metodológica.
- Alcance provisional.
- Objetivo general y objetivos específicos.
- Preguntas iniciales.
- Riesgos metodológicos.
- Bitácora de decisiones inicial.
- Lista de aspectos pendientes.

### Criterio de salida

El investigador puede explicar con sus propias palabras qué quiere estudiar, qué no puede afirmar todavía y qué decisiones siguen abiertas.

### Prompt 0

```text
Estamos desarrollando un proyecto académico de Machine Learning titulado provisionalmente “¿Qué tan pegajosa es la pobreza? Movilidad social, persistencia económica y desigualdad de oportunidades en el México actual”.

Actúa como científico de datos, analista socioeconómico y revisor metodológico.

Todavía no contamos con una base de datos validada. Por tanto, no inventes variables, observaciones, distribuciones ni resultados.

Construye la constitución metodológica del proyecto incluyendo:
1. Problema de investigación.
2. Objetivo general.
3. Entre 4 y 7 objetivos específicos.
4. Pregunta central.
5. Preguntas secundarias.
6. Hipótesis iniciales que posteriormente puedan rechazarse.
7. Definición conceptual de movilidad social.
8. Definición provisional de persistencia socioeconómica.
9. Diferencia entre pobreza, ingreso, riqueza, posición socioeconómica y movilidad social.
10. Alcance geográfico, temporal y poblacional provisional.
11. Qué afirmaciones requerirían evidencia causal y cuáles pueden sostenerse mediante asociación o predicción.
12. Principales riesgos metodológicos.
13. Posibles explicaciones alternativas.
14. Información que todavía necesitamos conocer antes de cerrar la metodología.

Separa explícitamente hechos, hipótesis, supuestos, decisiones metodológicas y aspectos pendientes de validar.

No intentes hacer que nuestras hipótesis parezcan correctas. El objetivo será ponerlas a prueba.

Termina con “Decisiones que el investigador debe revisar antes de aprobar esta fase”. No avances a selección de modelos.
```

### Revisión humana

- ¿La pregunta representa realmente la intención del proyecto?
- ¿Se mezclan pobreza y movilidad?
- ¿Hay una hipótesis presentada como hecho?
- ¿El alcance es viable?
- ¿Existe lenguaje causal injustificado?

---

## FASE 1. Árbol de preguntas e hipótesis

### Objetivo

Transformar la idea narrativa en preguntas medibles, falsables y no redundantes.

### Entregables

- Árbol de preguntas.
- Hipótesis nulas y alternativas.
- Registro de hipótesis.
- Priorización de 3 a 5 preguntas centrales.
- Mapa de confusores y explicaciones alternativas.

### Prompt 1

```text
Partiendo exclusivamente de la constitución metodológica aprobada, transforma la pregunta “¿Qué tan pegajosa es la pobreza?” en un árbol de preguntas de investigación medibles.

Para cada pregunta genera:
- hipótesis nula;
- hipótesis alternativa;
- variable resultado requerida;
- variables explicativas potenciales;
- información necesaria para probarla;
- técnica estadística potencial;
- posible aplicación de Machine Learning;
- principal variable de confusión;
- explicación alternativa;
- resultado que refutaría nuestra hipótesis.

Clasifica las preguntas como descriptivas, asociativas, predictivas, exploratorias o causales.

Si una pregunta causal probablemente no puede contestarse con datos observacionales, indícalo expresamente.

No selecciones todavía los modelos finales. Identifica las 3 a 5 preguntas de mayor valor académico evitando redundancias.

Termina con “Decisiones que debe tomar el investigador”.
```

### Hito crítico

Si las preguntas principales no pueden asociarse con variables observables plausibles, se deberá reformular el estudio antes de buscar modelos.

---

## FASE 2. Marco conceptual y operacionalización

### Objetivo

Evitar la confusión entre pobreza, ingreso, riqueza, vulnerabilidad y movilidad social.

### Entregables

- Glosario conceptual.
- Comparación entre movilidad absoluta y relativa.
- Alternativas de variable objetivo.
- Decisiones conceptuales congeladas.
- Decisiones adaptables al dataset.

### Prompt 2

```text
Construye el marco conceptual necesario para estudiar movilidad social en México dentro de este proyecto.

Distingue rigurosamente:
- ingreso;
- pobreza;
- vulnerabilidad;
- riqueza;
- posición socioeconómica;
- movilidad absoluta;
- movilidad relativa;
- movilidad intrageneracional;
- movilidad intergeneracional;
- persistencia socioeconómica;
- igualdad de oportunidades.

Para cada concepto indica:
1. qué representa;
2. cómo podría operacionalizarse;
3. qué información requeriríamos;
4. ventajas;
5. limitaciones;
6. error interpretativo producido por utilizarlo incorrectamente.

Propón diferentes maneras de operacionalizar la variable objetivo sin decidir todavía cuál utilizaremos. Compara quintiles, deciles, índices socioeconómicos, ingreso, condición de pobreza y cambios relativos.

No inventes información sobre la futura base.

Finaliza indicando qué decisiones conceptuales conviene congelar antes de observar resultados y cuáles pueden adaptarse legítimamente al conocer los datos.
```

### Riesgo principal

Definir la variable objetivo después de observar qué definición produce resultados más interesantes. Todo cambio deberá documentarse y justificarse.

---

## FASE 3. Adquisición, selección y auditoría de datos

### Objetivo

Determinar qué pregunta puede contestarse realmente con la información disponible.

### Posibles fuentes candidatas

Estas fuentes deberán evaluarse y verificarse antes de usarse:

- Encuesta ESRU de Movilidad Social en México.
- ENIGH del INEGI.
- ENOE del INEGI.
- Medición de pobreza de CONEVAL.
- Datos territoriales públicos de educación, empleo, salud, informalidad y acceso a servicios.

La inclusión de una fuente no implica que pueda unirse a otra a nivel individual. Si no existen identificadores compartidos, solo podrán realizarse integraciones agregadas y metodológicamente justificadas.

### Entregables

- Ficha técnica de cada fuente.
- Diccionario de variables.
- Reporte de calidad.
- Evaluación de representatividad.
- Riesgos de integración.
- Puerta de decisión VERDE, AMARILLO o ROJO.

### Prompt 3A. Evaluación de fuentes

```text
Evalúa las fuentes candidatas para responder nuestra pregunta de movilidad social.

Para cada fuente documenta:
- institución responsable;
- periodo;
- cobertura;
- unidad de observación;
- representatividad;
- diseño muestral;
- ponderadores;
- variables relacionadas con origen;
- variables relacionadas con situación actual;
- posibilidad de medir movilidad;
- restricciones de acceso o uso;
- compatibilidad con otras fuentes;
- principal fortaleza;
- principal limitación.

No supongas que dos encuestas pueden integrarse a nivel persona. Distingue integración individual, territorial y contextual.

Recomienda una fuente principal y fuentes complementarias, pero conserva las alternativas si la fuente principal no está disponible.
```

### Prompt 3B. Auditoría del dataset recibido

```text
Tenemos acceso a los datos candidatos. No construyas todavía modelos y no elimines observaciones.

Realiza una auditoría completa:
1. unidad de observación;
2. número de observaciones y variables;
3. periodo;
4. cobertura geográfica;
5. población representada;
6. factores de expansión o ponderadores;
7. tipos de variables;
8. IDs y llaves;
9. porcentaje de faltantes;
10. duplicados;
11. valores imposibles o sospechosos;
12. categorías escasas;
13. outliers;
14. información retrospectiva;
15. variables de origen;
16. variables de situación actual;
17. potenciales targets;
18. proxies sensibles;
19. variables con riesgo de leakage;
20. variables que requieren consultar el diccionario.

Distingue entre problema verdadero de calidad, característica legítima y aspecto indeterminado.

No realices imputación automática.

Evalúa si los datos permiten responder la pregunta original. Si no, propone una reformulación honesta.

Termina con “Puerta de decisión de datos”:
VERDE: continuar.
AMARILLO: continuar con restricciones.
ROJO: replantear.
```

### Árbol de adaptación según los datos

| Situación encontrada | Ruta recomendada |
|---|---|
| Origen y situación adulta comparables | Movilidad intergeneracional |
| Varias observaciones por persona en el tiempo | Movilidad longitudinal o intrageneracional |
| Solo situación actual | Desigualdad de oportunidades o vulnerabilidad, no movilidad demostrada |
| Target continuo confiable | Regresión y análisis distributivo |
| Categorías defendibles de ascenso/permanencia/descenso | Clasificación |
| Sin target adecuado y muchas características | Clustering exploratorio y perfiles |
| Datos agregados territoriales | Análisis regional, evitando conclusiones individuales |
| Muestra pequeña | Modelos simples, validación cuidadosa e incertidumbre explícita |
| Gran missingness no aleatoria | Modelado o análisis del patrón de ausencia |
| Pocos datos de origen | Proxy documentado, sensibilidad y reducción de alcance |

---

## FASE 4. Preparación, partición y feature engineering

### Objetivo

Construir un pipeline reproducible sin alterar silenciosamente el fenómeno social.

### Entregables

- Plan de limpieza aprobado.
- Bitácora de transformaciones.
- Pipeline reproducible.
- Estrategia train/validation/test.
- Pruebas de leakage.
- Dataset analítico versionado.

### Prompt 4A. Diseño

```text
A partir únicamente de la auditoría aprobada, diseña el pipeline de preparación.

Por cada transformación presenta:
- variable afectada;
- problema detectado;
- transformación propuesta;
- alternativas;
- justificación;
- información perdida;
- riesgo de sesgo;
- efecto esperado en los modelos.

Incluye missing values, categorías, outliers, ponderadores, escalamiento, dimensionalidad, leakage, duplicados, variables ordinales, monetarias, temporales y sensibles.

No escribas todavía el pipeline definitivo. Presenta las decisiones para aprobación humana y señala cuáles pueden cambiar materialmente las conclusiones.
```

### Prompt 4B. Implementación

```text
Implementa únicamente las transformaciones aprobadas en la bitácora.

Requisitos:
- código modular y reproducible;
- no modificar el archivo original;
- guardar dataset intermedio con versión;
- separar fit y transform para evitar leakage;
- documentar entradas y salidas;
- validar tipos y rangos después de transformar;
- generar un reporte automático de filas, columnas y missingness antes y después;
- registrar cualquier desviación respecto al plan aprobado.

No entrenes todavía modelos finales.
```

### Problemas previsibles

- **Ingreso altamente sesgado:** evaluar logaritmo, cuantiles y robustez sin ocultar desigualdad.
- **Inflación o años distintos:** llevar variables monetarias a precios comparables.
- **Categorías raras:** agrupar solo con fundamento sustantivo.
- **Ponderadores:** distinguir análisis descriptivo representativo de entrenamiento predictivo.
- **Clases desbalanceadas:** no resolver exclusivamente con oversampling; comparar class weights, métricas balanceadas y calibración.
- **Leakage temporal:** excluir información conocida únicamente después del resultado.

---

## FASE 5. Análisis exploratorio orientado por preguntas

### Objetivo

Comprender distribuciones, relaciones, grupos y contradicciones sin convertir correlaciones en causalidad.

### Entregables

- Notebook de EDA.
- Diccionario visual.
- Matriz de movilidad, si procede.
- Hallazgos esperados y contradictorios.
- Actualización del registro de hipótesis.

### Visualizaciones candidatas

- Distribución del target.
- Matriz origen-destino.
- Probabilidad de ascenso desde estratos bajos.
- Movilidad por región y condición urbano/rural.
- Movilidad por género y pertenencia a grupos relevantes.
- Escolaridad parental frente a propia.
- Educación frente a resultado económico.
- Formalidad, ocupación o sector frente a trayectoria.
- Missingness por grupo.
- Perfiles y tamaños de muestra.

### Prompt 5

```text
Realiza el análisis exploratorio evitando buscar únicamente evidencia favorable a nuestras hipótesis.

Organiza el EDA mediante preguntas. Para cada hallazgo reporta:
1. qué observamos;
2. magnitud;
3. población afectada;
4. posible explicación;
5. explicaciones alternativas;
6. confusores;
7. prueba posterior necesaria;
8. efecto sobre las hipótesis iniciales.

Busca resultados esperados, anomalías, contradicciones, subgrupos que rompan la tendencia, interacciones, diferencias territoriales, efectos Simpson, distribuciones sesgadas y grupos con pocos datos.

No interpretes correlación como causalidad.

Actualiza cada hipótesis como:
APOYADA PROVISIONALMENTE / DEBILITADA / SIN EVIDENCIA / CONTRADICHA.

Conserva las hipótesis y resultados contradictorios.
```

---

## FASE 6. Baselines y criterios de aceptación

### Objetivo

Establecer el desempeño mínimo que cualquier modelo complejo deberá superar.

### Baselines posibles

- Clase mayoritaria o `DummyClassifier`.
- Predicción estratificada.
- Media o mediana en regresión.
- Regresión logística o lineal sencilla.
- Árbol poco profundo como referencia interpretable.

### Métricas candidatas

Para clasificación:

- Balanced accuracy.
- Precision, recall y F1 por clase.
- Macro F1.
- Matriz de confusión.
- ROC-AUC One-vs-Rest, si procede.
- PR-AUC para clases raras.
- Log loss.
- Calibración.

Para regresión:

- MAE.
- RMSE.
- R², interpretado con cautela.
- Error por cuantiles y subgrupos.
- Diagnóstico de residuos.

### Prompt 6

```text
Construye los baselines apropiados para el problema aprobado.

Evalúa:
- estrategia ingenua;
- modelo estadístico sencillo;
- métricas justificadas;
- desempeño por clase;
- calibración;
- desempeño por subgrupos.

Explica qué tendría que aportar un modelo más complejo para justificar su uso.

No concluyas que un modelo complejo es mejor únicamente por mejorar una métrica.

Establece criterios objetivos de aceptación y descarte para los modelos posteriores.
```

---

## FASE 7. Modelado y comparación

### Objetivo

Comparar una escalera de complejidad y seleccionar modelos por utilidad científica, no solo por rendimiento.

### Escalera recomendada provisional

1. Dummy baseline.
2. Regresión logística o lineal.
3. Árbol de decisión.
4. Random Forest.
5. SVM, KNN, Naive Bayes u otro modelo solo si se justifica por la naturaleza de los datos.
6. K-Means o clustering jerárquico como componente complementario de perfiles, no como sustituto automático del target.

### Prompt 7

```text
Entrena y compara modelos siguiendo una escalera de complejidad.

Por cada modelo registra:
- objetivo;
- justificación;
- hiperparámetros;
- validación;
- métricas;
- desempeño frente al baseline;
- interpretabilidad;
- estabilidad;
- sensibilidad al preprocesamiento;
- tiempo y complejidad;
- principal ventaja;
- principal debilidad.

No selecciones automáticamente el modelo con la métrica más alta.

Construye una matriz de decisión con:
1. desempeño predictivo;
2. interpretabilidad;
3. robustez;
4. estabilidad entre subgrupos;
5. complejidad;
6. adecuación científica.

Marca los casos donde los modelos produzcan conclusiones distintas para revisión humana.
```

### Regla de selección

Si un modelo complejo mejora poco frente a uno interpretable, deberá justificarse por qué esa mejora compensa la pérdida de claridad, estabilidad o auditabilidad.

---

## FASE 8. Fundamentos matemáticos y validación profunda

### Objetivo

Conectar la teoría matemática de al menos dos modelos con las decisiones reales del proyecto.

### Entregables

- Formulación matemática.
- Función de costo.
- Optimización.
- Supuestos.
- Interpretación de parámetros.
- Relación con datos y métricas.
- Diagnósticos de validación.

### Prompt 8

```text
Desarrolla la fundamentación matemática de los dos modelos seleccionados empíricamente.

Para cada uno explica:
- notación;
- variables;
- formulación;
- función objetivo;
- función de costo;
- optimización;
- regularización;
- interpretación de parámetros;
- supuestos;
- relación con nuestros datos reales.

Conecta cada elemento matemático con una decisión concreta del proyecto.

No redactes matemáticas genéricas copiables a cualquier estudio. Explica específicamente qué significan dentro del análisis de movilidad social.
```

### Validaciones recomendadas

- Validación cruzada estratificada o temporal, según el diseño.
- Intervalos de confianza o variabilidad entre folds.
- Curvas de aprendizaje.
- Sensibilidad a semillas aleatorias.
- Sensibilidad a imputación y selección de variables.
- Calibración.
- Desempeño por subgrupos.
- Stress tests ante cambios de definición del target.

---

## FASE 9. Interpretabilidad, perfiles y convergencia de evidencia

### Objetivo

Investigar qué factores y combinaciones utiliza el modelo, separando asociación, predicción y posibles mecanismos.

### Técnicas candidatas

- Coeficientes y odds ratios.
- Importancia por permutación.
- SHAP global y local.
- Partial dependence o ALE cuando sean apropiados.
- Interacciones.
- Árboles simplificados.
- Análisis de errores.
- Clustering de perfiles.

### Prompt 9

```text
Analiza qué factores utiliza el modelo para distinguir trayectorias de movilidad social.

Distingue:
- importancia predictiva;
- asociación estadística;
- interacción;
- posible mecanismo socioeconómico;
- evidencia causal.

Para cada factor pregunta:
1. ¿Es robusto entre modelos?
2. ¿Es robusto entre subgrupos?
3. ¿Puede ser un proxy?
4. ¿Existe explicación alternativa?
5. ¿Puede haber causalidad inversa?
6. ¿Hay variables omitidas?
7. ¿Coincide con el EDA?

Utiliza perfiles estadísticos solamente como ilustración, no como prueba causal.

Termina con una tabla de convergencia mostrando qué conclusiones están apoyadas por EDA, modelos, pruebas y subgrupos.
```

### Tabla de convergencia sugerida

| Conclusión candidata | EDA | Modelo interpretable | Modelo complejo | Subgrupos | Literatura | Nivel de confianza |
|---|---|---|---|---|---|---|
| Pendiente | Pendiente | Pendiente | Pendiente | Pendiente | Pendiente | No evaluado |

---

## FASE 10. Escenarios futuros y simulaciones

### Objetivo

Explorar escenarios condicionados sin presentarlos como pronósticos inevitables ni efectos causales demostrados.

### Escenarios provisionales

1. Continuidad.
2. Mejora educativa.
3. Mejora educativa sin mejora laboral.
4. Mejora educativa con empleo formal o productivo.
5. Reducción de brechas territoriales.
6. Choque adverso de empleo, ingreso o vulnerabilidad.

### Prompt 10

```text
Construye escenarios exploratorios únicamente dentro de los límites de los datos.

Diferencia rigurosamente:
- predicción;
- forecast;
- simulación;
- escenario hipotético;
- inferencia causal.

Para cada escenario especifica:
- variables modificadas;
- variables constantes;
- plausibilidad;
- resultado estimado;
- incertidumbre;
- supuesto principal;
- razón por la que no implica necesariamente causalidad.

Rechaza escenarios que requieran extrapolación no sustentada.
```

### Regla de lenguaje

Usar: “Bajo el escenario hipotético X y manteniendo las relaciones estimadas...”  
Evitar: “La política X causará...” o “En el futuro ocurrirá...”.

---

## FASE 11. Red team, sesgos y robustez

### Objetivo

Intentar refutar el proyecto antes de redactar la historia final.

### Prompt 11

```text
Actúa como un revisor académico escéptico que intenta rechazar el proyecto.

Busca:
- sesgo de confirmación;
- leakage;
- selección conveniente de variables;
- causalidad injustificada;
- cherry picking;
- métricas cuestionables;
- problemas de representatividad;
- desbalance;
- proxies sensibles;
- variables omitidas;
- resultados inestables;
- escenarios injustificados;
- visualizaciones engañosas;
- redundancias;
- contradicciones;
- decisiones tomadas después de observar resultados.

Clasifica cada problema como CRÍTICO, ALTO, MEDIO o BAJO.

Para riesgos CRÍTICOS y ALTOS exige una acción correctiva o recomienda retirar la conclusión.

Termina respondiendo: “¿Qué afirmación sería la más fácil de atacar académicamente y por qué?”.
```

### Riesgos que deberán evaluarse siempre

- Sesgo de recuerdo en información retrospectiva.
- Sesgo de supervivencia.
- Sesgo urbano o territorial.
- Selección de muestra.
- Desbalance de clases.
- Variables proxy.
- Leakage.
- Missingness no aleatoria.
- Falacia ecológica.
- Confusión entre movilidad absoluta y relativa.
- Confusión entre educación y oportunidades laborales.
- Efectos heterogéneos ocultos por promedios nacionales.

---

## FASE 12. Síntesis, narrativa, reporte y presentación

### Objetivo

Construir una historia atractiva que represente la evidencia, incluyendo contradicciones y límites.

### Estructura narrativa sugerida

1. La paradoja inicial.
2. El punto de partida.
3. Quién asciende, permanece y desciende.
4. Circunstancias que diferencian trayectorias.
5. Casos o grupos que rompen la tendencia.
6. Interacción entre individuo, familia, mercado y territorio.
7. Lo aprendido por los modelos.
8. Lo que no puede concluirse.
9. Escenarios posibles.
10. Respuesta final a “¿qué tan pegajosa es la pobreza?”.

### Prompt 12

```text
Construye la narrativa final utilizando exclusivamente resultados validados.

Quiero una narrativa clara para lectores no especializados, pero rigurosa.

Incluye:
1. pregunta o paradoja inicial;
2. punto de partida;
3. quién asciende, permanece y desciende;
4. características asociadas con sus trayectorias;
5. excepciones;
6. interacción entre individuo, familia y entorno;
7. qué aprendieron los modelos;
8. qué no podemos concluir;
9. escenarios;
10. respuesta final.

Evita dramatización, causalidad sin evidencia, redundancias, lenguaje partidista, moralización y cherry picking.

Cuando existan resultados contradictorios, incorpóralos.

Diferencia evidencia, interpretación e hipótesis.
```

### Estructura del reporte académico

1. Introducción y planteamiento.
2. Descripción de datos.
3. Limpieza y preparación.
4. Análisis exploratorio.
5. Modelado.
6. Comparación y selección.
7. Desarrollo matemático de dos modelos.
8. Resultados y discusión.
9. Conclusiones y trabajo futuro.
10. Referencias.

---

## FASE 13. Auditoría final y reproducibilidad

### Objetivo

Verificar cobertura de la rúbrica, consistencia interna, reproducibilidad y comprensión técnica.

### Prompt 13

```text
Audita el proyecto terminado contra la rúbrica oficial.

Clasifica cada requisito como CUMPLIDO, PARCIAL o NO CUMPLIDO.

No otorgues crédito porque una sección simplemente exista. Evalúa si demuestra comprensión.

Comprueba:
- definición y justificación;
- datos;
- preparación;
- EDA;
- modelos;
- comparación;
- justificación metodológica;
- desarrollo matemático;
- métricas;
- interpretación;
- sesgos;
- limitaciones;
- conclusiones;
- trabajo futuro;
- referencias;
- claridad y reproducibilidad del código.

Para cada punto parcial o faltante indica qué agregar o corregir.

Finalmente formula las cinco preguntas más difíciles que un profesor podría realizar durante la presentación.

No inventes evidencia para completar apartados ausentes.
```

### Checklist técnico final

- [ ] Ambiente reproducible documentado.
- [ ] Semillas registradas.
- [ ] Datos originales preservados.
- [ ] Transformaciones reproducibles.
- [ ] Separación correcta de datos.
- [ ] Ausencia de leakage revisada.
- [ ] Modelos y parámetros registrados.
- [ ] Métricas reproducibles.
- [ ] Figuras exportadas con títulos y fuentes.
- [ ] Referencias completas.
- [ ] Limitaciones visibles.
- [ ] Resultados contradictorios documentados.
- [ ] Reporte PDF final.
- [ ] Notebook o scripts organizados.
- [ ] README actualizado.

---

# 7. Checkpoints mayores

| Hito | Pregunta de control | Acción si falla |
|---|---|---|
| H1 Conceptual | ¿Estamos haciendo la pregunta correcta? | Volver a Fases 0-2 |
| H2 Datos | ¿Los datos permiten contestarla? | Reformular pregunta o cambiar fuente |
| H3 Científico | ¿Los resultados sobreviven validación, modelos y subgrupos? | Volver a Fases 4-9 |
| H4 Narrativo | ¿La historia representa la evidencia sin exagerarla? | Cambiar narrativa, no resultados |

---

# 8. Escenarios problemáticos y respuestas

## 8.1 No existe una variable directa de origen socioeconómico

**Riesgo:** llamar movilidad intergeneracional a algo que no la mide.  
**Respuesta:** reducir el alcance a desigualdad de oportunidades, vulnerabilidad o asociación con antecedentes disponibles. Si se construye un proxy, documentar componentes, sensibilidad y limitaciones.

## 8.2 El dataset solo contiene una fotografía actual

**Riesgo:** inferir trayectorias sin tiempo ni información retrospectiva.  
**Respuesta:** no afirmar ascenso o descenso individual. Considerar clasificación de vulnerabilidad, segmentación o análisis territorial.

## 8.3 Existen muchos datos faltantes

**Riesgo:** sesgo por eliminación o imputación.  
**Respuesta:** estudiar patrones de missingness, comparar grupos, crear análisis de sensibilidad y mantener indicadores de ausencia cuando tengan sentido.

## 8.4 El target está desbalanceado

**Riesgo:** accuracy artificialmente alta.  
**Respuesta:** balanced accuracy, macro F1, recall por clase, PR-AUC, class weights, calibración y evaluación de errores.

## 8.5 Un modelo complejo gana por poco

**Riesgo:** perder interpretabilidad por una mejora marginal.  
**Respuesta:** preferir el modelo simple si la diferencia no es material o utilizar ambos con funciones distintas.

## 8.6 Los modelos cuentan historias diferentes

**Riesgo:** elegir el modelo que confirme la narrativa.  
**Respuesta:** localizar segmentos de desacuerdo, revisar interacciones, calibración, supuestos y estabilidad.

## 8.7 Una característica sensible resulta muy predictiva

**Riesgo:** discriminación, proxy o interpretación causal indebida.  
**Respuesta:** evaluación por grupo, análisis de proxies, explicación contextual y restricciones de uso.

## 8.8 La educación domina todos los modelos

**Riesgo:** conclusión trivial.  
**Respuesta:** estudiar dónde la educación sí o no rompe la persistencia, sus interacciones con empleo, territorio, género y origen.

## 8.9 El modelo tiene bajo desempeño

**Riesgo:** ocultar resultados o forzar complejidad.  
**Respuesta:** considerar que las variables observadas pueden ser insuficientes. Documentar el límite predictivo como hallazgo y evitar leakage para inflar métricas.

## 8.10 Los datos son de varios años

**Riesgo:** comparar valores monetarios y contextos no equivalentes.  
**Respuesta:** ajustar inflación, documentar cambios metodológicos, controlar periodo y considerar validación temporal.

## 8.11 Se integran fuentes distintas

**Riesgo:** falsa correspondencia entre personas o falacia ecológica.  
**Respuesta:** declarar el nivel de integración, verificar llaves, conservar granularidad y evitar inferencias individuales desde agregados.

## 8.12 Los resultados cambian con la definición de movilidad

**Riesgo:** conclusión dependiente de una decisión arbitraria.  
**Respuesta:** análisis de sensibilidad con definiciones alternativas y declaración de qué hallazgos son robustos.

---

# 9. Bitácora Maestra de Decisiones

Actualizar esta tabla durante todo el proyecto.

| ID | Fecha | Fase | Decisión | Alternativas | Evidencia | Riesgo | Responsable | Estado |
|---|---|---|---|---|---|---|---|---|
| D001 | Pendiente | 0 | México como ámbito inicial | Regional o estatal | Pregunta original | Heterogeneidad nacional | Investigador | Provisional |
| D002 | Pendiente | 0 | Movilidad social como tema central | Vulnerabilidad o desigualdad de oportunidades | Objetivo inicial | Datos insuficientes | Investigador | Provisional |
| D003 | Pendiente | 2 | Definición del target | Quintiles, pobreza, índice, ingreso | Sin dataset | Sesgo de definición | Investigador | No decidido |
| D004 | Pendiente | 6 | Modelo interpretable como baseline | Dummy solamente | Requisito de comparación | Subajuste | Equipo | Provisional |
| D005 | Pendiente | 7 | Random Forest como candidato | SVM, boosting, otro | Posible no linealidad | Menor interpretabilidad | Equipo | Provisional |

### Estados permitidos

`PROPUESTA / APROBADA / APROBADA CON CAMBIOS / RECHAZADA / REABIERTA / BLOQUEADA`

---

# 10. Registro de Hipótesis

| ID | Hipótesis | Evidencia necesaria | Evidencia a favor | Evidencia en contra | Confusores | Estado | Conclusión permitida |
|---|---|---|---|---|---|---|---|
| H001 | El origen socioeconómico se asocia con la posición adulta | Variables comparables de origen y destino | Pendiente | Pendiente | Región, cohorte, educación | No evaluada | Ninguna todavía |
| H002 | La educación puede moderar la persistencia | Educación propia, origen y destino | Pendiente | Pendiente | Calidad educativa, empleo | No evaluada | Ninguna todavía |
| H003 | El efecto asociado con educación varía territorialmente | Región e interacciones | Pendiente | Pendiente | Mercado laboral local | No evaluada | Ninguna todavía |
| H004 | Puede existir movilidad educativa sin movilidad económica equivalente | Educación parental/propia e ingreso/posición | Pendiente | Pendiente | Cohorte, ocupación | No evaluada | Ninguna todavía |
| H005 | Las combinaciones de desventajas pueden ser más informativas que factores aislados | Interacciones o modelos no lineales | Pendiente | Pendiente | Tamaño de muestra | No evaluada | Ninguna todavía |

### Estados permitidos

`NO EVALUADA / APOYADA PROVISIONALMENTE / DEBILITADA / SIN EVIDENCIA / CONTRADICHA / NO EVALUABLE`

---

# 11. Registro de Riesgos

| ID | Riesgo | Probabilidad | Impacto | Indicador | Mitigación | Estado |
|---|---|---:|---:|---|---|---|
| R001 | Dataset no mide origen y destino | Alta | Crítico | Ausencia de variables comparables | Reformular alcance | Abierto |
| R002 | Confusión entre asociación y causalidad | Alta | Alto | Lenguaje causal en borradores | Revisión metodológica y red team | Abierto |
| R003 | Leakage | Media | Crítico | Métricas anormalmente altas | Auditoría temporal y de variables | Abierto |
| R004 | Clases desbalanceadas | Media | Alto | Clase dominante | Métricas balanceadas y weights | Abierto |
| R005 | Falta de representatividad | Media | Alto | Diseño o cobertura limitada | Ponderadores y límites explícitos | Abierto |
| R006 | Narrativa anterior a la evidencia | Alta | Alto | Solo se buscan confirmaciones | EDA adversarial y registro de hipótesis | Abierto |
| R007 | Integración incorrecta de fuentes | Media | Crítico | Llaves no compatibles | Integración agregada o no integrar | Abierto |
| R008 | Definición inestable del target | Alta | Alto | Resultados cambian por umbral | Análisis de sensibilidad | Abierto |

---

# 12. Inventario de datos

| Dataset | Fuente | Periodo | Unidad | Cobertura | Ponderador | Acceso | Uso previsto | Restricciones | Estado |
|---|---|---|---|---|---|---|---|---|---|
| Pendiente | Pendiente | Pendiente | Pendiente | Pendiente | Pendiente | Pendiente | Pendiente | Pendiente | No evaluado |

---

# 13. Diccionario de variables analíticas

| Variable | Fuente | Tipo | Definición | Momento temporal | Rol | Sensible/proxy | Missing % | Transformación | Observaciones |
|---|---|---|---|---|---|---|---:|---|---|
| Pendiente | Pendiente | Pendiente | Pendiente | Pendiente | Pendiente | Pendiente | Pendiente | Pendiente | Pendiente |

Roles sugeridos: `ID / TARGET / PREDICTORA / CONTROL / PESO / AGRUPACIÓN / EXCLUIDA`.

---

# 14. Registro de experimentos

| Exp. | Fecha | Dataset | Target | Split | Preprocesamiento | Modelo | Parámetros | Métricas | Subgrupos | Artefacto | Decisión |
|---|---|---|---|---|---|---|---|---|---|---|---|
| E001 | Pendiente | Pendiente | Pendiente | Pendiente | Pendiente | Dummy | Pendiente | Pendiente | Pendiente | Pendiente | Pendiente |

Nunca reemplazar un experimento anterior. Crear una nueva fila.

---

# 15. Estructura recomendada del repositorio

```text
sticky-poverty-mx/
├── README.md
├── roadmap.md
├── requirements.txt
├── environment.yml
├── .gitignore
├── data/
│   ├── raw/
│   ├── interim/
│   ├── processed/
│   └── external/
├── docs/
│   ├── rubric/
│   ├── references/
│   ├── decisions/
│   └── report/
├── notebooks/
│   ├── 00_context_and_scope.ipynb
│   ├── 01_data_audit.ipynb
│   ├── 02_data_preparation.ipynb
│   ├── 03_eda.ipynb
│   ├── 04_baselines.ipynb
│   ├── 05_modeling.ipynb
│   ├── 06_interpretability.ipynb
│   ├── 07_scenarios.ipynb
│   └── 08_final_validation.ipynb
├── src/
│   ├── data/
│   ├── features/
│   ├── models/
│   ├── evaluation/
│   └── visualization/
├── reports/
│   ├── figures/
│   ├── tables/
│   └── final/
├── models/
└── tests/
```

### Reglas de archivos

- Los datos originales nunca se editan.
- Los notebooks se numeran y ejecutan en orden.
- El código reutilizable migra a `src/`.
- Las figuras finales se generan desde código.
- Los modelos guardados deben registrar versión de datos y parámetros.
- El README debe explicar cómo reproducir el proyecto.
- No subir datos sensibles o restringidos a GitHub.

---

# 16. Protocolo para trabajar con cualquier IA

Antes de aceptar una respuesta de IA, comprobar:

1. ¿Inventó datos, variables, fuentes o resultados?
2. ¿Presentó una hipótesis como hecho?
3. ¿Confundió asociación con causalidad?
4. ¿Ignoró una decisión aprobada?
5. ¿Cambió la definición del target sin registrarlo?
6. ¿Propuso eliminar datos sin evaluar sesgo?
7. ¿Utilizó accuracy como única métrica?
8. ¿Escogió el modelo más complejo sin justificación?
9. ¿Omitió subgrupos o representatividad?
10. ¿La conclusión es mayor que la evidencia?
11. ¿El código es reproducible y evita leakage?
12. ¿La respuesta contradice el diccionario o la bitácora?

### Prompt de recuperación de contexto

```text
Lee el roadmap adjunto y utiliza únicamente las decisiones marcadas como aprobadas. Estamos actualmente en la FASE [NÚMERO Y NOMBRE].

Antes de trabajar:
1. resume el estado actual;
2. identifica decisiones aprobadas, abiertas y bloqueadas;
3. enumera los archivos o resultados que necesitas;
4. advierte si el nuevo pedido contradice una decisión previa.

No avances a fases posteriores salvo que lo solicite expresamente. No inventes información ausente.
```

### Prompt de revisión de una respuesta producida por otra IA

```text
Audita la respuesta adjunta contra nuestro roadmap.

Identifica:
- afirmaciones sin evidencia;
- decisiones no autorizadas;
- supuestos ocultos;
- causalidad injustificada;
- riesgo de leakage;
- omisiones;
- contradicciones con la bitácora;
- instrucciones que no sean reproducibles.

Clasifica cada observación como CRÍTICA, ALTA, MEDIA o BAJA y presenta una versión corregida solamente después del diagnóstico.
```

---

# 17. Criterios de “terminado” por componente

## Datos

- Fuente y licencia documentadas.
- Unidad de observación comprendida.
- Ponderadores identificados.
- Calidad y missingness auditados.
- Integración justificada.

## EDA

- Preguntas explícitas.
- Tamaños de muestra visibles.
- Hallazgos y contradicciones registrados.
- Gráficas reproducibles.
- Sin lenguaje causal indebido.

## Modelo

- Baseline establecido.
- Validación adecuada.
- Métricas por clase y subgrupo.
- Calibración evaluada cuando corresponda.
- Robustez y sensibilidad documentadas.

## Interpretación

- Asociación separada de causalidad.
- Proxies considerados.
- Convergencia entre métodos evaluada.
- Casos de desacuerdo explicados.

## Reporte

- Responde a la pregunta central.
- Expone límites.
- Demuestra comprensión técnica.
- Incluye matemáticas conectadas al caso.
- No oculta resultados adversos.

---

# 18. Próximo paso recomendado

Iniciar formalmente la **FASE 0** mediante el Prompt 0. Después de revisar y aprobar la constitución metodológica:

1. Actualizar este archivo a la versión 1.1.
2. Registrar las decisiones D001 en adelante.
3. Crear el Registro de Hipótesis inicial.
4. Ejecutar la FASE 1.
5. No seleccionar un modelo final antes de la Puerta de Decisión de Datos.

---

# 19. Historial de versiones

| Versión | Fecha | Cambios | Autor/Revisor |
|---|---|---|---|
| 1.0 | 2026-11-10 | Creación del roadmap maestro, prompts, bitácoras, escenarios de adaptación y protocolo multi-IA | Luis David / Microsoft Copilot |

---

# 20. Fuente académica de requisitos

Este roadmap fue alineado con el archivo **“Contenido esperado del reporte Proyecto Integrador.docx”**, que solicita documentar el planteamiento, los datos, el preprocesamiento, el análisis exploratorio, los modelos, su comparación, el desarrollo matemático de al menos dos modelos, los resultados, las limitaciones, las conclusiones, el trabajo futuro y las referencias. También contempla un reporte en PDF y código en notebooks de Jupyter o scripts de Python, con GitHub como recomendación opcional.

---

## Nota final

Este documento no busca congelar desde ahora una solución. Su función es evitar que los cambios inevitables producidos por la disponibilidad, calidad y naturaleza de los datos destruyan la trazabilidad del proyecto. El roadmap debe adaptarse, pero cada adaptación deberá indicar qué cambió, por qué cambió, qué evidencia la justificó y qué consecuencias tiene para las conclusiones.
