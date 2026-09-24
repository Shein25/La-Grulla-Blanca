# Encargo para agente externo — Retest 5 Motor NPC Vivo v0.1.1

Audita exclusivamente la **cabeza actual** de:

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

La cabeza actual declara 42 llamadas a `test()`; el bloque de fixtures corre para tres NPC, por lo que se esperan **44 ejecuciones PASS** y exit code 0.

Si el número real difiere, informa y explica.

## 2. Stress

Ejecuta:

```bash
node stress.mjs 10000 1337
node stress.mjs 10000 1
node stress.mjs 10000 42
node stress.mjs 10000 999
node stress.mjs 10000 20260923
```

El preflight debe incluir propiedades heredadas, accessors, undefined y Proxy.

## 3. Reproducir obligatoriamente el hallazgo de Retest 4

Crea Proxies sobre objetos cuyos descriptores de datos sean válidos pero cuyo trap `get` devuelva valores distintos.

Prueba como mínimo:

### Contexto de acción
- `missionUrgency → NaN`
- `danger → NaN`
- un trap `get` que lance excepción

### Contexto de diálogo
- `topicSensitivity → NaN`

### NPC
- `traits.disciplina → NaN`
- `traits.disciplina` con trap que lance
- `behaviorState.consecutiveTurns → -Infinity`

Requisitos:

- la API nunca debe devolver score/raw/disclosure no finito;
- si el descriptor capturado es válido, el cálculo debe usar ese valor capturado y no ejecutar el trap `get`;
- si el descriptor entregado a la propia llamada de la API es inválido, la API debe rechazar antes del cálculo;
- `simulateTurn()` debe construir `nextNpc` desde el snapshot validado y no fallar al clonar un Proxy.

## 4. Descriptor dinámico entre llamadas

Construye un Proxy cuyo `getOwnPropertyDescriptor`:

1. entregue un valor válido a una llamada externa de `validateActionContext()`;
2. entregue `NaN` cuando después se llame a `chooseAction()`.

Resultado esperado: la segunda llamada debe volver a capturar/validar y rechazar. Una validación externa previa no debe actuar como autorización permanente.

Prueba el mismo principio con NPC o diálogo si resulta útil.

## 5. Confirmar frontera snapshot

Audita el código para verificar que, tras materializar el snapshot:

- Utility AI no vuelva a leer valores de negocio desde el input original;
- diálogo no vuelva a leer el contexto/NPC original;
- `simulateTurn()` no use `structuredClone(inputProxy)`;
- `nextNpc` provenga del snapshot plano;
- los snapshots no compartan referencias anidadas con el input.

## 6. Barrera de finitud

Busca una entrada aceptada por la propia llamada de API que consiga producir:

- score `NaN`;
- raw `NaN`;
- score/raw infinito en una acción disponible;
- disclosure/raw no finito;
- excepción tardía por un trap `get`.

Incluye Proxies, getters/setters, undefined, null, NaN, Infinity, prototipos ajenos y tipos incorrectos.

Si encontrás una reproducción, documentala.

## 7. No regresión completa

Confirma además:

- undefined rechazado en los 26 campos ya auditados;
- accessors rechazados sin ejecutarse;
- `toString`, `constructor`, `__proto__` y `R99` rechazados;
- campos heredados rechazados;
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

Evalúa si el contrato de frontera/snapshot ya permite congelar v0.1.1 como base experimental para:

```text
Utility AI → selecciona OBJETIVO
GOAP       → construye PLAN
Executor   → aplica acciones y verifica efectos
```

No implementes GOAP.

## Entregable

Devuelve únicamente:

`Informe_Test_Motor_NPC_Vivo_v0.1.1_RETEST5.md`

Termina exactamente con uno:

`V011_APTO_PARA_GOAP`

`V011_REQUIERE_CORRECCIONES`

`V011_FALLO_CONCEPTUAL`
