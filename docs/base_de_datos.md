# Base de datos

> **Estado:** ✅ auditada (notebook `01_data_audit`). Puerta de datos: 🟢 **VERDE**.

## La idea clave

Para medir movilidad social necesitamos **dos fotos de la misma persona**:

| Foto | Pregunta que responde | En la EMOVI |
|---|---|---|
| **Origen** | ¿Cómo vivía a los 14 años? | Bienes y servicios del hogar, escolaridad y ocupación de los padres, tipo de localidad, región |
| **Destino** | ¿Cómo vive hoy de adulto(a)? | Bienes y servicios del hogar actual, escolaridad, ocupación, ingreso |

## Fuentes recibidas

| Fuente | Archivo en el repo | Qué tiene | Uso |
|---|---|---|---|
| **ESRU-EMOVI 2023** (CEEY) | `data/esru_emovi.zip` | 17,843 personas de 25 a 64 años, 296 variables, factor de expansión y diseño muestral | ✅ **Fuente principal** |
| **CONEVAL 2022** | Release `base-datos-Coneval` → `pobreza_22.dta` | Medición de pobreza por persona (construida con la ENIGH 2022) | Pobreza por estado (contexto) |
| **ENOE 2022** (INEGI) | Release `Enoe-INEGI` → 4 trimestres | Encuesta de empleo | Informalidad laboral por estado (contexto) |
| **ENIGH 2022** (INEGI) | `data/enigh2022_ns_*.zip` (7 tablas) | Ingresos y gastos de hogares | No se procesa aparte: ya está incluida en CONEVAL (decisión D03) |

**Importante:** estas encuestas **no se pueden unir persona por persona**, porque no comparten identificadores. CONEVAL y ENOE solo se usan resumidas por estado.

## Calidad de los datos (resumen)

| Revisión | Resultado |
|---|---|
| Folios duplicados | 0 |
| Bienes a los 14 años con "No sabe" | < 5% por variable |
| Escolaridad del padre / madre faltante | 19% / 10%. Se conserva como categoría "No sabe / ausente" |
| Ocupación actual faltante | 33% (no trabaja). No se usa como predictor |
| Validación con cifras oficiales | Pobreza nacional 36.3% y pobreza extrema 7.1%. ✅ Coinciden con lo publicado por CONEVAL para 2022 |

## Cómo reproducir

```text
data/
├── esru_emovi.zip, enigh2022_*.zip   ← subidos al repo
└── raw/                              ← aquí se descomprimen (no se suben a GitHub)
    ├── esru_emovi/Data/entrevistado_2023.dta
    ├── coneval/pobreza_22.dta        ← descargar del Release "base-datos-Coneval"
    └── enoe/*.zip                    ← descargar del Release "Enoe-INEGI" (sin descomprimir)
```

```bash
unzip data/esru_emovi.zip -d data/raw/esru_emovi
```

Las tablas procesadas se generan en `data/processed/` al ejecutar los notebooks 01 y 02.
