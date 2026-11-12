# Variables

> **Estado:** ✅ variables reales de la ESRU-EMOVI 2023, revisadas contra el diccionario oficial (`Diccionario ESRU EMOVI 2023.xlsx`). El código que las construye está en `src/data/emovi.py`.

## 1. Variable objetivo (lo que queremos explicar)

| Variable | Qué mide | Cómo se construye |
|---|---|---|
| `sigue_q1` ⭐ | Nació en el 20% más pobre **y** sigue en el 20% más pobre | `q_origen == 1` y `q_destino == 1` (sí = 1, no = 0) |
| `movilidad` | Subió, se quedó o bajó | Ascenso / Permanencia / Descenso según `q_destino − q_origen` |
| `q_origen` / `q_destino` | Quintil de riqueza (1 = 20% más pobre) | Quintiles ponderados del índice, dentro de cada cohorte |
| `indice_origen` / `indice_destino` | Riqueza del hogar | Primer componente principal de los bienes del hogar |

## 2. Origen (a los 14 años) → predictores

| Variable | Qué mide | Pregunta EMOVI |
|---|---|---|
| `indice_origen` | Riqueza del hogar a los 14 años | p25–p32 (45 bienes y servicios, piso, autos, cuartos) |
| `educ_madre`, `educ_padre` | Escolaridad de los padres (4 niveles + "No sabe / ausente") | educm, educp |
| `clase_padre` | Ocupación del principal sostén económico | clasep |
| `madre_trabajaba` | La madre trabajaba | p51 |
| `vivia_ambos_padres` | Vivía con mamá y papá | p39 |
| `sosten_madre` | La madre era el principal sostén | p40 |
| `personas_hogar_14`, `hacinamiento_14` | Tamaño del hogar y personas por cuarto | p22, p24 |
| `hermanos`, `orden_nacimiento` | Número de hermanos y lugar entre ellos | p57, p58 |
| `localidad_14` | Metrópoli … pueblo de menos de 2,500 habitantes | p21 |
| `region_14` | Norte, Norte-occidente, Centro-norte, Centro, Sur | region_14 |
| `o_p33a`…`o_p33h` | Servicios en el barrio (alumbrado, escuelas, salud, seguridad…) | p33 |

## 3. Características dadas de la persona → predictores

| Variable | Qué mide | Pregunta EMOVI |
|---|---|---|
| `mujer` | Sexo | sexo |
| `cohorte` | Grupo de edad (25-34, 35-44, 45-54, 55-64) | cohorte |
| `lengua_indigena` | Habla lengua indígena | p111 |
| `tono_piel` | Tono de piel autopercibido: Oscuro (A-E), Medio (F-G), Claro (H-K) | p112 |
| `autoadscripcion` | Se considera indígena, negra, blanca, mestiza… | p110 |

## 4. Destino y trayectoria → **no** son predictores del modelo principal

| Variable | Qué mide | Uso |
|---|---|---|
| `indice_destino` | Riqueza del hogar actual (p88–p99) | Construye el objetivo |
| `educ` | Escolaridad propia | Solo en el modelo de mediación |
| `migro_entidad` | Vive en otro estado que a los 14 | Solo en el modelo de mediación |
| `ingreso_pc`, `clase` | Ingreso per cápita y ocupación actual | Validación y robustez |

## 5. Técnicas

| Variable | Para qué sirve |
|---|---|
| `id` | Folio de la persona |
| `factor` | Factor de expansión: hace que los resultados representen a 60 millones de personas |
| `upm`, `estrato` | Diseño muestral, para calcular errores estándar correctos |

## 6. Contexto por estado (`data/processed/contexto_estatal_2022.csv`)

| Variable | Fuente |
|---|---|
| `pobreza_pct`, `pobreza_extrema_pct`, `ingreso_pc_mensual` | CONEVAL 2022 |
| `informalidad_pct` | ENOE 2022 (promedio de 4 trimestres) |

## Reglas
- ⚠️ `tono_piel`, `lengua_indigena` y `autoadscripcion` son **sensibles**: se usan para medir desigualdad, no para juzgar ni decidir sobre personas.
- ⚠️ Las variables de destino no entran al modelo principal (sería hacer trampa: *leakage*).
- Cada cambio queda registrado en `docs/decisions/bitacora_decisiones.md`.
