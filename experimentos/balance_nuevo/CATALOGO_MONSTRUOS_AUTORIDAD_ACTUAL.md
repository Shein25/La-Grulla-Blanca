# AUTORIDAD ACTUAL — catálogo de monstruos de La Grulla Blanca

> **ENMIENDA URGENTE — 2026-10-10:** El índice V2 reúne **25 identidades verificadas, PERO NO es el total canónico definitivo**. Por confirmación humana, existen además **nuevos monstruos repetibles creados para LianQi III** que NO fueron incorporados aún porque faltan por recuperar sus IDs/nombres desde la fuente de creación. El total correcto queda **PENDIENTE**. Tanto «18 monstruos en total» como «25 monstruos en total» son afirmaciones inválidas. Las nuevas especies de LianQi II Y III forman parte del canon por decisión humana; la falta de identificación en el índice es una tarea de recuperación, no una exclusión.

**Decisión humana expresa:** 2026-10-10. **Estado:** CANÓNICO EN DISEÑO / REGISTRO MAESTRO DE IDENTIDADES.
**Fuente preferente para cualquier inventario:** [`CATALOGO_CANONICO_MONSTRUOS_ARCO1_V2.json`](CATALOGO_CANONICO_MONSTRUOS_ARCO1_V2.json).

## Derogación explícita del total histórico

La afirmación **«La Grulla Blanca tiene 18 monstruos en total» queda DEPRECADA**. No debe repetirse en nuevos handoffs, prompts, balances, auditorías, integraciones o listados como si fuera la situación actual.

El antiguo `monster_arc1_registry.json` con `rules.profile_count=18` es un **snapshot histórico parcial**, válido ÚNICAMENTE como fuente de sus perfiles numéricos/identidades originales y las decisiones T0 antiguas. **NO ES EL CATÁLOGO COMPLETO VIGENTE.** No editar sus valores aprobados solo para corregir el total; deben preservarse hashes e historia del balance.

Se reconoce canónicamente la incorporación de **seis monstruos repetibles nuevos** creados y aprobados para LianQi II en V35 y **un guardián nuevo** de LianQi III con identidad humana aprobada. hay **25 IDs verificados hasta ahora (total incompleto)**: 18 + 6 + 1. Los futuros monstruos que se creen, ratifiquen y documenten deben agregarse a ese índice y elevar la cuenta; **25 tampoco es un máximo fijo de diseño**.

## Seis perfiles LianQi II incluidos como canon

| Nombre aprobado | ID estable | Estado de balance |
|---|---|---|
| Jabalí de Pizarra | `jabali_pizarra` | V35 ratificado; integración HTML pendiente |
| Búho de la Niebla Gris | `buho_niebla_gris` | V35 ratificado; integración HTML pendiente |
| Zorro de los Bancales | `zorro_bancales` | V35 ratificado; integración HTML pendiente |
| Cangrejo del Cauce Pétreo | `cangrejo_cauce` | V35 ratificado; integración HTML pendiente |
| Murciélago Resonante | `murcielago_resonante` | V35 ratificado; integración HTML pendiente |
| Araña de la Veta Sombría | `arana_veta_sombria` | V35 ratificado; integración HTML pendiente |

**Autoridad numérica:** `experimentos/balance_nuevo/handoffs/CIERRE_RATIFICADO_VIENTO_Y_NORMALES_2026-10-09/DECISION_HUMANA_CIERRE_LII_NORMAL_Y_VIENTO_2026-10-09.json` en rama `experiment/lii-tramo1-multirraiz-v08-2026-10-08`.

## Incorporación LianQi III como identidad canónica

**El Custodio del Eco Pétreo**, ID `custodio_eco_petreo`, guardián único AOE de Tierra. Su **nombre e ID**, y el diseño de aparición legal en LianQi III, están ratificados. No se fingen T0 canónico, spawn, sala realmente integrada ni manual en runtime. `bosque_rocas_blancas` sigue siendo **sala propuesta**. Autoridad previa `experimentos/balance_nuevo/adaptive_six_revalidation_v0.1/DECISION_HUMANA_GUARDIANES_AOE_IDENTIDADES_UBICACIONES_2026-10-07.md`.

Los anteriores perfiles `pez_lunar`, `anguila_estelar` y `sombra_ahogada` **siguen formando parte del canon** como criaturas nativas LianQi III en el índice. No se los elimina ni modifica al incluir nuevos monstruos.

## Obligaciones de uso del índice

1. **Inventarios/cuentas:** leer primero el JSON canónico V2, no `rules.profile_count=18`.
2. **Balance:** resolver la ficha de la especie en su autoridad numérica (original histórico para antiguos; V35 para seis nuevos). El índice no altera daño, defensa, resistencia, equipo, recompensas ni adaptación.
3. **Etapa:** `native_stage` histórico no implica etapa legal de aparición. Los guardianes de manual son encuentros de LianQi III independientemente de etiquetas heredadas.
4. **Únicos:** `unique=true` significa identidad única; no darles adaptación persistente T1–T4 ni respawn. No confundir Centinela de plumas con Custodio.
5. **Runtime:** canon de diseño no certifica implementación en HTML; mapear ID/spawn/ROOM/gate/recompensa antes de afirmar que la criatura aparece efectivamente.
6. **AOE:** al probar LianQi III, incluir especies nuevas de LII si hay acceso legal a las salas y los grupos reales existen. No inventar spawns ni combates multiblanco.
7. **Handoff:** toda nueva conversación/agente/Astra debe citar el JSON V2 como referencia vigente y marcar el inventario de 18 como `LEGACY_DEPRECATED_COUNT`.

## Límites
Esta ratificación no autoriza modificar `main`, hacer merge, escribir runtime HTML, alterar los cuatro T0 congelados, abrir especies numéricamente cerradas ni inventar perfiles sin origen documental. **Se aprobó el catálogo de identidades y la vigencia de los seis LII; la integración sigue siendo trabajo independiente.**
