# Encargo para agente externo — Retest 4 Motor NPC Vivo v0.1.1

Audita exclusivamente la **cabeza actual** de la rama:

`experiment/motor-npc-v0.1.1`

Directorio:

`experimentos/motor-npc-vivo-v0.1.1/`

NO reutilices resultados de commits anteriores.
NO modifiques el juego principal.
NO toques `grulla-blanca_ver73.html`.
NO ajustes pesos.
NO implementes GOAP.
NO hagas merge.

## 1. Regresión oficial

Ejecuta:

```bash
node tests.mjs
```

La candidata actual declara 37 llamadas de test y el bloque de fixtures corre para tres NPC, por lo que se esperan **39 ejecuciones PASS** y exit code 0.

Si el número difiere, informa el número real y explica por qué.

## 2. Stress

Ejecuta:

```bash
node stress.mjs 10000 1337
node stress.mjs 10000 1
node stress.mjs 10000 42
node stress.mjs 10000 999
node stress.mjs 10000 20260923
```

Confirma que el preflight pasa antes del bucle y que las cinco corridas terminan con exit code 0.

## 3. Reproducción obligatoria del hallazgo de Retest 3

Prueba propiedades propias de datos con valor `undefined` en todos estos grupos:

### NPC top-level
- id
- name
- role
- traits
- relationPlayer
- knowledge
- behaviorState

### NPC internos
- al menos un trait
- al menos una relación
- R1
- behaviorState.lastAction
- behaviorState.consecutiveTurns

### Contexto de acción
Los 11 campos:
- playerPresent
- playerRequestsHelp
- playerRank
- dutyImportance
- danger
- missionUrgency
- anomalyPresent
- awayFromPost
- superiorReachable
- relevantKnowledge
- dutyMode

### Contexto de diálogo
- playerRank
- topicSensitivity
- formalRestriction

Requisito: todos deben ser rechazados por el validador y por la API pública **antes del cálculo**.

No debe existir ningún score, raw o disclosure `NaN`/infinito proveniente de una entrada aceptada.

## 4. No regresión de accessors

Repite al menos:

- getter mutable;
- setter-only;
- getter+setter;
- accessor no enumerable;

en knowledge, contexto y un campo numérico.

Los accessors deben seguir rechazados sin ejecutar getter/setter.

## 5. No regresión de propiedades heredadas

Repite:

- `toString`;
- `constructor`;
- `__proto__`;

como knowledge y relevantKnowledge.

Repite topicId:
- `toString`;
- `constructor`;
- `__proto__`;
- `R99`.

Repite `Object.create(...)`.

Todo debe seguir rechazado.

## 6. Finitud adversarial

Busca activamente cualquier entrada que:

1. pase `validateNpc` / `validateActionContext` / `validateDialogueContext`;
2. después produzca score/raw/disclosure no finito o una excepción tardía por datos obligatorios inválidos.

Si existe, entrega reproducción mínima.

Incluye explícitamente:

- `undefined`;
- `null`;
- `NaN`;
- `Infinity`;
- `-Infinity`;
- cadenas donde se esperan números/booleanos;
- arrays donde se esperan objetos;
- objetos con prototipo ajeno;
- accessors.

## 7. No regresión funcional

Confirma:

- `nextNpc` profundamente independiente;
- score → raw → ACTION_ORDER;
- inercia +6 → +4 → +2 → +0;
- dutyMode exclusivo;
- `rutina_trabajo → trabajar`;
- `espera_sin_tarea → esperar`;
- Disciplinado → vigilar;
- Leal → ayudar_jugador;
- Curioso → investigar;
- DESCONOCIDO nunca revela;
- SOSPECHA nunca COMPARTE.

## 8. Preparación para GOAP

Evalúa si ya puede congelarse v0.1.1 como base experimental para:

```text
Utility AI → selecciona OBJETIVO
GOAP       → construye PLAN
Executor   → aplica acciones y verifica efectos
```

No implementes GOAP todavía.

## Entregable

Devuelve únicamente:

`Informe_Test_Motor_NPC_Vivo_v0.1.1_RETEST4.md`

Termina con exactamente uno:

`V011_APTO_PARA_GOAP`

`V011_REQUIERE_CORRECCIONES`

`V011_FALLO_CONCEPTUAL`
