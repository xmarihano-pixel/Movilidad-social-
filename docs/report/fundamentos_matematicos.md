# Fundamentos matemáticos

El roadmap y la rúbrica piden el desarrollo matemático de **al menos dos modelos**. Aquí están el índice de riqueza (PCA), la regresión logística (modelo elegido) y random forest (el mejor modelo no lineal).

## 0. Índice de riqueza: análisis de componentes principales (PCA)

Sea $X \in \mathbb{R}^{n \times p}$ la matriz de bienes (1 = tiene, 0 = no tiene), estandarizada por columna: $Z_{ij} = (X_{ij} - \bar{x}_j)/s_j$.

La matriz de covarianzas es $\Sigma = \frac{1}{n-1} Z^\top Z$. El primer componente principal es el vector $v_1$ que maximiza la varianza de la proyección:

$$v_1 = \arg\max_{\lVert v \rVert = 1} \; v^\top \Sigma v \quad\Rightarrow\quad \Sigma v_1 = \lambda_1 v_1$$

es decir, el eigenvector del eigenvalor más grande. El índice de cada persona es $s_i = z_i^\top v_1$. El signo se orienta para que más bienes den un índice mayor.

En la EMOVI, el primer componente explica 21.6% de la varianza en el origen y 15.6% en el destino. Es lo esperado con decenas de variables binarias.

**Quintil ponderado:** las personas se ordenan por $s_i$ dentro de su cohorte y se acumulan los factores de expansión $w_i$. El quintil es $q_i = \lceil 5 \cdot \sum_{k \le i} w_k / \sum_k w_k \rceil$.

## 1. Regresión logística (modelo elegido)

**Modelo.** Para la persona $i$ con vector de circunstancias $x_i$:

$$P(y_i = 1 \mid x_i) = \sigma(\beta_0 + x_i^\top \beta) = \frac{1}{1 + e^{-(\beta_0 + x_i^\top \beta)}}$$

donde $y_i = 1$ si sigue en Q1.

**Momios y razón de momios.** Los log-momios son lineales:

$$\log \frac{p_i}{1 - p_i} = \beta_0 + x_i^\top \beta$$

Si $x_{ij}$ aumenta en 1, los momios se multiplican por $e^{\beta_j}$. Esa es la **razón de momios** que se reporta en el notebook 06.

**Estimación.** Se maximiza la log-verosimilitud penalizada (regularización L2, $C = 0.5$):

$$\ell(\beta) = \sum_{i=1}^{n} \left[ y_i \log p_i + (1 - y_i) \log(1 - p_i) \right] - \frac{1}{2C} \lVert \beta \rVert_2^2$$

El gradiente es $\nabla \ell = X^\top (y - p) - \beta / C$. La función es cóncava, así que tiene un único máximo; se resuelve con L-BFGS.

**Versión explicativa (inferencia).** Se usa un GLM binomial con pesos $w_i$ normalizados y errores estándar robustos agrupados por UPM (unidad primaria de muestreo), que respetan el diseño de la encuesta:

$$\widehat{V}(\hat\beta) = (X^\top W X)^{-1} \left( \sum_{g} X_g^\top \hat{u}_g \hat{u}_g^\top X_g \right) (X^\top W X)^{-1}$$

**Supuestos:** relación lineal en los log-momios, observaciones independientes entre UPM y ausencia de multicolinealidad perfecta. Esto último es la razón de la decisión D16.

## 2. Random forest

**Árbol de clasificación.** Un árbol divide el espacio de variables en regiones $R_m$. En cada nodo elige la variable $j$ y el corte $t$ que más reducen la impureza de Gini:

$$G(R) = \sum_{k \in \{0,1\}} \hat{p}_k (1 - \hat{p}_k), \qquad \Delta = G(R) - \frac{|R_L|}{|R|} G(R_L) - \frac{|R_R|}{|R|} G(R_R)$$

**Bosque.** Se entrenan $B = 400$ árboles. Cada uno usa:
1. una muestra *bootstrap* de los datos (*bagging*);
2. en cada corte, solo un subconjunto aleatorio de $\sqrt{p}$ variables (decorrelación).

La predicción es el promedio de las probabilidades de los árboles:

$$\hat{p}(x) = \frac{1}{B} \sum_{b=1}^{B} \hat{p}_b(x)$$

**¿Por qué funciona?** Si cada árbol tiene varianza $\sigma^2$ y la correlación entre árboles es $\rho$, la varianza del promedio es

$$\rho \sigma^2 + \frac{1 - \rho}{B} \sigma^2$$

Promediar reduce la varianza, y elegir variables al azar reduce $\rho$.

**Hiperparámetros:** `min_samples_leaf = 20`, para evitar hojas de muy pocas personas y el sobreajuste.

## 3. Métricas

- **AUC:** probabilidad de que el modelo asigne mayor riesgo a una persona que sí sigue en Q1 que a una que no, ambas elegidas al azar. 0.5 = azar.
- **Brier:** $\frac{1}{n} \sum_i (\hat{p}_i - y_i)^2$. Mide la calibración; menor es mejor.
- **Exactitud balanceada:** promedio de la sensibilidad y la especificidad.
- **Importancia por permutación:** caída del AUC en el conjunto de prueba al revolver al azar una variable. Mide cuánto *usa* el modelo esa variable, no su efecto causal.
