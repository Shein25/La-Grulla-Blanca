# PRE-A08 V37 — Eco del Caído: recuperación auténtica E8 y nuevo gate T0

**Fecha:** 2026-10-09. **Estado:** RECUPERACIÓN DOCUMENTAL + LAB DIAGNÓSTICO PASS. **ELITE AÚN NO RATIFICADO / NO HTML / NO T1–T4**.

## Prioridad humana ya ratificada, no reabrir

El usuario aprobó el cierre numérico de los **seis monstruos normales de LianQi II** y los ajustes focales de **habilidades Viento**. Autoridad: `experimentos/balance_nuevo/handoffs/CIERRE_RATIFICADO_VIENTO_Y_NORMALES_2026-10-09/`. **Se conserva Sobretúnica de patrulla DEF+2 HP+2**. El nuevo frente exclusivamente trata al élite único `eco_caido`.

## Desbloqueo documental: seis cifras E8 recuperadas

El preflight anterior V36 advertía de la ausencia de `balance_t0_pendientes.py::config()['eco_caido']['E8']` y, por tanto, de la dificultad para reconstruir el descriptor completo. **Esa advertencia se mantiene para el script íntegro original**, pero encontramos las **seis estadísticas primarias exactas del candidato E8** en la rama Git **`handoff/lii-monsters-close-2026-10-08`**, archivo `experimentos/balance_nuevo/handoffs/CIERRE_LII_MONSTRUOS_2026-10-08/HANDOFF_LII_MONSTRUOS_2026-10-08.md`, blob **`a0ecb21dafe126d05d897349ee1889198b8c088b`**:

| Campo | E8 histórico |
|---|---:|
| HP | **84** |
| Precisión | **96** |
| Evasión | **18** |
| DEF | **1** |
| Tenacidad | **18** |
| Básico | **`1d2+4`** |

La fuente todavía NO verifica el valor de **Control** de E8. Tampoco prueba una técnica especial: el registro `monster_arc1_registry.json` mantiene `technique=null`, `stats_status=PENDING_INTEGRAL_REBALANCE`, `adaptive.status=BLOCKED_UNTIL_T0_READY` y `resource_model=NONE`. No escribir READY en el registro ni asignar T1/T2.

## Microbatería nueva V37: explícitamente provisional

Con motor de laboratorio histórico T0 (ETAPA19B, sin overlay aprobado V36 ni paridad productiva) usamos **las seis cifras documentadas** y heredamos del registro crítico 5% y multiplicador 1,5, con **`control=0` como supuesto DIAGNÓSTICO NO VERIFICADO**. Se valida `READY` solo en copia RAM para poder simular y no se altera el original.

Cinco raíces × 2 equipos **garantizados de forma condicional** (prologo, post M03) × 2 políticas (solo ofensiva, defensiva **hipotéticamente** conocida) × 128 semillas discovery y 128 holdout. **2.560 peleas nuevas DISCOVERY + 2.560 HOLDOUT = 5.120**. Repetición COLD **640 filas × 17 columnas exactas**, sin sumar casos nuevos; 0 timeouts. Archivo portable preserva código, tres CSV y cinco fuentes originales LAB con sus hashes.

| Raíz | WR jugador ofensiva | WR jugador defensiva hipotética |
|---|---:|---:|
| Fuego | 77,34% | 81,64% |
| Tierra | 67,19% | 82,81% |
| Agua | 50,78% | 71,88% |
| Metal | 57,03% | 69,53% |
| Viento | 51,95% | 53,91% |
| **Promedio equitativo** | **60,86%** | **71,95%** |

La campaña histórica independiente V02 (34.560 T0) había arrojado en E8 con equipo prólogo 63,02% / 70,94%. **No declarar paridad**: semillas y `config` históricos difieren; Control=0 no se ha demostrado original. Los valores V36 ratificados de Viento tampoco se aplicaron en el motor de esta microbatería.

Las 2.560 comparaciones pareadas PROLOGUE frente a POST-M03 (a igualdad de raíz, política y semilla) resultaron **idénticas en victoria y rondas**; el Qi final de post-M03 fue **+2** en todos los pares. Es un efecto del fixture, no garantía de irrelevancia del fajín en el juego.

## Verificación del encuentro real y bloqueo de progresión

En el HTML de referencia ver74 (Git blob `d34f7ea3f9de9344130aa072fac34d14a7a474d6`), `eco_caido` está listado como único en **`cruce_vetas`**, área `cantera_vetas`, sala `oculta:true`. El texto narrativo y la bandera `muerto_eco_caido` aluden a campo de entrenamiento y vena resentida de `veta_negra`. La cronología real (M03, LianQi II, permisos, habilidades accesibles) **NO está verificada**, ni las defensivas de la prueba están acreditadas. No editar `ROOMS.exits`, misiones, gates ni historia automáticamente.

## Puertas reales para aprobar E8

1. Recuperar script original `balance_t0_pendientes.py` con `E8` si existe; al menos verificar Control y paridad con `run_native.py`. No canonizar el supuesto 0.
2. Confirmar etapa y secuencia narrativa `cruce_vetas`; posesión verdadera de defensivas y equipo. No otorgar AOE LIII ni Ultimates por comodidad.
3. Integrar en **LAB** los cambios V17/V36 de Viento ya ratificados y medir contrafactuales comparables sobre E8 con cinco raíces. No reabrir normales.
4. Definir criterio humano de dificultad/recompensa para ELITE único; sólo entonces ratificar T0 y pasar a adaptación/paridad T1/T2.

## Paquete y guardias

ZIP **`GRULLA_PRE_A08_V37_ELITE_ECO_E8_DIAGNOSTICO_2026-10-09.zip`**; SHA256 **`93171fde83ad9e4263f239d7f8791f09802d793ae6093fd1b8565bb3df8fda2e`**, **21 archivos**, integridad CRC y SHA256 por archivo PASS. Reejecución COLD en carpeta nueva: 640 filas (17 columnas) idénticas byte a byte. Incluye runner, QA, análisis, RAW y 5 fuentes Python/JSON del motor LAB.

**Sin cambio a** `main`, merge, HTML, A07, `ROOMS.exits`, estadísticas canónicas, monstruos normales, Sobretúnica, comercio ni precios.
