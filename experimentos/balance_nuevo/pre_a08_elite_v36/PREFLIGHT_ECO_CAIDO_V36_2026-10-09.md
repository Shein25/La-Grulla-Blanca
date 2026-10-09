> **ACTUALIZACIÓN VERIFICADA V37 (2026-10-09):** el preflight V36 quedó parcialmente superado. Se recuperaron las seis estadísticas numéricas del E8 histórico desde la rama `handoff/lii-monsters-close-2026-10-08` (HP 84, PREC 96, EVA 18, DEF 1, TEN 18, básico `1d2+4`). El archivo original `balance_t0_pendientes.py::config()['eco_caido']['E8']` y el dato de **Control** siguen sin recuperarse, por lo que el descriptor E8 íntegro **NO** es reproducible con exactitud. V37 ejecutó 5.120 duelos T0 diagnósticos (`Control=0` expresamente hipotético), sin ratificar E8 ni alterar el registro. **Fuente actualizada:** [V37](../pre_a08_elite_v37/DICTAMEN_ELITE_E8_V37_2026-10-09.md). Este aviso prevalece sobre las frases posteriores que afirman que no se dispone de ninguna estadística E8.

# V36 — Apertura de balance élite: Eco del Caído (LianQi II)
**2026-10-09. Estado:** PREFLIGHT PASS / datos históricos T0 revalidados / ELITE NUEVO NO SIMULADO / SIN FREEZE NI RUNTIME. Los seis monstruos normales LII quedaron cerrados en V35 y no se reabren.

## Identidad y autoridad numérica
Registro de fuente `monster_arc1_registry.json` del paquete LAB V34: **`eco_caido`**, `role=ELITE`, `native_stage=LianQi_II`, `unique=true`, región `cantera_vetas`; **`stats_status=PENDING_INTEGRAL_REBALANCE`**, HP/precisión/evasión/DEF/etc. principales `null`, `technique=null` y `adaptive.status=BLOCKED_UNTIL_T0_READY`. No está habilitado para T1–T4. El élite `sombra_ahogada` corresponde a LianQi III y queda aparte. `sapo_caldera` y `rey_escarabajo` son jefes de LianQi II, no este frente élite.

## Histórico útil encontrado y verificado
Del backup total pre-A08 se recuperó **`GRULLA_ECO_CAIDO_T0_V02_AUDITORIA_2026-10-08.zip`** con `RUN.csv`, 34.560 duelos **HISTÓRICOS T0**, comparando Eco E5/E7/E8/E9 y dos controles READY. Procedencia fuente motor commit **`9a6baa41bd6fc505a755a474cd4f64a2522ba0b9`**. El `RUN.csv` tiene SHA256 **`0cfc2c7c5c97f4ff73748eb4d888b016f895a06d195140d565fc2aba197da290`**, mismo que el reporte previo; 0 timeouts y 0 IDs de pelea duplicados. Un script nuevo `audit_elite_historical_v36.py` recalculó sus agregados. Esos 34.560 casos **no se presentan como simulaciones nuevas**.

El histórico dejó **E8 como candidato T0 preferente pero NO ratificado**. Equipo del prólogo garantizado, 960 peleas por política:
| Política del fixture | WR jugador E8 |
|---|---:|
| `UNITARGET_FIRST` solo ofensiva | **63,02 %** |
| `DEFENSE_OPEN` con técnica defensiva hipotética | **70,94 %** |

Contra controles reales de la misma campaña y equipo: Sapo Ceniza **80,31 / 85,42 %**, Escarabajo Hierro **51,35 / 59,06 %** (solo ofensiva / defensiva). E8 intermedio en ese laboratorio, sin asumir que eso determina una dificultad humana correcta para un élite único.

**Por raíz, E8 con equipo del prólogo**:
| Raíz | Solo ofensiva | Defensa hipotética |
|---|---:|---:|
| Fuego | 82,81 % | 85,94 % |
| Tierra | 67,19 % | 81,77 % |
| Agua | 57,29 % | 61,98 % |
| Metal | 51,56 % | 66,67 % |
| Viento | **56,25 %** | **58,33 %** |

El fajín M03 mejoró Qi bruto, pero NO cambió victorias en las políticas de ese T0 histórico. No extrapolar a técnicas defensivas reales ni avanzar una fase de progresión por ello.

## Bloqueo real del nuevo laboratorio
El ZIP V02 trae runner y resultados, pero ese runner importa `balance_t0_pendientes.py::config()['eco_caido']['E8']` y `run_native.py`, **ausentes del paquete** y usa rutas locales absolutas; por eso puede auditarse el historial, pero **no reproducirse integralmente desde ese ZIP** ni disponer del descriptor numérico E8 a partir de sus filas. No inventar una copia aproximada de HP/ataque/DEF/precisión. Tampoco convertir un perfil `PENDING` a READY sin descriptor y contrato.

## Primer gate del frente elite (no repetir campañas)
1. Recuperar el descriptor E8 numérico auténtico de su fuente original, con commit y SHA de autoridad, antes de escribir simulador T0 nuevo.
2. Verificar **cuándo se enfrenta al Eco** (el informe V02 lo sitúa en Cruce de las Vetas y notaba desajustes narrativos entre otras salas/flags); comprobar equipo y técnicas defensivas verdaderamente disponibles **en ese momento**. No alterar exits, misiones ni historia automáticamente.
3. Ejecutar solo los escenarios T0 que **no** quedaron cubiertos por las 34.560 peleas históricas, con controles READY, cinco raíces y comparación pareada, respetando recompensa por progresión.
4. Tras ratificar T0 humano, comprobar la integración del motor nuevo y únicamente entonces adaptar T1–T2. No mezclar el minijefe con los seis normales ya cerrados, jefes o el élite LIII.

## Reproducibilidad
Paquete portátil V35 + preflight V36: `GRULLA_PRE_A08_V35_CIERRE_NORMALES_Y_PREFLIGHT_ELITE_2026-10-09.zip` SHA256 `bb944e145d39a23ef9d106b39bcca33fafd13c31abf32ef28814ec0199fe2a7a`; 63 entradas, CRC/manifiesto PASS y nueva extracción seguida de `audit_elite_historical_v36.py` PASS. Incluye el ZIP T0 histórico intacto, tablas E8 por raíz/equipo, controles y QA del material previo.

**Guardias:** no main, no merge, no HTML, no A07, no `ROOMS.exits`, no ajustes a piezas equipables, no cambio a comercio/precios, no modificación canónica de monstruos.
