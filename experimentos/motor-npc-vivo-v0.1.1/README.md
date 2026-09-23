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

## Retest 2 — hardening de propiedades propias

El primer retest de v0.1.1 confirmó las correcciones de esquema incompleto, snapshots, clamp/raw, inercia y dutyMode, pero detectó que JavaScript permitía valores heredados como `toString` y `constructor` mediante el operador `in`.

La candidata actual de esta rama corrige ese hueco:

- estados de conocimiento se validan contra una lista cerrada;
- los campos obligatorios del contexto deben ser propiedades propias;
- los contextos con prototipo ajeno se rechazan;
- `topicId` debe ser propiedad propia de `knowledge`;
- el contexto de diálogo exige sus tres propiedades propias;
- la suite incorpora casos negativos para `toString`, `constructor`, `__proto__`, temas inexistentes y objetos con campos sólo heredados;
- el stress incorpora un preflight de estas condiciones.

La suite contiene ahora **30 ejecuciones de prueba** (28 bloques declarados, con el bloque de fixtures ejecutándose para tres NPC). Este número describe la suite; el resultado definitivo debe obtenerlo el retest externo de la nueva cabeza de rama.

## Retest 3 — registros de datos sin accessors

El segundo retest confirmó el hardening contra propiedades heredadas, pero encontró que una propiedad **propia** implementada como getter podía cambiar entre validación y uso y producir `NaN`.

La cabeza actual endurece el contrato: los NPC y contextos aceptados por el motor deben ser **registros de datos**, no objetos con accessors en los campos consumidos.

Se añadió:

- lectura de validación mediante `Object.getOwnPropertyDescriptor()`, sin ejecutar getters;
- rechazo explícito de getters/setters en campos top-level del NPC;
- rechazo de accessors en traits, vínculos, knowledge y behaviorState;
- rechazo de accessors en todos los campos obligatorios del contexto de acción;
- rechazo de accessors en contexto de diálogo;
- pruebas negativas de getters mutables;
- comprobación de que los getters rechazados ni siquiera sean ejecutados;
- preflight de getters mutables en cada stress run.

No se modificaron pesos, reglas sociales, `dutyMode`, desempate, inercia ni las tres personalidades.

## Próximo paso

**No mergear todavía.** Ejecutar el Retest 3 indicado en `PROMPT_AGENTE_TEST.md`.

Sólo si el informe termina en `V011_APTO_PARA_GOAP`, considerar el merge y diseñar v0.2 como GOAP experimental.
