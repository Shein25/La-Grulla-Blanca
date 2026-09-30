# ETAPA 19 — Matriz masiva de balance en Colab

Fecha: 2026-09-29
Rama: experiment/combat-stat-contract-v0.1
Estado: **PIPELINE INICIADO / ESPACIO ESTRUCTURAL CERRADO / COMBATE MASIVO A EJECUTAR EN COLAB**

## Objetivo

Cruzar por etapa:
- todos los monstruos nativos;
- todas las raíces;
- todas las configuraciones legales de Tramos/puntos;
- todo el catálogo de equipo disponible por etapa;
- T0 natural y T1 supervivencia;
- varias políticas de uso de técnicas;
- posteriormente escenarios de grupo para AOE.

La adquisición económica definitiva queda fuera hasta su auditoría. Esta primera matriz usa:
`UNCONSTRAINED_STAGE_AVAILABLE_GEAR`.

## 1. Espacio real de combinaciones

Equipo, permitiendo slot vacío y hasta 2 anillos:

| Etapa | combinaciones de equipo |
|---|---:|
| LianQi I | 6,144 |
| LianQi II | 6,881,280 |
| LianQi III | 548,100,000 |
| LianQi IV | 5,234,761,728 |

Builds legales de habilidades POR RAÍZ, permitiendo guardar puntos:

| Etapa | puntos totales | builds por raíz |
|---|---:|---:|
| LI | 0 | 1 |
| LII | 2 | 37 |
| LIII | 4 | 739 |
| LIV | 6 | 11,512 |

Con cinco raíces:

| Etapa | builds de habilidades totales |
|---|---:|
| LI | 5 |
| LII | 185 |
| LIII | 3,695 |
| LIV | 57,560 |

Producto bruto jugador:

| Etapa | equipment × skill builds |
|---|---:|
| LI | 30,720 |
| LII | 1,273,036,800 |
| LIII | 2,025,229,500,000 |
| LIV | 301,312,885,063,680 |

Si además se cruza cada build contra cada monstruo nativo en T0/T1:

| Etapa | escenarios brutos antes de iteraciones |
|---|---:|
| LI | 307,200 |
| LII | 12,730,368,000 |
| LIII | 16,201,836,000,000 |
| LIV | 2,410,503,080,509,440 |

Por tanto "Monte Carlo de cada fila bruta" es computacionalmente absurdo incluso en Colab.

## 2. Qué significa exhaustivo

La matriz será exhaustiva en estructura:

1. todos los objetos entran en el generador;
2. todos los slots y combinaciones legales quedan contabilizados;
3. todos los nodos de las 15 técnicas entran;
4. todas las builds legales de puntos quedan enumeradas;
5. todos los monstruos nativos entran;
6. T0 y T1 entran;
7. ninguna raíz o familia se excluye.

La simulación probabilística usará reducción/funnel:

### PASS A — EXACT STRUCTURAL
Cuenta todos los estados y genera firmas.

### PASS B — MECHANICAL SIGNATURE
Colapsa loadouts que producen exactamente la misma firma mecánica relevante.

### PASS C — COVERAGE SCREEN
Muestreo estratificado que garantiza:
- cada objeto;
- cada nodo;
- cada técnica;
- cada raíz;
- cada monstruo;
- extremos por stat;
- perfiles MANDATORY/EXPECTED/HIGH_ROLL.

### PASS D — MONTE CARLO LOW-N
Barrido barato para detectar regiones.

### PASS E — ACTIVE REFINEMENT
Re-simula con N alto:
- fronteras ~50% win;
- extremos;
- anomalías;
- builds dominantes;
- builds que cambian mucho T0→T1;
- configuraciones de alta varianza.

Esto permite analizar el espacio entero sin fingir que 300 billones de builds pueden recibir miles de duelos individualmente.

## 3. Traducción LAB de monstruos

Archivo:
`experimentos/balance_nuevo/monster_arc1_new_contract_lab.json`

Regla clave:
- legacy `defensa` NO se copia como DEF plana;
- se traduce principalmente a Evasión, porque en ver74 formaba parte del chequeo de impacto;
- DEF plana nueva se asigna por anatomía/rol.

Preservación de probabilidades de referencia:

```text
monster Precision = 60 + 5 * legacy_attack
monster Evasion   = 5 * legacy_defense - 10
```

Referencias:
- jugador legacy desnudo: ataque1 / defensa10 / esquiva5;
- jugador nuevo desnudo: Precisión100 / Evasión5.

DEF y Tenacidad del monstruo son LAB por rol/anatomía y serán sensibilidad, no CANON.

## 4. C_STAGGERED

Matriz nativa principal:
- T0 NATURAL;
- T1 SUPERVIVENCIA.

Para monstruos nativos de la misma etapa el ceiling normal es T1.

Regression posterior:
- monstruos de etapas anteriores contra jugador superior;
- T2/T3/T4 cuando el ceiling y presión lo permitan.

## 5. Habilidades

Enumerador:
`experimentos/balance_nuevo/etapa19_skill_buildspace.py`

Incluye las 15 técnicas y sus opciones I/II/III.

Regla:
- un tramo superior necesita cualquier elección anterior en la misma técnica;
- no obliga a misma familia;
- puntos guardables.

Antes del Monte Carlo final, el adaptador unificado debe convertir cada selección a primitivas del contrato:
- DIRECT_DAMAGE;
- DOT;
- CONTROL;
- ABSORPTION;
- DEFENSE;
- EVASION;
- PRECISION/PENETRATION;
- debuffs;
- reactive windows;
- Qi cost.

## 6. Equipo

Fuente:
`equipment_arc1_catalog.json`

Para esta primera matriz:
- se ignora todavía la factibilidad económica exacta;
- cualquier objeto con min_stage <= etapa es elegible;
- se conserva el Tesoro único;
- se marcan aparte builds imposibles después de auditoría económica.

Después de auditar adquisiciones:
`ACQUISITION_LEGAL_ONLY`
se vuelve a ejecutar sin cambiar el motor.

## 7. Métricas

Por escenario:
- win rate;
- draw/timeout;
- HP final;
- Qi final;
- Qi gastado;
- rondas;
- daño infligido/recibido;
- DOT;
- daño evitado por DEF/EVA/Absorción;
- controles intentados/exitosos;
- acciones enemigas negadas;
- supervivencia T1 usada;
- placas/pools/cargas consumidas;
- daño por Qi;
- técnicas por combate;
- basic fallback;
- cambios T0→T1.

Agregados:
- percentiles P05/P25/P50/P75/P95;
- mejores/peores builds por monstruo;
- sensibilidad por item/nodo;
- frecuencia de cada objeto en builds top;
- builds universales sospechosas;
- piezas/nodos muertos;
- interacción raíz×equipo;
- interacción equipo×monstruo.

## 8. Fases

### 19A
Espacio de builds + traducción monstruos. CERRADO.

### 19B
Motor unificado jugador/monstruo para 1v1 nativo.

### 19C
Colab native-stage T0/T1.

### 19D
Packs 2/3 enemigos y AOE.

### 19E
Regresión poblaciones antiguas T2–T4.

### 19F
Repetición post-auditoría de adquisición.

## 9. Guardias

- no promover números de monstruos traducidos a CANON;
- no convertir legacy DEF a flat DEF;
- no balancear bosses como normales;
- no nerfear equipo por un único mob;
- no buffear equipo sólo por un boss opcional;
- no interpretar HIGH_ROLL como baseline;
- conservar seeds/provenance/commit hashes;
- cualquier reducción del espacio debe mantener multiplicidad/trazabilidad.

## 10. Estado actual

Archivos:
- monster_arc1_new_contract_lab.json
- etapa19_skill_buildspace.py
- etapa19_buildspace_planner.py

Siguiente implementación inmediata:
- motor unificado ETAPA19B;
- notebook Colab dedicado a ETAPA19.
