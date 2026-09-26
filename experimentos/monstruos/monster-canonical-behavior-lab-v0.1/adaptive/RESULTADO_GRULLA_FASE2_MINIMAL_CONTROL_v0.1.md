# Resultado — Grulla Fase II-A · control toolkit mínimo v0.1

**Fecha:** 2026-09-26  
**Estado:** EXPERIMENTAL / CONTROL INICIAL  
**Rama:** `experiment/monster-adaptive-survival-lab-v0.1`

## 1. Alcance

Se inicia exclusivamente:

```text
FASE II — LAS ALAS RECUERDAN
```

Fase I permanece cerrada y congelada.

Baseline restaurado:

```text
Fase II HP = 100
```

Toolkit del jugador:

```text
técnica raíz
ATACAR
DEFENDER
1 poción
```

No se usan todavía Paso/Piel/Filamento.

## 2. Cerebro

Se reproduce la lógica de `grulla-boss-brain-v0.1.mjs`:

- memoria útil de las últimas 3 acciones;
- resumen heredado de Fase I;
- counter heredado si Fase I mostró dependencia exclusiva de una skill;
- lock normal tras 3 usos consecutivos de la misma técnica;
- BASIC rompe el lock;
- DEFENDER/RECOVER no lo borran;
- Utility adaptativa con anti-spam de intenciones.

Intenciones:

```text
Golpe de Ala
Tormenta de Mil Plumas
Cerrar las Alas
Recordar el Filo
Eco del Meridiano
```

## 3. Efectos numéricos de control

Se reutilizan únicamente como control los valores provisionales del benchmark histórico:

```text
Tormenta      +3 ATQ, 2d6+3, drena 2 qi si hace daño
Cerrar Alas   absorción 4 / reserva 8
Recordar Filo +20 Esquiva siguiente ofensiva
Eco Meridiano drena 4 qi
```

No se declaran balance final.

## 4. Perfiles comparados

```text
SAME
ATQ 4
DEF 13
Golpe 1d6+2

DAMAGE
ATQ 4
DEF 13
Golpe 1d6+3

ATTACK
ATQ 5
DEF 13
Golpe 1d6+2
```

## 5. Volumen

```text
3 perfiles
× 4 estrategias
× 27 builds raíz
× 5.000
=
1.620.000 duelos
```

## 6. Resultado global

| Perfil | SPAM | SPAM+DEF | ALTERNATE | READER |
|---|---:|---:|---:|---:|
| SAME | 0,00% | 0,00% | **27,66%** | **26,38%** |
| DAMAGE | 0,00% | 0,00% | 22,71% | 21,56% |
| ATTACK | 0,00% | 0,00% | 18,92% | 17,64% |

### SAME por raíz

| Estrategia | Fuego | Metal | Agua |
|---|---:|---:|---:|
| ALTERNATE | 31,73% | 25,95% | 25,29% |
| READER | 32,00% | 23,24% | 23,90% |

Rangos de builds SAME:

```text
ALTERNATE
13,92% .. 48,62%

READER
12,58% .. 53,84%
```

## 7. Invariantes

En los tres perfiles:

```text
SPAM             -> 0% en las 27 builds
SPAM + DEFENDER  -> 0% en las 27 builds
```

El contrato duro anti-spam funciona.

DEFENDER no hace olvidar la técnica heredada.

## 8. Hallazgo

Los números provisionales antiguos no escalan bien al baseline restaurado de 100 HP.

Incluso con jugador fresco:

```text
SAME + ALTERNATE ~27,7%
SAME + READER    ~26,4%
```

Por tanto el problema no debe corregirse reduciendo los 100 HP ni debilitando el contrato de memoria.

El siguiente ajuste debe limitarse a los efectos provisionales de Fase II:

- Tormenta de Mil Plumas;
- Cerrar las Alas;
- Recordar el Filo;
- Eco del Meridiano.

También debe mejorarse la política READER para explotar correctamente los telegraphs sin reaccionar de forma automática.

## 9. Estado

```text
FASE I                         CERRADA
FASE II-A control              CERRADO
anti-spam                      VALIDADO
HP Fase II = 100               MANTENER

FX históricos                  DEMASIADO PUNITIVOS
perfil SAME                    CONTROL MÁS SUAVE
Paso/Piel/Filamento            TODAVÍA NO PROBAR

FASE III                       NO TOCAR
```

Script:

`benchmark/colab/grulla-phase2-minimal-grid-v0.1.py`
