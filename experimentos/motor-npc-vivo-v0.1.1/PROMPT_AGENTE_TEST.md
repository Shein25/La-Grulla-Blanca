# Encargo para agente externo — Retest 2 Motor NPC Vivo v0.1.1

Audita exclusivamente la **cabeza actual** de:

`experiment/motor-npc-v0.1.1`

directorio:

`experimentos/motor-npc-vivo-v0.1.1/`

No reutilices como resultado el informe del commit `946fd177fa443601233a1be767a4bbaed71bdfc0`: desde entonces se corrigió el hueco de propiedades heredadas.

NO modifiques el juego de producción.
NO integres nada en `grulla-blanca_ver73.html`.
NO conviertas fixtures ficticios en NPC canónicos.
NO ajustes pesos.

## 1. Regresión completa

Ejecuta:

```bash
node tests.mjs
```

Reporta PASS/FAIL y exit code.

## 2. Stress reproducible

Ejecuta:

```bash
node stress.mjs 10000 1337
node stress.mjs 10000 1
node stress.mjs 10000 42
node stress.mjs 10000 999
node stress.mjs 10000 20260923
```

Confirma que el preflight adversarial también pasa.

## 3. Reproducciones obligatorias del hallazgo anterior

Prueba explícitamente como valores de conocimiento:

```text
toString
constructor
__proto__
```

en:

- `npc.knowledge.R1`;
- `context.relevantKnowledge`.

Todos deben ser rechazados antes de puntuar.

Prueba como `topicId`:

```text
toString
constructor
__proto__
R99
```

Todos deben lanzar rechazo de tema no definido y nunca producir `NaN`.

## 4. Propiedades heredadas

Construye:

```js
Object.create(BASE_CONTEXT)
```

y un contexto de diálogo cuyos tres campos existan sólo en el prototipo.

Ambos deben ser rechazados.

Intenta también un NPC o subobjeto construido con un prototipo ajeno. Debe rechazarse o quedar demostrado que no puede saltarse la validación de propiedades propias.

## 5. Finitud

Busca activamente cualquier entrada que **pase los validadores** y luego genere:

- `NaN`;
- `Infinity`;
- `-Infinity` en una acción disponible;
- disclosure no finito.

Si encontrás una, entrega reproducción mínima.

## 6. No-regresión

Repite y confirma:

- B1 de campos faltantes;
- B2 de independencia profunda;
- score → raw → ACTION_ORDER;
- inercia +6 → +4 → +2 → +0;
- dutyMode exclusivo;
- `rutina_trabajo → trabajar`;
- `espera_sin_tarea → esperar`;
- las tres personalidades siguen diferenciadas;
- DESCONOCIDO nunca revela;
- SOSPECHA nunca COMPARTE.

## 7. Preparación para GOAP

Evalúa si, una vez cerrada la validación, la arquitectura puede mantener esta separación:

```text
Utility AI → selecciona OBJETIVO
GOAP       → construye PLAN
Executor   → aplica acciones y verifica efectos
```

No implementes GOAP.

## Entregable

Devuelve únicamente:

`Informe_Test_Motor_NPC_Vivo_v0.1.1_RETEST2.md`

Termina con exactamente uno:

`V011_APTO_PARA_GOAP`

`V011_REQUIERE_CORRECCIONES`

`V011_FALLO_CONCEPTUAL`
