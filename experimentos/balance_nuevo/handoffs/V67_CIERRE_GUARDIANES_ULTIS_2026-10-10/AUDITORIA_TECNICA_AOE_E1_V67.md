# Auditoría inicial de integración AOE × monstruos LianQi III

> **AUTORIDAD CANÓNICA DE MONSTRUOS (2026-10-10):** el inventario histórico de **18** se encuentra **DEPRECADO COMO TOTAL**. Usar siempre `experimentos/balance_nuevo/CATALOGO_CANONICO_MONSTRUOS_ARCO1_V2.json` y `experimentos/balance_nuevo/CATALOGO_MONSTRUOS_AUTORIDAD_ACTUAL.md` (25 identidades verificadas = 18 históricas + seis repetibles LII V35 + Custodio LIII). Las menciones a «registro de 18 perfiles» solo identifican la fuente numérica histórica, nunca el catálogo total válido. No reabrir T0 por esta incorporación.

**Fecha:** 2026-10-10. **Estado:** PRECHECK_DE_FUENTES, **NO** simulación AOE multiblanco ni balance validado.

## 1. Hallazgo limitante demostrado en las fuentes V66
Se inspeccionó el ZIP V66 sellado, específicamente `V66/sources/physical_source/source_lab/etapa19b_combat_engine.py` y `techniques_arc1_catalog.json`.

- Encabezado del motor: **«motor unificado 1v1»**; `FightState` contiene `monster` singular.
- `resolve_player_direct(...)` obtiene `m=state.monster` y usa `c["aoe_scalar"]` como multiplicador de ese impacto individual. No hace un bucle sobre blancos distintos.
- `execute_player_technique(...)` llama una sola vez a `resolve_player_direct`; `fight_once` termina cuando muere **ese** monstruo.
- `choose_player_action(..., "AOE_FIRST")` sí selecciona la AOE, pero **no verifica en ese runner** que el jugador posea el manual ya ganado. El test necesita gate externo para ser legal.
- Las cinco fichas AOE del catálogo provisional usan `aoe_single_target_scalar=0.65`, coste nominal base `9 Qi` (excepto modificadores por raíz/nodo aplicables, ej. Agua). Son: `circulo_cien_ascuas`, `lluvia_filos`, `marea_ocho_orillas`, `temblor_montana`, `tijera_vendaval`.

**CONCLUSIÓN:** E1 sí permite estudiar POST_AOE **contra un solo blanco** en un fixture con manual/maestría demostrados, pero **no** permite inferir resultados de 2+ monstruos ni cumplir automáticamente factor x1 y un único Qi. No adjudicar victorias multiblanco a V67. Hace falta un resolver multiblanco legal y validado (Astra/integración); este frente no lo implementó.

## 2. Otro hallazgo: deriva de fuente de registro
- El `monster_arc1_registry.json` incrustado en el ZIP original V66 (**snapshot anterior**) marca `pez_lunar`, `anguila_estelar`, `sombra_ahogada` como `PENDING_INTEGRAL_REBALANCE` y tiene `null` en sus estadísticas/T0.
- El registro histórico de autoridad en commit `45c3a9c240ea74208a0d8fd4d5be187bc817df35`, blob `0261dd2b254ee0db0d28256b37e54fd7756790c7`, los declara **READY** con T0 numérico. En Pez/Anguila indica `T0–T4 CLOSED`; en Sombra `UNIQUE_T0_CLOSED_NO_T1_T4`.
- Por ello, un intento directo de `fight_once` con el registro embebido V66 **es rechazado correctamente** por la guarda de T0 no READY. No remendar mediante estadísticas inventadas ni declarar «monstruos pendientes de balance» por ese snapshot obsoleto.
- El test AOE siguiente debe **fijar la fuente correcta del registro**, comparar hashes, y documentar qué código/depencias correspondan a ella, sin editar los T0 aprobados.

## 3. Pruebas requeridas antes de calificar la interacción
1. Implementar/parificar ruta real de AOE multiblanco, sin escribir en main/HTML: un único Qi, 1 acción, eventos independientes por objetivo, factor x0.65 para 1 enemigo, x1 para >=2; 0 nuevos spawns.
2. Verificar gate legal `POST_MANUAL_AOE` y 4 PT de LIII; no usar la técnica en el combate `PRE_AOE` que entrega su manual.
3. Seleccionar enfrentamientos realmente posibles según salas y reglas de aparición: **no deducir multienemigo por compartir `region`**; grupo sintético solo con etiqueta `FIXTURE_NOT_RUNTIME`.
4. Probar Pez, Anguila y Sombra por separado antes de los grupos; desglosar Veneno, drenaje Qi, precisión/evasión y memoria/IA según contratos.
5. Si se incluye Ulti, aplicar únicamente raíz principal legal y máximo una por combate; la técnica AOE no consume la cuota de Ulti.
6. Comparar resultados sin AOE vs con AOE para uno/dos/múltiples objetivos en mismas semillas; revisar AI del monstruo tras recibir AOE, supervivencia y telegráficos.

**Estado real al cierre:** cero combates POST_AOE multiblanco ejecutados; no modificaciones ni propuestas numéricas autorizadas para los tres monstruos. El trabajo previo V65–V67 de guardianes fue **PRE_AOE 1v1**, por lo que no responde esta pregunta.

## 4. Corrección de alcance de monstruos nuevos (2026-10-10)
El apartado 2 enumera correctamente tres perfiles **nativos LIII del registro histórico**, pero era incorrecto utilizarlo como inventario general de enemigos POST_AOE. Los **seis repetibles nuevos de LII ratificados en V35** no aparecen en el registro de 18 perfiles: `jabali_pizarra`, `buho_niebla_gris`, `zorro_bancales`, `cangrejo_cauce`, `murcielago_resonante`, `arana_veta_sombria`. Se agregan al preflight de enfrentamientos del jugador LIII **sujeto a verificar spawn y acceso a las salas existentes**, sin declararlos nativos LIII, sin inventar combates y sin reabrir los seis balances LII. Fuente: `experimentos/balance_nuevo/handoffs/CIERRE_RATIFICADO_VIENTO_Y_NORMALES_2026-10-09/DECISION_HUMANA_CIERRE_LII_NORMAL_Y_VIENTO_2026-10-09.json`. Ver corrección detallada en `PENDIENTES_LIII_Y_AOE_POST_MANUAL.md`.
