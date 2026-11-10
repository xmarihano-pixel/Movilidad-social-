# Base de datos

> **Estado:** provisional. Nada de esto está confirmado hasta hacer la auditoría de datos (Fase 3 del roadmap).

## ¿Qué necesitamos que tenga la base?

Para medir movilidad social necesitamos **dos fotos de la misma persona**:

| Foto | Pregunta que responde | Ejemplo |
|---|---|---|
| **Origen** | ¿Cómo vivía cuando era niño(a)? | Escolaridad de los padres, bienes en casa a los 14 años |
| **Destino** | ¿Cómo vive hoy de adulto(a)? | Su escolaridad, ocupación, ingreso o bienes actuales |

Si la base solo tiene la foto de **hoy**, no podemos hablar de movilidad: solo de desigualdad.

## Fuentes candidatas

| Fuente | Quién la hace | ¿Tiene origen y destino? | Uso en el proyecto |
|---|---|---|---|
| **Encuesta ESRU de Movilidad Social (ESRU-EMOVI)** | Centro de Estudios Espinosa Yglesias (CEEY) | Sí, con preguntas retrospectivas | **Fuente principal** (por verificar) |
| ENIGH | INEGI | No, solo situación actual | Contexto de ingreso y gasto |
| ENOE | INEGI | No, solo situación actual | Contexto de empleo e informalidad |
| Medición de pobreza | CONEVAL | No (datos por estado y municipio) | Contexto territorial |

**Importante:** estas encuestas **no se pueden unir persona por persona**, porque no comparten identificadores. Solo se pueden combinar por estado o región.

## Dónde guardar los datos

```text
data/
├── raw/        ← archivos originales tal cual se descargan (nunca se editan)
├── interim/    ← versiones intermedias mientras se limpian
├── processed/  ← la tabla final lista para los modelos
└── external/   ← datos de contexto (CONEVAL, INEGI por estado, etc.)
```

Los datos **no se suben a GitHub** (están en `.gitignore`). Cada persona los descarga de la fuente oficial.

## Pendientes

- [ ] Confirmar qué edición de la ESRU-EMOVI usaremos y cómo se obtiene.
- [ ] Descargar el cuestionario y el diccionario oficial.
- [ ] Llenar la auditoría en `notebooks/01_data_audit.ipynb`.
- [ ] Decidir la puerta de datos: 🟢 VERDE, 🟡 AMARILLO o 🔴 ROJO.
