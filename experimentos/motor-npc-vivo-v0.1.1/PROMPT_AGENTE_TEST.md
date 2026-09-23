# Encargo para agente externo — Retest Motor NPC Vivo v0.1.1

Audita exclusivamente:

`experimentos/motor-npc-vivo-v0.1.1/`

La v0.1 original debe permanecer como referencia histórica.

NO modifiques el juego de producción.
NO integres nada en `grulla-blanca_ver73.html`.
NO conviertas fixtures ficticios en NPC canónicos.
NO ajustes pesos durante la auditoría.

## 1. Regresión

Ejecuta:

```bash
node tests.mjs
```

Confirma el número exacto de PASS/FAIL.

## 2. Stress

Ejecuta:

```bash
node stress.mjs 10000 1337
node stress.mjs 10000 1
node stress.mjs 10000 42
node stress.mjs 10000 999
node stress.mjs 10000 20260923
```

Reporta distribución exacta de acciones para cada seed.

## 3. Reproducir los bugs de v0.1

### B1
Intenta eliminar individualmente:

- un trait obligatorio;
- una dimensión de relationPlayer;
- R1/R2/R3;
- behaviorState;
- un campo obligatorio de contexto.

La entrada incompleta debe ser rechazada antes de puntuar.

### B2
Genera `nextNpc` con `simulateTurn()` y modifica después:

- `nextNpc.traits`;
- `nextNpc.relationPlayer`;
- `nextNpc.knowledge`;
- `nextNpc.behaviorState`.

El NPC original debe quedar byte-equivalente a su snapshot anterior.

## 4. Empates y clamp

Busca contextos con varias acciones en score 100.

Comprueba que:

1. mayor `raw` gana;
2. `ACTION_ORDER` sólo decide si score y raw son iguales;
3. resultado sigue siendo determinista.

## 5. Inercia

Comprueba la secuencia:

```text
+6 → +4 → +2 → +0
```

y busca si existe algún mecanismo residual capaz de mantener artificialmente una acción sólo por inercia durante tiempo indefinido.

Distingue entre:

- seguir haciendo algo porque su utilidad real continúa siendo mayor;
- seguir haciéndolo sólo por inercia.

## 6. dutyMode

Verifica:

- `vigilar` sólo disponible con dutyMode=vigilar;
- `trabajar` sólo disponible con dutyMode=trabajar;
- `patrullar` sólo disponible con dutyMode=patrullar;
- con dutyMode=ninguno las tres quedan bloqueadas;
- dutyMode inválido se rechaza.

Evalúa también si esta decisión conceptual es razonable como futura precondición de planner.

## 7. Casos de aceptación

Los escenarios:

- `rutina_trabajo` debe permitir que trabajar gane;
- `espera_sin_tarea` debe permitir que esperar gane;
- las tres personalidades deben seguir diferenciándose en la misma situación.

No juzgues calidad por uniformidad estadística de las nueve acciones.

## 8. Conocimiento

Repite pruebas adversariales de:

- DESCONOCIDO → nunca revela;
- SOSPECHA → nunca COMPARTE;
- SABE / CONFIRMADO condicionados por vínculo, rango y restricciones.

## 9. Arquitectura

Evalúa específicamente si v0.1.1 está lista para que v0.2 agregue:

```text
Utility AI → selecciona OBJETIVO
GOAP       → construye PLAN
executor   → ejecuta acciones
```

sin fusionar todavía esas tres responsabilidades.

## Entregable

Devuelve únicamente:

`Informe_Test_Motor_NPC_Vivo_v0.1.1.md`

Termina con exactamente uno:

`V011_APTO_PARA_GOAP`

`V011_REQUIERE_CORRECCIONES`

`V011_FALLO_CONCEPTUAL`
