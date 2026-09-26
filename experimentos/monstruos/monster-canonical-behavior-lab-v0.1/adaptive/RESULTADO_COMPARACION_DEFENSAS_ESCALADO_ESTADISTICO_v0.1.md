# Resultado — Defensas E1 definitivas vs escalado estadístico por etapa v0.1

> **DOCUMENTO HISTÓRICO / SUPERSEDED.** La dirección adaptativa vigente está definida en `DECISION_MODELO_C_ADAPTACION_POBLACIONAL_v0.2.md` (`C_STAGGERED`). Este archivo se conserva como evidencia de los experimentos que llevaron a esa decisión.

**Estado:** EXPERIMENTAL / NO CANÓNICO.

## Objetivo

Comparar dos modelos:

### MODELO A — DEFENSA E1 SIN ESCALADO DE STATS

La especie conserva exactamente sus estadísticas canónicas de ver74.

Sólo aprende una acción de supervivencia coherente con su anatomía/rol.

### MODELO B — DEFENSA E1 + PROGRESIÓN ESTADÍSTICA

La especie conserva ATQ y DEF canónicos, pero su etapa nativa añade:

```text
LianQi I    HP ×1,00   daño ×1,00
LianQi II   HP ×1,05   daño ×1,05
LianQi III  HP ×1,10   daño ×1,10
LianQi IV   HP ×1,15   daño ×1,15
```

ATQ y DEF no escalan porcentualmente.

## Por qué ATQ/DEF quedan fuera del porcentaje

Se probó escalar **todos** los stats entre 1% y 5% por etapa.

Aunque el porcentaje parezca pequeño, ATQ/DEF son enteros dentro de una tirada d20.

Ejemplo experimental:

```text
Etapa IV
2% por escalón
factor = 1,06

DEF 15 × 1,06 = 15,9
→ round = 16
```

Ese solo punto puede equivaler a ~5 puntos porcentuales de impacto y crea un salto brusco.

En el barrido:

```text
Mantis, victoria jugador
0% escalado total  → 73,5%
1% / etapa         → 72,1%
2% / etapa         → 58,6%

Centinela
0%                 → 82,6%
1%                 → 81,2%
2%                 → 70,4%

Guardián Coral
0%                 → 34,9%
1%                 → 32,9%
2%                 → 27,2%
```

Por eso el escalado proporcional de ATQ/DEF fue rechazado.

## Valores E1 fijados como candidato final

| Monstruo | Etapa | Familia | Valor final |
|---|---:|---|---|
| Rata de Qi | I | Esquiva | +25 |
| Avispa de Jade | I | Esquiva | +25 |
| Serpiente de Qi | I | Esquiva | +20 |
| Macaco ladrón | I | Esquiva | +20 |
| Lobo espiritual | I | Defensa | +3 |
| Sapo de Ceniza | II | Mitigación | 35% |
| Escarabajo de Hierro | II | Absorción | 4 / reserva 8 |
| Eco del Caído | II | Mitigación | 40% |
| Sapo Caldera | II | Absorción | 4 / reserva 8 |
| Rey Escarabajo | II | Absorción | 5 / reserva 10 |
| Pez Lunar | III | Esquiva | +25 |
| Anguila Estelar | III | Esquiva | +25 |
| Sombra Ahogada | III | Mitigación | 40% |
| Guardián Coral | III | Absorción | 5 / reserva 10 |
| Devorador de Niebla | IV | Absorción | 4 / reserva 8 |
| Halcón de Tormenta | IV | Esquiva | +30 |
| Mantis de Nube | IV | Defensa | +5 |
| Centinela de Plumas | IV | Defensa | +5 |

Todas:

```text
consumen la acción
cooldown = 2 rondas
no rompen CADENCE_COMPAT
```

## Qué cambió respecto del set anterior

Sólo se reforzaron las defensas donde gastar la acción defensiva hacía al monstruo ligeramente más fácil:

```text
Sapo Ceniza      30 → 35%
Eco Caído        35 → 40%
Pez Lunar        +20 → +25 esquiva
Sombra Ahogada   35 → 40%
Anguila          +20 → +25 esquiva
Devorador        3/6 → 4/8
Halcón           +25 → +30 esquiva
Mantis           +4 → +5 defensa
Centinela        +4 → +5 defensa
```

En el barrido final, estos cambios movieron la victoria preparada aproximadamente entre 0 y −0,4 puntos porcentuales respecto del set anterior.

No se reforzó indiscriminadamente el resto.

## Modelo A — resultado sin escalado estadístico

Promedio de victoria del jugador preparado por banda:

```text
Etapa I    94,9%
Etapa II   71,3%
Etapa III  78,6%
Etapa IV   87,2%
```

La media mezcla NORMAL/ELITE/BOSS y no debe leerse como dificultad objetivo única.

Casos representativos:

```text
Escarabajo       94,6%
Sapo Caldera     44,2%
Rey Escarabajo   31,5%

Guardián Coral   35,8%

Devorador        97,9%
Halcón           96,3%
Mantis           72,9%
Centinela        81,8%
```

Lectura:

- las defensas aportan identidad y supervivencia;
- no convierten por sí solas a los normales en elites;
- los jefes mantienen el papel que ya tenían por ficha/kit;
- volver a etapas antiguas sigue transmitiendo progreso del jugador.

## Modelo B — +5% HP y daño por etapa

Promedio de victoria del jugador preparado por banda:

```text
Etapa I    94,7%
Etapa II   66,4%
Etapa III  71,4%
Etapa IV   74,3%
```

Casos representativos:

```text
Escarabajo       91,8%
Sapo Caldera     35,7%
Rey Escarabajo   24,5%

Guardián Coral   22,1%

Devorador        93,4%
Halcón           89,5%
Mantis           51,3%
Centinela        63,0%
```

Este modelo hace que la diferencia entre bandas se note mucho más.

## Variante probada: HP/daño + ATQ discreto

También se probó:

```text
HP y daño +5% por etapa
ATQ +1 desde Etapa III
DEF sin cambios
```

Promedios:

```text
Etapa I    95,2%
Etapa II   66,9%
Etapa III  67,9%
Etapa IV   70,0%
```

Fue descartada como opción base porque castiga demasiado Aguas/Alturas y vuelve a los jefes notablemente más duros:

```text
Guardián Coral 17,2%
Mantis         45,3%
Centinela      57,5%
```

## Conclusión de los dos modelos

### Modelo A

Más conservador.

Ventajas:

- preserva el balance canónico actual;
- la evolución cambia conducta, no números;
- maximiza la sensación de que el jugador supera zonas viejas;
- menor riesgo de power creep.

### Modelo B

Más marcado.

Ventajas:

- la etapa nativa se siente también físicamente;
- diferencia más claramente Cantera/Aguas/Alturas;
- HP y daño son continuos y no introducen breakpoints de precisión.

Coste:

- los jefes de Etapas II–IV se vuelven significativamente más exigentes;
- requiere considerar esta progresión al balancear consumibles/equipo.

## Candidato fijado

Quedan dos configuraciones válidas y explícitas en el laboratorio:

```text
A: FINAL_E1_FIXED_STATS
   estadísticas canónicas
   + valores E1 finales

B: FINAL_E1_STAGE_SCALING
   valores E1 finales
   + HP/daño 100/105/110/115%
   + ATQ/DEF sin cambio
```

No se recomienda usar escalado porcentual de ATQ/DEF.

## Volumen de simulación de esta comparación

Además de los barridos anteriores del laboratorio, para este cierre se ejecutaron aproximadamente:

```text
828.000 duelos — sensibilidad 0–5% de todos los stats
496.800 duelos — set anterior vs E1 final vs all-stat 1%
372.600 duelos — sin escalado vs HP/daño 5% vs HP/daño 5% + ATQ
---------------------------------------------------------------
1.697.400 duelos
```

Las cifras son Monte Carlo; sirven para comparar modelos, no como promesa exacta de win rate de una partida concreta.
