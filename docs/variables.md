# Variables

> **Estado:** lista de trabajo. Son las variables que **esperamos** encontrar. Los nombres reales se llenarán cuando tengamos el diccionario oficial de la base.

## 1. Variable objetivo (lo que queremos explicar)

| Variable | Qué mide | Tipo | Opciones |
|---|---|---|---|
| `movilidad` | Si la persona subió, se quedó o bajó respecto a su hogar de origen | Categórica | Ascenso / Permanencia / Descenso |
| `posicion_destino` | Posición socioeconómica actual (por ejemplo, quintil 1 a 5) | Ordinal | 1 (más bajo) a 5 (más alto) |

La forma exacta de medirla se decide en la Fase 2 y **se congela antes de ver resultados**.

## 2. Origen (cómo vivía la persona a los 14 años)

| Variable | Qué mide | Tipo |
|---|---|---|
| `escolaridad_padre` | Años o nivel de estudio del padre | Ordinal |
| `escolaridad_madre` | Años o nivel de estudio de la madre | Ordinal |
| `ocupacion_padre` | Tipo de trabajo del padre o principal proveedor | Categórica |
| `bienes_hogar_origen` | Índice de bienes y servicios en casa (luz, agua, auto, etc.) | Numérica |
| `tamano_hogar_origen` | Número de personas en el hogar | Numérica |
| `localidad_origen` | Rural o urbana | Categórica |
| `region_origen` | Región o estado donde creció | Categórica |

## 3. Destino (cómo vive hoy)

| Variable | Qué mide | Tipo |
|---|---|---|
| `escolaridad` | Años o nivel de estudio de la persona | Ordinal |
| `ocupacion` | Tipo de trabajo actual | Categórica |
| `bienes_hogar_actual` | Índice de bienes y servicios en su casa actual | Numérica |
| `ingreso` | Ingreso del hogar o personal (si existe) | Numérica |

## 4. Características de la persona

| Variable | Qué mide | Tipo |
|---|---|---|
| `sexo` | Sexo | Categórica |
| `edad` | Edad en años | Numérica |
| `lengua_indigena` | Habla o sus padres hablaban lengua indígena | Binaria |
| `tono_piel` | Tono de piel (escala de la encuesta, si existe) | Ordinal |
| `region_actual` | Región o estado donde vive hoy | Categórica |

## 5. Técnicas (no son para el modelo)

| Variable | Para qué sirve |
|---|---|
| `id` | Identificar a cada persona |
| `factor_expansion` | Ponderador para que los resultados representen a la población |

## Reglas

- ⚠️ Variables como `sexo`, `lengua_indigena` o `tono_piel` son **sensibles**: se usan para medir desigualdad, no para juzgar personas.
- ⚠️ Las variables de **destino** no pueden usarse para predecir la movilidad (sería hacer trampa: *leakage*).
- Cada cambio a esta lista se anota en `docs/decisions/`.
