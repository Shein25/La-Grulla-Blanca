# Resultado — T3 dual-stage focal V02

Fecha: 2026-10-06
Estado: **VALID / FINALISTS_SELECTED_FOR_FINAL_GATE**

Review ZIP SHA-256:
`f14ea3caf85ceb6f55eb19c5efe5e8f0ce7109fb041a53e18f68c454736bfaee`

## Integridad

- 176.640 combates.
- 2 workers.
- 2 réplicas por individuo/celda.
- LianQi I overreach + LianQi IV structural.
- T0/T1/T2 congelados.
- Mutantes/sufijos V1 activos.
- manifest 7/7 correcto.
- 0 timeouts.
- 0 NaN/Inf.
- false counter rate = 0.
- degenerate loops = 0.
- `issues=[]`.

## Selección final

### Rata Qi
Seleccionado: `R1_INSTANCE_BASIC` sin `ONCE_PER_FIGHT`.

Motivo:
- no falsos counters;
- no loops;
- multi-counter real pero limitado por el propio T1/cooldown/combate;
- la variante ONCE sólo reduce presión y añade una regla artificial;
- en LIV la diferencia entre libre y ONCE es mínima;
- en LI la mayor dureza corresponde a sobreextensión autoinducida.

### Serpiente Qi
Seleccionado: `S1_INSTANCE_POISON_TICK`.

- usa sólo el daño de veneno ya materializado de la instancia;
- no crea una duración adicional;
- estable en LI y LIV;
- identidad de presión sostenida preservada.

### Avispa Jade
Seleccionado: `A2_INSTANCE_POISON_TICK`.

- respuesta compacta;
- preserva identidad de picadura/veneno;
- no añade una nueva duración;
- estable en todas las poblaciones.

### Mono Píldoras
Seleccionado: `M2_INSTANCE_MANOTAZO_PACKET`.

- usa daño directo de Manotazo de la instancia;
- añade el QI_DRAIN 6 ya existente;
- no crea daño ni economía nueva;
- M1 drain-only quedó demasiado saturado/débil.

### Lobo Espiritual
Seleccionado: `L2_INSTANCE_EMBOSCADA_DAMAGE`.

- más específico a la identidad APEX/Emboscada que un básico genérico;
- no modifica la cadencia normal de Emboscada;
- no falsos counters/loops;
- presión superior a L1 pero estable en LIV y extremos.

## Nota de etapa

Los resultados LI son estrés de sobreextensión, no target de balance.
El contexto previsto de T3 sigue siendo presión avanzada / LIV.

El gate final debe repetir:
- LI_OVERREACH;
- LIV_STRUCTURAL;
- T2 vs T3 seleccionado;
- 4 réplicas;
- todas las poblaciones y policies.

No congelar hasta gate final.
