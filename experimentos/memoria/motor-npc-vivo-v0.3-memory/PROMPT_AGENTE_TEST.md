# Encargo para agente externo — Auditoría REV1 Motor NPC Vivo v0.3.0 MEMORIA

Audita exclusivamente la cabeza indicada de:

`experiment/motor-npc-v0.3-memory`

Directorio:

`experimentos/memoria/motor-npc-vivo-v0.3-memory/`

No modifiques el repositorio, producción, Utility AI ni GOAP.

## 1. Identificación obligatoria

Reporta:

- agente auditor;
- modelo/versión;
- fecha;
- rama;
- HEAD exacto;
- tipo de revisión.

## 2. Suite oficial

Ejecuta:

```bash
node tests.mjs
```

La candidata declara 23 tests.

Reporta PASS/FAIL reales y exit code.

## 3. Stress

Ejecuta al menos:

```bash
node stress.mjs 10000 1337
node stress.mjs 10000 1
node stress.mjs 10000 42
node stress.mjs 10000 999
node stress.mjs 10000 20260924
```

Confirma:

- determinismo con misma seed;
- `entries.length <= 32`;
- ausencia de keys duplicadas;
- ausencia de excepciones inesperadas.

## 4. Semántica obligatoria

Reproduce de forma independiente:

- upsert de misma key sin duplicación;
- `firstTurn` estable y `lastTurn` actualizado;
- rechazo si una key cambia `kind` o `subject`;
- rechazo de evento atrasado para la misma key;
- expiración inclusiva en `expiresTurn`;
- purga después de `expiresTurn`;
- expulsión determinista por importancia → confianza → recencia → key;
- recall ordenado y filtrado;
- forget sin mutar el input.

## 5. Inputs hostiles

Prueba:

- getter/accessor en campos requeridos;
- objeto heredado;
- `NaN`, `Infinity`, `-Infinity`;
- turnos negativos;
- scores fuera de 0..100;
- valores objeto/array;
- memory con keys duplicadas;
- entry interna malformada.

Comprueba que ningún input inválido alcance operaciones de negocio.

## 6. Inmutabilidad

Comprueba que:

- `recordMemory` no muta memory ni event;
- `recallMemory` devuelve copias;
- `forgetMemory` no muta la memoria original;
- una salida previa no cambia al modificar una salida posterior.

## 7. Casos adversariales

Busca contraejemplos mínimos en:

- expiración + upsert en mismo turno;
- entrada que expira y luego reaparece con la misma key;
- empate total de retención;
- `-0` vs `0` como `value`;
- strings Unicode en `key`;
- capacidad mínima 1 y máxima 1024;
- secuencias largas de actualizaciones de una sola key.

## 8. Alcance

No exijas todavía integración con Utility AI/GOAP, relaciones, scheduler, social AI, pathfinding o canon.

## Entregable

Termina exactamente con uno:

`V030_MEMORY_APTO_PARA_ITERAR`

`V030_MEMORY_REQUIERE_CORRECCIONES`

`V030_MEMORY_FALLO_CONCEPTUAL`
