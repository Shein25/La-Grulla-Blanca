# DECISIÓN HUMANA — Guardianes únicos de AOE (Arco 1)

**Fecha:** 2026-10-07  
**Ámbito:** memoria durable de diseño y autoridad para laboratorios futuros; **NO es implementación ni freeze numérico nuevo**.  
**Decisión expresa del autor:** RATIFICAR el nombre **El Custodio del Eco Pétreo** para el guardián de Tierra que faltaba. Adoptar el identificador de diseño `custodio_eco_petreo`.

## 1. Identidades y salas — NO perder al avanzar de etapa

| Raíz | ID de guardián | Nombre | Sala actual documentada | Cambios de ubicación | AOE vinculada |
|---|---|---|---|---|---|
| Fuego | `sapo_caldera` | Sapo Caldera de Tres Gargantas | `camara_caldera` | Conservar | Círculo de las Cien Ascuas |
| Metal | `rey_escarabajo` | Rey Escarabajo de la Veta Negra | `nido_escarabajos` | Conservar | Lluvia de Filos |
| Agua | `guardian_coral` | Guardián de Coral Memorioso | `aguas_rama_oscura` | Conservar (NO `aguas_camara_hidrica`) | Marea de las Ocho Orillas (en catálogo experimental; el runtime histórico nombra su entrada `marea_circular`) |
| Viento | `mantis_nube` | Mantis de Nube Cortante | `alturas_senda_mantis` | Propuesta aceptada para futura reubicación `bosque_corredor_viento`; aún NO implementada | Tijera del Vendaval Partido |
| Tierra | **`custodio_eco_petreo`** | **El Custodio del Eco Pétreo** | **NO tiene spawn en runtime** | **`bosque_rocas_blancas`** es la ubicación preferida de diseño; asignación real pendiente de Astra/integración autorizada | Temblor de Montaña |

**Sentencia de autoridad:** el nombre y el ID de diseño del custodio de Tierra quedaron aprobados por el autor en esta conversación; no sustituirlo, no inventar otro jefe, no marcar un spawn inexistente como implementado. La propuesta de ubicación queda preservada como preferencia, no como hecho productivo confirmado.

## 2. Estado real de combate y fuente correcta

**CUATRO ÚNICOS CON T0 RATIFICADO EN FUENTE HISTÓRICA:**
- Fuente de cierre de únicos: Git commit `45c3a9c240ea74208a0d8fd4d5be187bc817df35`, archivo `experimentos/balance_nuevo/monster_arc1_registry.json`, blob `0261dd2b254ee0db0d28256b37e54fd7756790c7`.
- `sapo_caldera`: HP 83; técnica «Eructo del Horno Hundido»; `stats_status=READY`; `adaptive.status=UNIQUE_T0_CLOSED_NO_T1_T4`.
- `rey_escarabajo`: HP 87; técnica «Mandíbula de Yunque»; READY / UNIQUE_T0_CLOSED_NO_T1_T4.
- `guardian_coral`: HP 80; técnica «Marea de los Nombres Hundidos»; READY / UNIQUE_T0_CLOSED_NO_T1_T4.
- `mantis_nube`: HP 72; técnica «Tijera del Horizonte»; READY / UNIQUE_T0_CLOSED_NO_T1_T4.

**IMPORTANTE — DRIFT DOCUMENTAL REAL:** en la rama `experiment/monster-adaptive-six-revalidation-v0.1` el mismo registro `monster_arc1_registry.json` (blob `c0d2131f2cc8dbbb96babf9711c197e54fe97591`) es un snapshot ANTERIOR que aún etiqueta estos cuatro jefes `PENDING_INTEGRAL_REBALANCE` y `BLOCKED_UNTIL_T0_READY`. **NO CONCLUIR que el T0 ratificado no existe a partir de esa rama antigua.** No se modifica automáticamente el registro antiguo: futuros laboratorios fijan explícitamente fuente de únicos ratificada y solicitan decisión si surge conflicto.

**Tierra** `custodio_eco_petreo`: **SIN T0 NUMÉRICO**, sin parámetros exactos, sin manual de runtime, sin spawn, sin ensayos; no heredar estadísticas de otro jefe ni marcar READY.

## 3. Reglas duras ratificadas para todos los Guardianes AOE

1. **Jefes únicos; una sola derrota por partida; sin respawn.** El T0 de los cuatro históricos es autoridad ratificada; NO les aplicar automáticamente adaptación persistente T1/T2/T3/T4 de monstruos repetibles.
2. Se perciben/materializan legalmente desde **LianQi III**, tras conectar el gate de cultivo NEW. Diferenciar percepción, spawn real, combate y entrega de recompensa.
3. **Sin fases de jefe.** Kit y mecánica continua propia, telegráfica, contra-jugable; no resolverlo inflando HP arbitrariamente. No atribuir capacidad ya implementada a recetas conceptuales.
4. Encuentro anclado a la sala; **sin atracción entre salas**. Huida/abandono reinicia encuentro completo; muerte confirmada no respawnea. No tocar `ROOMS.exits` ni otros gates.
5. Recompensa/manual AOE una sola vez, entrega idempotente; el jugador debe derrotar legalmente al guardián y aprender el manual para tener la AOE. **PRE-GUARDIAN LIII: sin esa AOE. POST-GUARDIAN LIII: con esa AOE**.
6. **Benchmark principal de obtención:** jugador LianQi III `PRE_AOE + MAIN_ROOT_ULTI_READY`, **una Ulti por combate**, brazo control `NO_ULTI`. Validar burst legal de 1/2/3 acciones, mecánica de encuentro y duración sin inmunidad artificial. 
7. **El catálogo experimental y las tablas del runtime histórico pueden usar IDs/nombres diferentes.** Ejemplo Agua: `manual_marea_circular → marea_circular` en ver76 frente a `marea_ocho_orillas` en catálogo. No inventar una equivalencia de migración/runtime sin auditoría de Astra.
8. Ubicaciones históricas Sapo/Rey/Coral se conservan; mover Mantis y materializar Tierra sólo mediante una futura implementación expresamente autorizada. No modificar el grafo/Atlas/extracción como efecto colateral.

## 4. Estado de las mecánicas del jefe

Astra auditó en `AUDITORIA_VIABILIDAD_GUARDIANES_AOE.md` (2026-10-05) recetas conceptuales:
- Sapo: respiración/carga y ventana de vulnerabilidad;
- Rey: placas defensivas que pueden abrir exposición;
- Coral: memoria local finita dentro de la pelea;
- Mantis: alternancia de corte/evasión;
- Tierra: resonancia acumulada y descarga anunciada.

Estos son **conceptos VIABLES, no kits cuantificados ni tests funcionales aprobados**. Hay que establecer detalles con autoridad humana y probarlos; no reabrir T0 ratificado de los cuatro sin evidencia nueva.

## 5. Handoff de fuentes y orden de trabajo

- Auditoría Astra `AUDITORIA_VIABILIDAD_GUARDIANES_AOE.md` — 2026-10-05, sobre ver76 + candidata G03, distingue ubicación histórica y propuesta. **No implementó cambios.**
- `HANDOFF_LA_GRULLA_TECNICAS_HEAVY_2026-10-04.md` — §§15.5–15.9, define reglas de únicas, AOE desde LIII y benchmark con Ulti.
- Fuente ratificada cuatro únicos: commit `45c3a9c240ea74208a0d8fd4d5be187bc817df35`; snapshot experimental más viejo no prevalece.
- La IA adaptativa de especies repetibles T0→T4 no debe confundirse con las mecánicas propias de un jefe **T0 único**.
- V04 LII actual no es el balance de guardianes. Completar etapas previas, construir poder legal `PRE_AOE LIII` con equipo y Ultis, validar kits/burst de los cuatro y diseñar T0 del nuevo custodio Tierra. Sólo después probar recompensa `POST_AOE`.

**No tocar `main`, no merge, no modificar HTML/runtime, ni sincronizar registros automáticamente. Este archivo es registro documental de decisión, no una orden de implementación a Astra.**
