# Encargo para agente externo — Retest 3 Motor NPC Vivo v0.1.1

Audita exclusivamente la **cabeza actual** de la rama:

`experiment/motor-npc-v0.1.1`

Directorio:

`experimentos/motor-npc-vivo-v0.1.1/`

NO reutilices los resultados de los commits anteriores.
NO modifiques el juego de producción.
NO toques `grulla-blanca_ver73.html`.
NO ajustes pesos.
NO implementes GOAP.

## 1. Regresión completa

Ejecuta:

```bash
node tests.mjs
```

Reporta PASS/FAIL exacto y exit code.

## 2. Stress reproducible

Ejecuta:

```bash
node stress.mjs 10000 1337
node stress.mjs 10000 1
node stress.mjs 10000 42
node stress.mjs 10000 999
node stress.mjs 10000 20260923
```

Confirma que el preflight de propiedades heredadas y getters mutables pasa antes de cada corrida.

## 3. Reproducir obligatoriamente el hallazgo del Retest 2

Crea getters mutables en:

- `npc.knowledge.R1`;
- `context.relevantKnowledge`;
- un trait numérico;
- un campo numérico de contexto;
- un campo estructural del NPC, por ejemplo `traits`;
- un campo del contexto de diálogo.

Los getters pueden devolver primero un valor válido y después:

- `toString`;
- `constructor`;
- `NaN`.

Requisitos:

1. el validador debe rechazarlos;
2. la API pública debe lanzar antes de puntuar/revelar;
3. el getter no debe ser ejecutado durante la validación;
4. no debe aparecer `NaN` ni disclosure no finito.

## 4. Accessors adicionales

Prueba también:

- setter-only;
- getter+setter;
- accessor no enumerable si reemplaza un campo obligatorio;
- accessor en `behaviorState.lastAction`;
- accessor en `relationPlayer.confianza`;
- accessor en `topicSensitivity`.

Todo campo consumido por el motor debe ser una **propiedad propia de datos**.

## 5. Propiedades heredadas — no regresión

Repite:

- `toString`;
- `constructor`;
- `__proto__`;

como estados de conocimiento y `relevantKnowledge`.

Repite `topicId`:

- `toString`;
- `constructor`;
- `__proto__`;
- `R99`.

Repite contextos creados con `Object.create(...)`.

Todos deben seguir rechazados.

## 6. Finitud

Busca activamente una entrada que **pase todos los validadores** y después produzca:

- score `NaN`;
- raw `NaN`;
- score/raw infinito en una acción disponible;
- disclosure `NaN` o infinito.

Si encontrás una, entrega reproducción mínima.

## 7. No regresión funcional

Confirma:

- campos faltantes rechazados;
- `nextNpc` profundamente independiente;
- score → raw → ACTION_ORDER;
- inercia +6 → +4 → +2 → +0;
- `dutyMode`;
- `rutina_trabajo → trabajar`;
- `espera_sin_tarea → esperar`;
- Disciplinado / Leal / Curioso siguen diferenciándose;
- DESCONOCIDO nunca revela;
- SOSPECHA nunca COMPARTE.

## 8. Preparación para GOAP

Evalúa si, con el contrato de entrada cerrado, es razonable pasar a:

```text
Utility AI → selecciona OBJETIVO
GOAP       → construye PLAN
Executor   → aplica acciones y verifica efectos
```

No implementes esas capas todavía.

## Entregable

Devuelve únicamente:

`Informe_Test_Motor_NPC_Vivo_v0.1.1_RETEST3.md`

Termina con exactamente uno:

`V011_APTO_PARA_GOAP`

`V011_REQUIERE_CORRECCIONES`

`V011_FALLO_CONCEPTUAL`
