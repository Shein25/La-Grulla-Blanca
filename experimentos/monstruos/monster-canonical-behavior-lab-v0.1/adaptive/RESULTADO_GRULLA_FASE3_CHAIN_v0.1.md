# Resultado — Grulla Fase III-A · cadena y política maestra v0.1

**Fecha:** 2026-09-26  
**Estado:** EXPERIMENTAL / M_A CANDIDATO PRINCIPAL  
**Rama:** `experiment/monster-adaptive-survival-lab-v0.1`

## 1. Punto de partida congelado

Fase I y Fase II permanecen cerradas. Fase II usa `CHAIN_A`. Fase III conserva el baseline correcto de **50 HP**.

El cerebro `LA CAMPANA SIN DUEÑO` no se modifica: Picotazo Blanco, Campana sin Dueño, Ala Vacía, Pata Inmóvil, Silencio entre Campanas, Romper Ritmo y Buscar Pulso.

## 2. Perfiles de sensibilidad

```text
HIST (control histórico, no candidato)
ATQ 5 / DEF 12
Picotazo +2 ATQ, 1d8+4
Campana +5 ATQ, 2d8+5, drain 4
Ala +25 EVA / Pata +5 DEF
Romper +4 ATQ, 2d8+3

M_A
ATQ 4 / DEF 13
Picotazo +1 ATQ, 1d4+1
Campana +1 ATQ, 1d6+2, drain 2
Ala +10 EVA / Pata +3 DEF
Romper +2 ATQ, 1d6+2

M_B
ATQ 4 / DEF 13
Picotazo +1 ATQ, 1d4+1
Campana +1 ATQ, 1d6+3, drain 2
Ala +15 EVA / Pata +3 DEF
Romper +2 ATQ, 1d8+2

M_C
ATQ 5 / DEF 13
Picotazo +1 ATQ, 1d4+2
Campana +2 ATQ, 1d8+2, drain 2
Ala +15 EVA / Pata +3 DEF
Romper +3 ATQ, 1d8+3
```

## 3. Aislamiento descartado para balance

Con jugador fresco, M_A/M_B/M_C superan ~97–99% READER. HIST ronda 47,9%. Fase III debe balancearse en cadena porque el desgaste heredado domina el resultado.

## 4. Cadena I -> II -> III — selección 2.000

Entrada media READER a Fase III: ~10,2 HP y ~7,6 qi.

| Perfil | Estrategia | Llega FIII | FIII condicional | I+II+III |
|---|---|---:|---:|---:|
| HIST | ALTERNATE | 11,08% | 3,52% | 0,54% |
| HIST | READER | 20,38% | 4,40% | 1,19% |
| M_A | ALTERNATE | 10,93% | 25,90% | 3,37% |
| **M_A** | **READER** | **19,95%** | **31,66%** | **7,43%** |
| M_B | ALTERNATE | 11,19% | 26,32% | 3,34% |
| M_B | READER | 20,33% | 30,23% | 7,12% |
| M_C | ALTERNATE | 10,98% | 15,44% | 2,06% |
| M_C | READER | 20,47% | 18,81% | 4,67% |

## 5. Confirmación M_A / M_B — 10.000

```text
M_A
ALTERNATE  FIII condicional 26,48% / total 3,36%
READER     FIII condicional 32,10% / total 7,55%

M_B
ALTERNATE  FIII condicional 25,18% / total 3,20%
READER     FIII condicional 30,09% / total 7,10%
```

M_A READER por raíz: Fuego 30,61%, Metal 38,57%, Agua 27,12% condicional.

## 6. Anti-spam global

Con M_A y M_B, 5.000 por build:

```text
PURE SPAM            llega FIII = 0% / victoria total = 0%
SPAM + DEFENDER      llega FIII = 0% / victoria total = 0%
```

## 7. Hallazgo de política

El READER heredado de Fase II era demasiado conservador: alternaba raíz/BASIC de forma casi rígida y producía ~0 apariciones de Silencio/Buscar Pulso.

Un jugador codicioso que ignora planes alcanzó ~34,24% condicional con M_A, frente a ~32,22% del READER antiguo. El problema estaba en la política del jugador simulado, no en los stats del jefe.

## 8. MASTER_READER

Política:

- permite hasta dos técnicas consecutivas;
- si aparece Silencio entre Campanas usa BASIC y rompe el patrón;
- si aparece Buscar Pulso usa acción sin qi;
- si aparece Romper Ritmo o amenaza pesada con HP comprometido usa DEFENDER;
- conserva cura crítica;
- no conoce RNG futuro.

Screening 5.000 con M_A:

```text
READER antiguo   32,22%
GREEDY            34,24%
MASTER_READER     35,32%
```

Frecuencia media aproximada por Fase III:

```text
MASTER_READER
Silencio       0,259
Buscar Pulso   0,030
planes armados 0
planes rotos   0,289

GREEDY
Silencio       0,248
planes armados 0,160
Romper Ritmo   0,153
planes rotos   0,088
```

## 9. Confirmación MASTER_READER — M_A, 15.000

| Estrategia | Llega FIII | FIII condicional | I+II+III |
|---|---:|---:|---:|
| GREEDY | 20,32% | 34,11% | 8,05% |
| **MASTER_READER** | **20,22%** | **35,17%** | **8,33%** |

MASTER por raíz:

| Raíz | Llega FIII | FIII condicional | Total |
|---|---:|---:|---:|
| Fuego | 21,54% | 34,97% | 8,61% |
| Metal | 20,37% | 42,50% | 9,89% |
| Agua | 18,75% | 28,05% | 6,49% |

Rango condicional entre builds: **16,30% .. 74,29%**.

## 10. Lectura provisional

M_A es el candidato principal: mantiene 50 HP, respeta el desgaste acumulado, MASTER_READER supera al codicioso, los planes tienen counterplay real, spam sigue en 0% y las tres raíces tienen ruta.

Fase III todavía NO se congela.

Pendiente:

```text
Paso en cadena completa
Piel en cadena completa
Filamento en cadena completa
stress de recursos
confirmación de counterplay opcional
```

## 11. Estado

```text
FASE I              CERRADA
FASE II             CERRADA
FASE III HP 50      MANTENER
M_A                  CANDIDATO PRINCIPAL
M_B                  SENSIBILIDAD
M_C                  SENSIBILIDAD
HIST                 DESCARTADO COMO BALANCE
MASTER_READER        SELECCIONADO PARA VALIDACIÓN
OPCIONALES FIII      PENDIENTES
VER74                SIN CAMBIOS
```