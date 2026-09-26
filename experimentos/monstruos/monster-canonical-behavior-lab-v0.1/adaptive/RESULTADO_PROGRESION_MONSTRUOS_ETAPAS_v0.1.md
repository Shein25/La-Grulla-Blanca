# Resultado — Progresión natural de monstruos por cuatro etapas v0.1

## Estado

`EXPERIMENTAL_NON_CANONICAL_STAGE_PROGRESSION_V01`

Rama:

`experiment/monster-adaptive-survival-lab-v0.1`

## Qué se midió

Se simuló cada monstruo en su **etapa nativa propuesta** contra todas las raíces y ramas ofensivas disponibles legalmente en esa etapa.

Dos envolventes:

### MINIMAL

```text
uniforme inicial
espada de madera
sin consumibles
```

### PREPARED

Sensibilidad, no canon:

```text
equipo razonable de etapa
+ una poción de sangre
```

La progresión de ramas usada fue:

```text
LianQi I   → técnica base
LianQi II  → tramo 1
LianQi III → tramos 1–2
LianQi IV  → tramos 1–2
```

El tramo 3 permanece fuera porque exige ZhuJi.

## Tamaño del barrido

```text
2.000 duelos por build
2 perfiles
276 configuraciones nativas de build
1.104.000 duelos totales
```

No hizo falta Colab: el barrido fue suficientemente manejable localmente.

Benchmark reproducible:

`benchmark/stage-progression-benchmark-v0.1.mjs`

Comando:

```text
npm run benchmark:stage-progression -- --runs=2000
```

## Resultado por etapa

| Etapa | Monstruo | Rol | Win jugador MINIMAL | Win jugador PREPARED |
|---|---|---|---:|---:|
| I | Rata de Qi | NORMAL | 99,6% | 99,9% |
| I | Avispa de Jade | NORMAL | 98,3% | 99,6% |
| I | Serpiente de Qi | NORMAL | 91,4% | 95,6% |
| I | Macaco ladrón | SKIRMISHER | 84,5% | 92,1% |
| I | Lobo espiritual | APEX_BRIDGE | 74,8% | 83,3% |
| II | Sapo de Ceniza | NORMAL | 90,4% | 97,6% |
| II | Escarabajo de Hierro | TANK | 78,4% | 94,9% |
| II | Eco del Caído | ELITE | 50,5% | 83,1% |
| II | Sapo Caldera | BOSS | 22,8% | 44,4% |
| II | Rey Escarabajo | BOSS | 13,7% | 34,0% |
| III | Pez Lunar | NORMAL | 89,1% | 99,4% |
| III | Anguila Estelar | SKIRMISHER | 66,2% | 94,6% |
| III | Sombra Ahogada | ELITE | 34,0% | 81,5% |
| III | Guardián Coral | BOSS | 4,8% | 37,9% |
| IV | Devorador de Niebla | NORMAL | 71,4% | 97,8% |
| IV | Halcón de Tormenta | SKIRMISHER | 68,0% | 95,9% |
| IV | Mantis de Nube | BOSS | 17,5% | 70,7% |
| IV | Centinela de Plumas | BOSS | 23,2% | 79,7% |

## Lectura

### Etapa I

La curva es muy limpia:

```text
Rata / Avispa
→ tutorial

Serpiente
→ primera presión de estado

Macaco
→ primer skirmisher

Lobo
→ apex / puente a Etapa II
```

No hace falta inflar ninguna ficha para que se sientan distintas.

### Etapa II

Los normales/tank funcionan como segunda banda.

Eco del Caído se comporta como élite: con mínimo equipo es casi 50/50, pero un jugador preparado lo supera con claridad.

Sapo Caldera y Rey Escarabajo **no deben usarse para definir la dificultad promedio de Etapa II**.

Son picos de zona.

Incluso preparado:

```text
Sapo Caldera     44,4% victoria jugador
Rey Escarabajo   34,0%
```

Eso los confirma como jefes/encuentros opcionales o de preparación específica.

No se recomienda bajar sus estadísticas sólo para igualarlos a los normales.

### Etapa III

Pez y Anguila forman una banda media coherente.

Sombra Ahogada funciona como élite: el equipo y consumible cambian mucho el resultado.

Guardián Coral es un verdadero jefe de banda:

```text
MINIMAL   4,8%
PREPARED 37,9%
```

Debe tratarse como encuentro de preparación, no como fauna estándar de Aguas.

### Etapa IV

Devorador y Halcón son amenazas avanzadas pero razonables para un cultivador LianQi IV preparado.

Mantis y Centinela cumplen mejor el papel de jefes finales:

```text
Mantis      70,7% preparado
Centinela   79,7% preparado
```

Sin preparación siguen siendo muy peligrosos.

## Conclusión sobre la matriz 5 / 5 / 4 / 4

La distribución propuesta se sostiene:

```text
ETAPA I
Secta Exterior + Bosques
5 especies

ETAPA II
Cantera y Vetas
5 especies

ETAPA III
Aguas y Barrancos
4 especies

ETAPA IV
Alturas
4 especies
```

La dificultad interna se expresa mediante **rol**, no moviendo jefes de etapa sólo porque tengan una tasa de victoria menor.

## Progresión propia de monstruos

La etapa nativa y la etapa del jugador se relacionan así:

```text
playerStage < nativeStage
→ Tier 0
→ base natural
→ sin adaptación adicional

playerStage == nativeStage
→ techo Tier 1
→ supervivencia

playerStage == nativeStage + 1
→ techo Tier 2
→ memoria persistente de patrones
→ defensa anticipatoria elegible

playerStage == nativeStage + 2
→ techo Tier 3
→ contraadaptación por especie

playerStage == nativeStage + 3
→ techo Tier 4
→ segunda adaptación compatible
```

El techo sólo habilita posibilidades.

No otorga:

```text
+HP
+ATQ
+DEF
```

por el simple hecho de que el jugador haya subido de etapa.

## Ejemplo de sensación de progreso

Una Rata de Qi veterana en LianQi IV puede:

- haber aprendido a anticipar la apertura del jugador;
- usar Reflejo de Madriguera con mejor timing;
- haber desarrollado una segunda respuesta compatible.

Pero sigue teniendo la identidad física de una Rata de Qi.

El jugador que vuelve a Exterior en LianQi IV debe seguir sintiéndose muy superior.

## Relación con Survival Evolution

```text
especie
↓
etapa nativa
↓
rol regional
↓
etapa actual del jugador
↓
techo adaptativo
↓
XP adaptativa real
↓
defensa / memoria / contraadaptación
↓
effectiveKit
↓
Monster Combat AI
```

No se añade otro motor.

## Estado de implementación

Implementado en laboratorio:

- asignación nativa 18/18;
- bandas 1–4;
- roles;
- cálculo de relación jugador/especie;
- techo adaptativo 0–4;
- prohibición explícita de stat scaling;
- benchmark reproducible;
- sensibilidad MINIMAL/PREPARED.

Pendiente antes de producción:

- persistencia real de XP adaptativa;
- definición de umbrales Tier 2–4;
- señales persistentes de patrones;
- executor defensivo;
- simulación completa con las defensas E1 activas;
- escenarios multi-enemigo / unión ecológica.

## Resultado de tests

```text
8/8 PASS
```

Comprueba que:

- los 18 combatientes están asignados;
- la distribución es 5/5/4/4;
- todos los roles/etapas son válidos;
- un monstruo adelantado queda en Tier 0;
- la etapa nativa habilita Tier 1;
- una especie temprana puede ampliar su techo al ser superada por el jugador;
- no aparecen campos de escalado HP/ATQ/DEF;
- las relaciones de etapa se clasifican correctamente.
