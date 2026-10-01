# Rata T2 — revisión Policy Generalization

Fecha: 2026-10-01

## Integridad

Archivo:

`RESULTADOS_RATA_T2_POLICY_GENERALIZATION_V01.zip`

SHA-256:

`5783c4fdb6b8a9c70f2d6528f43dd38a7962e9cd987e518798175ee8d32577ca`

Contrato:

- experimento `RATA_T2_POLICY_GENERALIZATION_V01`;
- 5 player policies;
- 10 contextos por arm;
- 500 peleas naturales/contexto;
- 100 Mutantes/contexto;
- 6.000 peleas/arm;
- 20 arms;
- 120.000 peleas totales;
- T1 congelado +40 EVA / CD5 / REACTIVO_1 / BASE;
- observable action categories only;
- fallback a basic registrado como acción real;
- no canonical write;
- T3-T4 no ejecutados.

Policies:

- VETERAN;
- UNITARGET_FIRST;
- AOE_FIRST;
- DEFENSE_OPEN;
- ROTATION.

## R2_SHORT

```text
memory_window = 2
repeticiones = 2
bonus reconocimiento = +8
```

### Normal natural

| policy | trigger | precisión | falso + | desplazamiento Reflejo |
|---|---:|---:|---:|---:|
| VETERAN | 33,88% | 99,15% | 0,85% | +0,0626/pelea |
| UNITARGET_FIRST | 35,12% | 99,95% | 0,05% | +0,0640 |
| AOE_FIRST | 47,35% | 72,37% | 27,63% | +0,0380 |
| DEFENSE_OPEN | 23,92% | 99,64% | 0,36% | +0,0914 |
| ROTATION | 0,26% | 100% | 0% | +0,0000 |

Lectura:

- detecta muy bien repetición sostenida;
- se apaga de forma natural cuando el jugador rota categorías;
- no fuerza reconocimiento donde no existe repetición;
- el fallo AOE_FIRST aparece al romperse la cadena repetida, típicamente al
  cambiar la acción realmente ejecutada después del tramo AOE;
- ese fallo no produce una escalada peligrosa de Reflejo: el desplazamiento
  efectivo queda en +0,038 por pelea.

Mutantes mantienen la misma forma cualitativa:

- VETERAN: 96,82% precisión;
- UNITARGET_FIRST: 99,89%;
- AOE_FIRST: 71,56%;
- DEFENSE_OPEN: 99,13%;
- ROTATION: 100% con trigger muy bajo.

## R2_CENTRAL

```text
memory_window = 3
repeticiones = 2
bonus reconocimiento = +12
```

Problemas observados:

- reconoce con demasiada frecuencia en VETERAN/UNITARGET/AOE;
- AOE_FIRST: 33,77% falsos positivos;
- ROTATION: sólo 19,05% precisión y 80,95% falsos positivos;
- Mutante ROTATION: 31,36% precisión / 68,64% falso positivo.

Aunque el impacto de combate sigue siendo pequeño, conceptualmente deja de
representar una lectura limpia de hábito reciente.

No recomendado para T2.

## R3_CONSERVATIVE

```text
memory_window = 3
repeticiones = 3
bonus reconocimiento = +16
```

- excelente precisión cuando detecta patrones simples;
- casi no se expresa en VETERAN / UNITARGET / DEFENSE_OPEN / ROTATION;
- AOE_FIRST activa más, pero con 36,90% falsos positivos;
- el desplazamiento de Reflejo es prácticamente cero salvo AOE_FIRST.

No recomendado: demasiado silencioso para expresar la identidad T2 y tampoco
resuelve mejor el caso AOE.

## Interpretación del caso AOE_FIRST

AOE_FIRST es deliberadamente repetitiva mientras la acción puede ejecutarse.
Cuando el comportamiento real cambia, una predicción basada sólo en las dos
acciones anteriores puede fallar.

Esto no implica acceso oculto ni bug del recognizer.

Es una propiedad deseable de una IA de reconocimiento limitado:

```text
jugador repite un patrón
→ Rata aprende
→ jugador cambia patrón
→ Rata puede ser engañada
```

La capa T2 no debe convertirse en un predictor omnisciente.

Además el reconocimiento no cambia +40 EVA ni CD5; sólo añade presión de score
hacia el Reflejo ya congelado.

## Efecto de combate R2_SHORT

Los deltas frente a T1 permanecen pequeños:

- VETERAN normal: +0,021 rondas, +0,118 Qi;
- UNITARGET_FIRST: +0,023 rondas, +0,138 Qi;
- AOE_FIRST: -0,027 rondas, Qi prácticamente sin cambio;
- DEFENSE_OPEN: +0,041 rondas, +0,219 Qi;
- ROTATION: sin cambio medible.

No hay inestabilidad, timeout ni interacción explosiva con Mutantes.

## Recomendación de cierre humano

Seleccionar:

```text
RATA T2 — RECOGNITION
candidate: R2_SHORT

memory_window = 2
repeated_same_category_required = 2
count_results = EFECTIVA
preemptive_survival_bonus = +8

T1 sigue congelado:
Reflejo de Madriguera
+40 EVA
CD5
REACTIVO_1
BASE
```

Interpretación:

la Rata puede reconocer una repetición corta y anticipar el Reflejo, pero un
jugador que cambie de patrón puede romper esa predicción.

Estado recomendado:

`T2_NUMERIC_CANDIDATE_SELECTED_AWAITING_HUMAN_RATIFICATION`

T3 permanece bloqueado hasta ratificación humana.
T4 permanece bloqueado.
