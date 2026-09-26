# Intermedios — baseline agrupado v0.1

Se agrupan seis NPC intermedios restantes usando el snapshot canónico ver74.

## Shen Baojun

- M03: entrenamiento básico/Paso de Nube.
- M16: NO CERRADO EN FUENTE.
- Política: FSM mínima; M03 emite entrenamiento, M16 no inventa rol.

## Madre Wen

- continuidad cotidiana de externos;
- M01: integración de aspirantes;
- M16 informal/no cerrado.
- Política: FSM mínima; no se inventa frente formal.

## Tao Ming

Canon M16 explícito:

`deja de registrar trabajos rutinarios y registra emergencias`.

Se prueba cambio de modo ROUTINE → EMERGENCY → ROUTINE.

## Su Lian

- tutorial Herboristería;
- responsable principal única de JARDINES en M16.

Behavior Tree: crisis de jardines preempta tutorial.

## Chen Bo

- M02 Examen Espiritual;
- M16 co-responsable MEDICINA;
- canon: prioriza pacientes.

Behavior Tree: pacientes preemptan examen.

## Yao Fen

- desbloqueo Alquimia LII;
- co-responsable MEDICINA M16.

Behavior Tree: crisis médica preempta lección de alquimia.

Todos los intents siguen siendo simbólicos; no ejecutan movimiento, cultivo, tratamiento ni crafting.

Estado: `INTERMEDIATE_GROUP_BASELINE: 30_PASS_0_FAIL_CONFIRMED`.


## Confirmación

```text
PASS: 30
FAIL: 0
```

Trazas clave confirmadas:

- Tao Ming: `ROUTINE → EMERGENCY → ROUTINE`;
- Su Lian: crisis de Jardines preempta tutorial;
- Chen Bo: pacientes preemptan examen;
- Yao Fen: crisis médica preempta lección de alquimia;
- Shen Baojun y Madre Wen no generan comportamiento M16 no cerrado por fuente.
