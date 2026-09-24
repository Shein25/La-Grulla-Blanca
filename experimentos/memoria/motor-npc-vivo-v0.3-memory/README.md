# Motor NPC Vivo v0.3.0 — Laboratorio de memoria

Primera iteración experimental posterior al cierre de GOAP v0.2.2.

Rama:

`experiment/motor-npc-v0.3-memory`

## Objetivo de esta iteración

Probar exclusivamente un núcleo de **memoria semántica acotada y determinista**.

Todavía NO se conecta la memoria a Utility AI ni a GOAP. Primero se valida que almacenar, actualizar, recordar, olvidar y expirar información sea estable.

## Arquitectura preservada

La base experimental anterior queda congelada:

```text
Utility AI → selecciona objetivo
GOAP       → plan lógico
Executor   → ejecuta / verifica
```

v0.3.0 añade una capacidad lateral todavía no conectada:

```text
Evento validado
      ↓
Memoria semántica v0.3.0
      ↓
recall / prune / forget
```

La integración futura podrá alimentar estado derivado o relaciones antes de Utility AI, pero no forma parte de v0.3.0.

## Contrato de un recuerdo

Cada recuerdo interno contiene:

```js
{
  key,          // identidad semántica estable
  kind,         // categoría sintética del laboratorio
  subject,      // sujeto al que refiere
  value,        // null | boolean | string | number finito
  importance,   // entero 0..100
  confidence,   // entero 0..100
  firstTurn,    // primer turno observado
  lastTurn,     // actualización más reciente
  count,        // cantidad de observaciones
  expiresTurn   // null o turno de expiración explícita
}
```

## Reglas v0.3.0

- `key` identifica un único concepto semántico.
- Repetir una `key` actualiza el recuerdo; no crea duplicados.
- Una misma `key` no puede cambiar de `kind` ni `subject`.
- Eventos atrasados para una misma `key` se rechazan.
- No existe decay automático en esta versión.
- La expiración sólo ocurre si se declara `expiresTurn`.
- Un recuerdo es válido durante `expiresTurn` inclusive y expira al turno siguiente.
- Capacidad por defecto: 32 recuerdos.
- El límite configurable permitido es 1..1024.
- Si hay que expulsar recuerdos, se conservan por este orden:
  1. mayor importancia;
  2. mayor confianza;
  3. mayor recencia (`lastTurn`);
  4. `key` lexicográficamente menor según comparación JS.
- El almacenamiento interno queda ordenado canónicamente por `key`.
- `recallMemory` devuelve por fuerza de retención, no por orden de almacenamiento.
- No se mutan memoria, eventos ni resultados anteriores.

## Frontera de seguridad

El evento externo se captura mediante propiedades de datos propias. Se rechazan:

- accessors/getters en campos requeridos;
- objetos heredados no planos;
- números no finitos;
- turnos negativos;
- importancia/confianza fuera de rango;
- valores complejos como objetos o arrays.

Esto adopta desde el inicio una parte de las lecciones de hardening de Utility AI v0.1.1.

## Suite inicial

La candidata inicial contiene:

- 23 tests unitarios/regresión;
- stress determinista de 10.000 eventos;
- límite comprobado de 32 recuerdos;
- ausencia de keys duplicadas;
- repetición con misma seed produce la misma salida.

## Fuera de alcance

Todavía no implementar:

- efectos sobre afinidad/confianza/deuda;
- memoria NPC↔NPC;
- rumores;
- propagación de conocimiento;
- decay probabilístico;
- embeddings o búsqueda vectorial;
- LLM dentro de la memoria;
- scheduler;
- persistencia save/load real;
- NPC, salas, gates o misiones canónicas.
