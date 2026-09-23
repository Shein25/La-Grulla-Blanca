# Motor NPC Vivo v0.1.1 — Laboratorio

Iteración correctiva de v0.1 basada en la auditoría externa `V01_REQUIERE_CORRECCIONES`.

## Regla de seguridad

Este directorio es **experimental**.

No se importa desde `grulla-blanca_ver73.html`, no modifica el baseline, no usa los 32 NPC canónicos y no implementa GOAP todavía.

La carpeta `motor-npc-vivo-v0.1/` se conserva intacta como referencia histórica.

## Qué corrige v0.1.1

### B1 — esquema estricto

`validateNpc()` ya no acepta estructuras incompletas.

Exige:

- seis rasgos: disciplina, sociabilidad, curiosidad, prudencia, lealtad_institucional, empatía;
- seis dimensiones de vínculo: afinidad, confianza, respeto, deuda, temor, rivalidad;
- R1, R2 y R3;
- `behaviorState.lastAction` y `behaviorState.consecutiveTurns`.

También existe `validateActionContext()` para validar rango, booleanos, magnitudes 0..100, conocimiento relevante y deber actual.

### B2 — snapshots independientes

`simulateTurn()` usa clonado profundo para producir `nextNpc`.

Modificar el resultado no puede modificar el estado anterior.

### Empates a 100

La prioridad ahora es:

```text
score visible
   ↓ empate
raw sin clamp
   ↓ empate
ACTION_ORDER
```

El clamp sirve para presentación, pero ya no destruye diferencias internas.

### Inercia con decaimiento

La inercia ya no es +6 perpetuo.

```text
repetición 1 → +6
repetición 2 → +4
repetición 3 → +2
repetición 4+ → +0
```

Si una acción sigue ganando después, lo hace por su utilidad real, no por quedar atrapada en el bono.

### Deber explícito

Se incorporó `dutyMode`:

- `vigilar`
- `trabajar`
- `patrullar`
- `ninguno`

Las tres acciones de deber sólo compiten cuando ese deber existe realmente. Esto evita resolver la baja frecuencia de `trabajar` inflando pesos artificialmente y prepara el concepto de precondiciones para una futura capa GOAP.

## Pruebas locales previas a revisión externa

Ejecutadas antes de subir la candidata:

```bash
node tests.mjs
node stress.mjs 10000 1337
node stress.mjs 10000 1
node stress.mjs 10000 42
node stress.mjs 10000 999
node stress.mjs 10000 20260923
```

Resultado local:

- **26/26 PASS**
- cinco stress de 10.000 casos: PASS
- 0 fallos de determinismo o conocimiento.

Distribución aproximada observada por 10.000 casos:

- informar_superior: ~4.1k
- investigar: ~1.4k
- regresar_puesto: ~1.1–1.2k
- hablar_jugador: ~1.0k
- ayudar_jugador: ~0.9k
- vigilar: ~0.65k
- trabajar: ~0.24–0.30k
- patrullar: ~0.19–0.21k
- esperar: ~0.11–0.13k

No se interpreta esa distribución como objetivo de balance.

## Archivos

- `engine.mjs` — Utility AI y validadores.
- `npc-fixtures.mjs` — tres personalidades ficticias.
- `scenarios.mjs` — escenarios controlados, incluidos trabajo y espera.
- `tests.mjs` — 26 pruebas.
- `stress.mjs` — stress reproducible.
- `simulator.html` — visor interactivo.
- `PROMPT_AGENTE_TEST.md` — encargo para auditoría externa.
- `CAMBIOS_v0.1.1.md` — trazabilidad de correcciones.

## Qué NO hace aún

- no planifica rutas;
- no tiene GOAP;
- no tiene memoria episódica;
- no simula relaciones NPC↔NPC;
- no transmite conocimiento entre NPC;
- no genera diálogo textual;
- no usa datos canónicos de producción.

## Próximo paso

Sólo si la auditoría externa aprueba v0.1.1, diseñar v0.2 como **GOAP experimental**, manteniendo Utility AI para elegir objetivos y un planner separado para decidir cómo alcanzarlos.
