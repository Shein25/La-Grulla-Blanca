# Cierre experimental — Grulla Blanca · Fase III v0.1

**Fecha:** 2026-09-26  
**Estado:** FASE III CERRADA EXPERIMENTALMENTE  
**Rama:** `experiment/monster-adaptive-survival-lab-v0.1`  
**Producción:** `ver74` sin cambios

## 1. Alcance

Queda cerrada:

```text
FASE III — LA CAMPANA SIN DUEÑO
```

Fase I y Fase II permanecen congeladas y no se reabren.

## 2. Perfil final — M_A

```text
HP                     50
ATQ                    4
DEF                    13

Picotazo Blanco        +1 ATQ / 1d4+1
Campana sin Dueño      +1 ATQ / 1d6+2 / drain 2 qi si daña
Ala Vacía              +10 EVA siguiente ofensiva
Pata Inmóvil           +3 DEF siguiente ofensiva
Romper Ritmo           +2 ATQ / 1d6+2
```

Silencio entre Campanas y Buscar Pulso permanecen como intenciones maestras de lectura/planificación, no como daño bruto inflado.

## 3. Política del jugador de referencia

Se congela `MASTER_READER` como política de validación.

Reglas:

- permite hasta dos técnicas consecutivas;
- si aparece Silencio entre Campanas usa BASIC y rompe patrón;
- si aparece Buscar Pulso usa acción sin qi;
- ante Campana/Romper con HP comprometido puede usar DEFENDER;
- conserva cura crítica;
- no conoce RNG futuro.

Confirmación:

```text
GREEDY
FIII condicional 34,11%
total             8,05%

MASTER_READER
FIII condicional 35,17%
total             8,33%
```

El lector supera al codicioso sin necesidad de estadísticas extra.

## 4. Cadena completa

Con M_A + MASTER_READER:

```text
Llega FIII           ~20,22%
FIII condicional     ~35,17%
I+II+III              ~8,33%
```

Por raíz:

| Raíz | Llega FIII | FIII condicional | Total |
|---|---:|---:|---:|
| Fuego | 21,54% | 34,97% | 8,61% |
| Metal | 20,37% | 42,50% | 9,89% |
| Agua | 18,75% | 28,05% | 6,49% |

Las tres raíces conservan rutas reales.

## 5. Anti-spam global

```text
PURE SPAM            0%
SPAM + DEFENDER      0%
```

El contrato duro del jefe se conserva hasta el final del encuentro.

## 6. Opcionales

Paso, Piel y Filamento fueron validados en cadena completa.

| Herramienta | Llega FIII | FIII condicional | I+II+III |
|---|---:|---:|---:|
| Paso | 13,28% | 16,11% | 2,45% |
| Piel | 21,45% | 21,48% | 5,22% |
| Filamento | 17,58% | 17,16% | 3,40% |

Reutilizar la opcional dentro de FIII altera la tasa condicional menos de 0,04 pp en valor absoluto.

Conclusión:

> Ninguna opcional es una llave de Fase III; el desgaste heredado y la lectura del plan dominan el resultado.

## 7. Stress de recursos

FIII standalone con HP28 / qi0 / poción0:

```text
victoria global 89,45%
```

Cadena real con qi y poción forzados a cero al entrar a FIII:

```text
llega FIII       20,35%
FIII condicional 18,40%
I+II+III          4,15%
```

No existe soft-lock de recursos.

## 8. Filosofía cerrada

La dificultad de Fase III proviene de:

1. desgaste acumulado de I y II;
2. planes que observan la acción resuelta;
3. necesidad de romper patrones;
4. presión de qi;
5. lectura de Silencio/Buscar Pulso;
6. coste de defender demasiado;
7. memoria y counters ya aprendidos;
8. elección de cuándo ser agresivo y cuándo variar.

No proviene de inflar HP, DEF o daño.

## 9. Contrato congelado

```text
FASE III HP                    50
FASE III ATQ                   4
FASE III DEF                   13

PICOTAZO                       +1 ATQ / 1d4+1
CAMPANA                        +1 ATQ / 1d6+2 / drain 2
ALA VACÍA                      +10 EVA
PATA                           +3 DEF
ROMPER RITMO                   +2 ATQ / 1d6+2

PERFIL                         M_A
POLÍTICA QA                    MASTER_READER
```

## 10. Estado final

```text
FASE I                         CERRADA / CONGELADA
FASE II                        CERRADA / CONGELADA
FASE III                       CERRADA / CONGELADA

M_A                            CONGELADO
MASTER_READER                  CONGELADO PARA QA
HP 50                          CONGELADO
ANTI-SPAM                      VALIDADO
OPCIONALES                     VALIDADAS
ZERO-QI                        VALIDADO

VER74                          SIN CAMBIOS
INTEGRACIÓN PRODUCTIVA         NO REALIZADA
```

No reabrir Fase III salvo invalidación concreta de las reglas simuladas o cambio productivo relevante.

## 11. Evidencia

- `adaptive/RESULTADO_GRULLA_FASE3_CHAIN_v0.1.md`
- `adaptive/RESULTADO_GRULLA_FASE3_FINAL_VALIDATION_v0.1.md`
- `benchmark/colab/grulla-phase123-chain-ma-v0.1.py`
- `benchmark/colab/grulla-phase123-optionals-v0.1.py`