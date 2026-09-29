# TEST — LianQi I NAKED · PHASE A direct packet

Fecha: 2026-09-29  
Rama: `experiment/combat-stat-contract-v0.1`  
Estado: **PASS PROVISIONAL / NO CANON**

## Objetivo

Validar el primer baseline estricto de daño directo de LianQi I bajo el sistema
nuevo, sin usar estadísticas legacy.

Baseline probado:

```text
enemigo de referencia
Evasión 20
DEF 2

ataque básico
1d4+4
coste 0 Qi

técnicas iniciales
Palma Ardiente       2d4+5
Destello de Plata    2d4+4
Latigazo de Marea    2d4+3
Golpe de Montaña     2d4+4
Lanza que Parte Nubes 2d4+3
```

Todas las cifras anteriores son **PROVISIONAL**.

## Aislamiento

Este test mide sólo:

- Precisión/Evasión;
- daño variable;
- crítico;
- modificadores generales de raíz;
- penetración;
- DEF plana;
- redondeo `ROUND_HALF_UP`.

Excluye todavía:

- HP/TTK;
- Qi máximo y economía completa;
- daño enemigo;
- equipo;
- Concordancias;
- injerto;
- Tramos;
- valor adicional de Arrastre;
- valor adicional de Peso;
- defensivas.

## Monte Carlo

Se ejecutó una comprobación reproducible de **300.000 acciones por acción/raíz**.

| Raíz | Básico medio | Técnica media | Premium técnica | Hit básico | Hit técnica |
|---|---:|---:|---:|---:|---:|
| Fuego | 4.649 | 7.650 | 1.646x | 79.86% | 79.93% |
| Metal | 3.966 | 6.157 | 1.553x | 84.92% | 85.03% |
| Agua | 3.738 | 4.978 | 1.332x | 80.04% | 80.08% |
| Tierra | 3.743 | 5.785 | 1.546x | 80.13% | 79.94% |
| Viento | 3.741 | 5.476 | 1.464x | 80.03% | 85.01% |

Promedios descriptivos:

- ataque básico: ~3.967 daño por acción;
- técnica: ~6.009 daño por acción;
- premium medio: ~1.508x;
- rango del premium: ~1.332x–1.646x.

No hubo impactos conectados reducidos a 0 por DEF en ninguna de las diez
combinaciones.

## Cross-check determinístico

Se añadió:

`experimentos/balance_nuevo/phase_a_exact_check.py`

El script enumera todas las tiradas posibles y calcula el valor esperado sin
muestreo aleatorio.

Resultados exactos:

| Raíz | Básico exacto | Técnica exacta | Premium exacto | Hit básico | Hit técnica |
|---|---:|---:|---:|---:|---:|
| Fuego | 4.6600 | 7.6500 | 1.6416x | 80% | 80% |
| Metal | 3.9738 | 6.1519 | 1.5481x | 85% | 85% |
| Agua | 3.7400 | 4.9700 | 1.3289x | 80% | 80% |
| Tierra | 3.7400 | 5.7900 | 1.5481x | 80% | 80% |
| Viento | 3.7400 | 5.4719 | 1.4631x | 80% | 85% |

La desviación máxima entre Monte Carlo y valor esperado exacto fue inferior a
**0,25%**.

## Lectura por raíz

### Fuego

Presenta el mayor premium bruto (~1.64x) porque su raíz aumenta daño directo y
probabilidad crítica.

Esto es consistente con su identidad ofensiva.

### Metal

Mantiene ~85% de impacto y un premium ~1.55x. Su penetración aún tiene margen
para ganar valor contra DEF superior.

### Agua

Tiene el menor premium bruto (~1.33x).

No se interpreta como déficit todavía: este test excluye deliberadamente el
valor de Arrastre y también excluye su ventaja de economía de Qi.

### Tierra

Premium bruto ~1.55x antes de valorar Peso y su ventaja de supervivencia por
raíz.

### Viento

Premium ~1.46x, con ~85% de impacto por la Precisión propia de la técnica y
mejor crítico por raíz.

## Criterios de PASS

El baseline cumple simultáneamente:

1. el ataque básico sigue siendo funcional sin Qi;
2. gastar Qi mantiene una mejora clara de daño directo;
3. ninguna técnica queda por debajo del ataque básico;
4. ninguna acción acertada es anulada por la DEF ordinaria de referencia;
5. Precisión y penetración conservan espacio para crear identidades distintas;
6. las diferencias de Agua/Tierra no se corrigen artificialmente antes de
   valorar sus propiedades secundarias;
7. Monte Carlo y cálculo exacto coinciden.

## Resultado

**PHASE_A_DIRECT_PACKET = PASS PROVISIONAL**

No significa que Evasión 20, DEF 2 o los dados elegidos sean CANON definitivos.
Significa que forman un baseline suficientemente sano para continuar el diseño
sin reabrir PHASE A en cada prueba.

Se conservan como stress profiles:

- DEF 4 → resistente/acorazado;
- Evasión ~35 → evasivo especializado.

## Siguiente fase

**PHASE B — QI BUDGET**

Pendientes:

- Qi máximo de LianQi I;
- piso global de coste de Qi.

Preguntas que deberá responder:

1. cuántas técnicas puede lanzar un personaje desde Qi lleno;
2. cuánto pesa el coste 6/7;
3. cuánto valor real aporta la reducción de coste de Agua;
4. cuándo aparece el ataque básico por agotamiento;
5. si hace falta o no una futura acción de circulación activa de Qi.

No se fijará regeneración pasiva universal.
