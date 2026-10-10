# LianQi III — monstruos pendientes y pruebas POST_AOE

> **AUTORIDAD CANÓNICA NUEVA V3 (2026-10-10):** el inventario **vigente verificado es 31 identidades**: 18 perfiles históricos + seis repetibles nuevos LII (V35) + seis repetibles nuevos LIII (V45/V46) + `custodio_eco_petreo` único. La cifra **18 como total** y el índice incompleto V2 de **25** quedan **DEPRECADOS**. Fuente obligatoria: `experimentos/balance_nuevo/CATALOGO_CANONICO_MONSTRUOS_ARCO1_V3.json` y `experimentos/balance_nuevo/CATALOGO_MONSTRUOS_AUTORIDAD_ACTUAL.md`. Nuevas seis LIII: `garza_bruma_roca`, `cangrejo_laja_humeda`, `sanguijuela_remanso_turbio`, `salamandra_filtracion_tibia`, `rana_cascajo_barranco`, `carpa_lamina_reflejo`. Canon de diseño V46; T0 numérico y T1–T4 siguen propuestos.




**Fecha:** 2026-10-10. **Estado:** AUDITORÍA DE ALCANCE Y PLAN, sin nuevas cifras de monstruo, sin simulaciones AOE cerradas.
**Autoridad de registro consultada:** `experimentos/balance_nuevo/monster_arc1_registry.json` en commit `45c3a9c240ea74208a0d8fd4d5be187bc817df35` (snapshot histórico T0). `native_stage` es etiqueta de perfil **NO prueba de acceso geográfico/legal al encuentro**.

## 1. Monstruos de etapa LianQi III fuera del cierre de cinco guardianes

| ID exacto | Nombre / clase | T0 histórico | Ataque principal y prioridad AOE | Decisión |
|---|---|---|---|---|
| `pez_lunar` | pez de luna sin ojos / NORMAL | `READY`; adaptación `T0–T4 CLOSED` | `Mordida de Corriente` daño directo; evasión elevada 29, DEF 2 | **Pendiente** validar impactos independientes y estrategia vs AOE; no cambiar T0 sin fallo acreditado |
| `anguila_estelar` | anguila de constelación rota / SKIRMISHER | `READY`; adaptación `T0–T4 CLOSED` | `Mordida del Meridiano Azul` daño directo + drenaje Qi 6; EVA 36 | **Pendiente** interacciones de AOE con drenaje de Qi y ventanas de energía; no buff a ciegas |
| `sombra_ahogada` | sombra ahogada del estanque / ELITE única | `READY`; `UNIQUE_T0_CLOSED_NO_T1_T4` | `Velo de Ahogo`: Veneno 1d2+2 ×3, cadencia 3 | **Pendiente** AOE contra objetivo único (×0,65) y persistencia Veneno; inmunidad a Hemorragia anatómica solo como hipótesis a ratificar |

### Exclusiones obligatorias
- `sapo_caldera`, `rey_escarabajo`, `guardian_coral` y `mantis_nube` son **guardianes de manual AOE legalmente en LIII**, independientemente de `native_stage` viejo; el quinto `custodio_eco_petreo` es guardián conceptual con T0/spawn canónico pendientes. **No contarlos como 3 monstruos adicionales sin cerrar**.
- `centinela_pluma`, `devorador_niebla` y `halcon_tormenta` figuran en el snapshot con `native_stage=LianQi_IV`, y `centinela_pluma` NO es el Custodio de Tierra. No desplazarlos artificialmente a LIII.
- Otros monstruos de LII/I solo se ensayarán si el Atlas y las reglas de acceso existentes demuestran que hay enfrentamientos POST_AOE relevantes; no crear nuevos spawns o mezclas como si existieran en runtime.
- El registro histórico no prueba que el T0 necesite **modificación numérica**: lo pendiente es **auditoría de interacción AOE y dificultad**. Reabrir freezes T0–T4 exige evidencia causal y decisión humana.

## 1 bis. CORRECCIÓN DE ALCANCE — seis monstruos repetibles NUEVOS omitidos

**Corrección del 2026-10-10, por advertencia expresa del usuario.** La tabla del §1 estaba incompleta como universo de pruebas POST_AOE: se consultó solo el registro histórico de **18 monstruos**, que NO incluye los seis perfiles normales nuevos del frente PRE-A08. Son **repetibles del ámbito de LianQi II**, con balance numérico **ratificado el 2026-10-09**: NO se deben reetiquetar falsamente como perfiles nativos de LianQi III. Sí deben formar parte del **inventario de enemigos existentes a contrastar** cuando el jugador alcance LianQi III y pueda volver a sus ubicaciones, condicionado a comprobación real de ROOM/spawn/acceso.

| ID exacto nuevo | Nombre | Etapa de balance / estado | Interacción POST_AOE por revisar |
|---|---|---|---|
| `jabali_pizarra` | Jabalí de Pizarra | LII repetible, V35 ratificado | embestida y mitigación T1 ante AOE |
| `buho_niebla_gris` | Búho de la Niebla Gris | LII repetible, V35 ratificado | precisión, evasión y lectura de ataque AOE |
| `zorro_bancales` | Zorro de los Bancales | LII repetible, V35 ratificado | evasión 21, oportunidad de esquivar por objetivo |
| `cangrejo_cauce` | Cangrejo del Cauce Pétreo | LII repetible, V35 ratificado | defensa y mitigación reactivas al daño AOE |
| `murcielago_resonante` | Murciélago Resonante | LII repetible, V35 ratificado | drenaje Qi 6 versus coste único de una AOE |
| `arana_veta_sombria` | Araña de la Veta Sombría | LII repetible, V35 ratificado | Veneno y DOT, no multiplicar eventos por objetivo |

**Fuente humana y numérica:** `experimentos/balance_nuevo/handoffs/CIERRE_RATIFICADO_VIENTO_Y_NORMALES_2026-10-09/DECISION_HUMANA_CIERRE_LII_NORMAL_Y_VIENTO_2026-10-09.json` y `experimentos/balance_nuevo/pre_a08_cierre_normales_v35/FINAL_NUMERIC_TARGETS_SIX_NORMALS_V35.json`; rama `experiment/lii-tramo1-multirraiz-v08-2026-10-08`. Esos seis NO están añadidos al `monster_arc1_registry.json` de 18 perfiles, así que su ausencia allí **no los elimina del proyecto**.

**Inventario corregido, excluidos los cinco guardianes:** 3 perfiles nativos LIII (Pez, Anguila y Sombra; 2 repetibles + 1 única) **más 6 repetibles recientes de LII a auditar como encuentros potencialmente accesibles desde LIII**. En total son **9 perfiles distintos para preflight POST_AOE**, pero la legalidad de los seis encuentros de arrastre sigue **POR VERIFICAR**. Otros repetibles LII/LI previos también requieren barrido de acceso si sus zonas permanecen abiertas: no declarar esta lista exhaustiva de TODO Arco 1.

No repetir balance ya cerrado de LII ni actualizar T0 o HTML al agregar cobertura de pruebas.


## 1 ter. SEIS NUEVOS REPETIBLES PROPIOS DE LIII — V45/V46 RECUPERADOS Y CANÓNICOS

Los siguientes seis **sí fueron creados y aprobados específicamente para LianQi III**, según documentación original V45/V46 ahora preservada en esta rama. La identidad y diseño son canónicos, mientras que **sus T0 numéricos V45 y T1–T4 V46 siguen como propuestas hasta ratificación específica**. El registro antiguo de 18 no los contenía:

| ID | Especie | Mecánica para ensayar con AOE |
|---|---|---|
| `garza_bruma_roca` | Garza de Bruma de Roca | EVA/Precisión, tirada independiente por blanco |
| `cangrejo_laja_humeda` | Cangrejo de Laja Húmeda | DEF alta/Tenacidad y penetración AOE |
| `sanguijuela_remanso_turbio` | Sanguijuela de Remanso Turbio | Veneno y eventos DOT independientes |
| `salamandra_filtracion_tibia` | Salamandra de Filtración Tibia | Quemadura, Absorción y DOT por entidad |
| `rana_cascajo_barranco` | Rana de Cascajo del Barranco | Daño directo sostenido |
| `carpa_lamina_reflejo` | Carpa de Lámina Reflejada | Drenaje de Qi y pago único AOE |

Fuente sellada en Git de V45 y V46: `FUENTE_IMPORTADA_V45_NUEVA_FAUNA_LIII_2026-10-09.md`, `FUENTE_IMPORTADA_V46_CADENA_ADAPTATIVA_LIII_2026-10-09.md`. Para estas especies, **12 salas son planes de colocación**, no apariciones productivas. NO declarar ninguna prueba multiblanco ejecutada con estos perfiles.

**Cobertura primaria actualizada:** 8 repetibles nativos LIII (Pez + Anguila + 6 nuevos), Sombra única LIII, y 6 repetibles LII nuevos cuya disponibilidad en etapa superior debe verificarse = **15 identidades prioritarias POST_AOE**, sin contar otros repetibles anteriores ni cinco guardianes. Esto es una lista de focos, no autorización de spawns. El índice maestro V3 contiene 31 identidades globales.

## 2. Contrato AOE obligatorio

Fuentes:
- `docs/experimentos/CONTRATO_COMBATE_ESTADISTICAS_DOT_V0_1.md` + `docs/experimentos/CONTRATO_MOTOR_EVENTOS_EFECTOS_V0_1.md`.
- `experimentos/balance_nuevo/handoffs/V66_GUARDIANES_AOE_2026-10-10/HANDOFF_V66_COMPLETO_2026-10-10.md`.

Separar dos etapas:
1. **PRE_AOE**: LianQi III antes del manual obtenido del guardián. Ningún personaje usa esa AOE. El duelo para obtener el manual no puede contar como POST_AOE.
2. **POST_AOE**: manual legalmente ganado una vez y técnica aprendida. Usar realmente sus costes, disponibilidad y adquisiciones; no regalar manual/maestría. La única Ulti de raíz principal se rige por decisión V67 separada.

Al ejecutar una AOE:
- Con **un solo enemigo hostil real** en el alcance: **×0,65 del daño directo AOE antes de DEF**, incluso si ese único enemigo es un jefe o élite.
- Con **dos o más enemigos hostiles reales**: factor **×1 por objetivo** y sin reparto, **un único gasto de Qi por ejecución**.
- **Cada objetivo** resuelve su propia Precisión/Evasión, DEF, Absorción, Control, estados y fuentes de DOT. No multiplicar alcance ni gasto por número de impactos. Conservar `ON_HP_DAMAGE` al determinar si abre Hemorragia.
- Sin blancos extras inventados, sin atracción entre habitaciones, sin afectación de aliados o neutrales no declarada por la técnica; el número de hostiles debe ser el legalmente presente.
- Hemorragia se activa con **acción voluntaria individual**, no al inicio de turno ni por perder turno bajo Control. Quemadura/Veneno conservan sus propios eventos. No crear ticks duplicados al haber varios objetivos.
- Cualquier Eco, Concordancia y efecto especial sigue la autoridad de eventos: no multiplicar por N un evento que contractualmente ocurre una sola vez.

## 3. Matriz mínima de comprobación real

| Eje | Casos obligatorios | Qué demuestra |
|---|---|---|
| Fase de progresión | PRE_AOE, POST_AOE con manual legal, intento sin manual | gate sin acceso gratuito |
| Cantidad de enemigos | 1, 2 y 3+ SOLO si hay composición existente verificada; fixtures sintéticos marcados como tales | x0,65 vs x1; un pago de Qi |
| Raíz | Fuego, Metal, Agua, Tierra, Viento | cinco AOE propias y Concordancias legales |
| Perfil | `pez_lunar`, `anguila_estelar`, `sombra_ahogada`; LII accesibles si procede | DEF/EVA, drenaje Qi, Veneno |
| Motor/IA | T0 y tiers legalmente desbloqueados de repetibles; élite única solo T0 | no aplicar adaptación T1–T4 a la sombra |
| Equipo/experiencia | equipamiento realmente alcanzable, 3 builds LIII y políticas autorizadas | no inflar monstruos por equipo hipotético |
| Recursos/aflicciones | impacto conectado/fallido, absorción, muerte parcial, estados de acción | independencia por blanco |
| Resultado | victoria, derrota, HP/Qi final, TTK, daño directo y DOT por objetivo, elección y prioridad IA | balance y trazabilidad |

### Pruebas adversariales de aceptación
A. AOE contra un solo `pez_lunar`: aplicar ×0,65 **antes** de DEF, con evasión por tirada.
B. AOE contra dos hostiles **solo en fixture identificado o ubicación verificada**: ambos reciben ×1, Qui una sola vez y tiradas separadas.
C. `anguila_estelar` reduce el Qi del personaje según su habilidad; NO se le atribuye AOE al monstruo si el catálogo solo declara DIRECT+QI_DRAIN.
D. `sombra_ahogada` aplica Veneno según su contrato y no adquiere T1–T4; bajo Control no duplicar ni omitir ticks incorrectamente.
E. Un enemigo muere por AOE y otro sobrevive: persistencia/target-list/AI estables; no segunda activación ni XP/drop duplicado.
F. Sin manual, comando AOE rechazado **sin consumir Qi ni acción** salvo que el contrato de intento fallido indique otra cosa.
G. AOE + Ulti principal con máximo una Ulti por pelea (la AOE es técnica normal, no debe gastar el cupo de Ulti).

## 4. Orden de ejecución recomendado — SIN inventar resultados
1. Auditar código exacto de cinco AOE, spawn/ROOM existentes y llegada legal a ocho repetibles LIII (Pez, Anguila, seis V45), Sombra única, además de los seis LII de V35 si corresponde.
2. Certificar eventos y pruebas unitarias 1/2/3 objetivos; comparar el resolver unitarget con AOE.
3. Recién entonces simular POST_AOE por monstruo/raíz/build/equipo/política con seeds pareadas y desgloses de daño/IA.
4. Ampliar el cruce también a los seis repetibles nuevos ratificados LII si sus encuentros se comprueban accesibles en LIII. Proponer ajustes **solo** cuando un fallo/imbalance esté demostrado; conservar T0–T4 congelados y élite T0 si funcionan.
5. Preparar integración Astra A08 sin tocar `main` o HTML durante investigación.

**Estado actualizado:** 31 identidades globales en V3; para la campaña POST_AOE hay 15 perfiles prioritarios (9 nativos LIII y seis LII de V35 bajo verificación de acceso). **Ningún resultado multiblanco real se ha ejecutado ni ratificado.**
