# HANDOFF DE CONVERSACIÓN — LA GRULLA BLANCA
## Comercio Arco 1 · B01 · NEW_PLAYER_STATS_EQUIPMENT_PRODUCTIVE_BINDING_PREFLIGHT

Fecha de cierre: 2026-10-02
Motivo: límite de conversación.
Estado: CONTINUIDAD LISTA PARA NUEVO CHAT.

---

# 1. Repositorio / rama

Repositorio:

```text
Shein25/La-Grulla-Blanca
```

Rama activa:

```text
experiment/monster-loot-equipment-economy-v0.1
```

HEAD funcional/de diseño antes de los documentos de cierre:

```text
e77887b6901b049881669e6436652d6da2e0b248
```

En ese HEAD:
- contratos de Comercio ratificados;
- preflight Slice 1 ratificado;
- CI de Commerce/Slice 1 en success;
- no implementación runtime del Slice 1.

Documentos de continuidad añadidos después:

```text
670512555d3214a6602cf2183a212e3307fe4472
docs: clarify B01 uses new combat stats and deprecates legacy consumers

5a72896e99d6ad5ba15258a35e3fc25a6a2b414b
docs: add resume prompt for commerce B01 player stats preflight
```

Este handoff es documental. No modifica runtime.

---

# 2. Guardias duras

Mantener:

- NO tocar `main`.
- NO merge automático.
- NO modificar `ROOMS.exits`.
- NO inventar NPCs, rooms, gates, misiones o estados.
- decisiones humanas prevalecen.
- `freeAiText=false`.
- no LLM/API libre en runtime.
- no timers/reloj nuevo.
- no reabrir A07 salvo bug reproducible o extensión mínima autorizada.
- no compatibilidad legacy en runtime final.
- no migración de saves antiguos.
- no aliases/fallbacks old/new.
- final sigue siendo un HTML autocontenido.
- Astra se encarga de integración productiva cuando se autorice; este frente diseña/audita primero.

---

# 3. Autoridades de Comercio vigentes

Directorio:

```text
experimentos/balance_nuevo/loot_equipment_v0.1/
```

Autoridades ratificadas:

```text
ARC1_COMMERCE_AUTHORITY_V0_4.json
ARC1_MERCHANT_CAPABILITIES_V0_1.json
ARC1_COMMERCE_TRANSACTION_CONTRACT_V0_1.json
ARC1_COMMERCE_CATALOG_UI_V0_1.json
ARC1_CONTRIBUTION_CLEANSLATE_V0_1.json
ARC1_EQUIPMENT_RUNTIME_BINDING_V0_1.json
ARC1_COMMERCE_SLICE1_A07_PREFLIGHT_V0_1.json
```

Catálogo de equipo:

```text
experimentos/balance_nuevo/equipment_arc1_catalog.json
```

---

# 4. Comercio — decisiones cerradas

## Entrada

Comercio entra por diálogo:

```text
HABLAR
→ handler canónico / misión tiene prioridad
→ host A07 general
→ DOMAIN:COMMERCE si corresponde
```

No comandos públicos:

```text
comprar <item>
vender <item>
comerciar <npc>
```

`DOMAIN:COMMERCE`:
- no forma parte de las 84 authored player entries;
- no es intent conversacional A07;
- no es NPC utterance;
- no modifica ROLE/SELF_INTRODUCTION.

## UI

Catálogo textual, estilo actual del MUD.

No UI MMORPG nueva.

La UI nunca es autoridad de:
- precio;
- stock;
- Contribution;
- permisos;
- materiales;
- balance;
- disponibilidad.

## Transacción

Pipeline ratificado:

```text
EVALUATE
→ CONFIRM
→ REVALIDATE
→ BUILD_DELTA
→ COMMIT
→ RECEIPT
```

Revalidar en commit.
Todo-o-nada.
Doble defensa contra replay/doble click.
AI nunca muta economía.

## Venta

BUY del comerciante es sink económico por defecto:
- lo vendido desaparece de circulación;
- no alimenta automáticamente stock SELL.

## Servicios

SERVICE usa materiales + piedras.
Contribution sólo abre acceso; nunca se gasta.

---

# 5. Contribution clean-slate

Autoridad única:

```text
player.facciones[factionId].contribucion
```

Semántica:
- acumulativa;
- monotónica;
- no gastable.

Eliminar en futura integración:
- saldo;
- gastos;
- mirror `player.contribucion`;
- `gastarContribucion()`;
- `cmd_canjear()`;
- servicios legacy basados en gastar Contribution.

Objetivo save:

```text
SAVE_SCHEMA_VERSION = 3
facciones_version = 2
```

Schema 2:
- rechazo/reset;
- NO migración.

---

# 6. Equipo clean-slate

Slots canónicos:

```text
ARMA
TOCADO
VESTIDURA
BRAZALES
FAJIN
PIERNAS
CALZADO
AMULETO
PULSERA
ANILLO
TESORO_ESPIRITUAL
```

Representación:

```text
ARRAY_PER_SLOT
```

Capacidades:

```text
ANILLO = 2
TESORO_ESPIRITUAL = 2
resto = 1
```

No slot translation legacy.

Stats de equipo se conectan al nuevo contrato, no a:
- ataque;
- daño;
- qi_med;
- agregadores legacy.

---

# 7. Slice 1 Ning Cai — ratificado

Actor:

```text
ning_cai
room = taller_ning_cai
mobility = ANCLADO
capabilities Slice 1 = SELL + FULFILL
```

Oferta única:

```text
calzas_sendero_pinos
Calzas de sendero de pinos
slot = PIERNAS
price = 8 piedras espirituales
stock = ROUTINE_UNLIMITED
Contribution = 0
permission = none
sourceMission = M04
minStage = LianQi_II
stats = hp_max +3, evasion +1
```

Disponibilidad ratificada:

```text
M04 realmente completada
+
etapa mínima
```

No mostrar sólo por LianQi II.

Predicado identificado por Astra:

```js
game.quests.M04 === "hecha"
```

## HP al equipar

Ratificado:

```text
EQUIP:
max HP +3
HP actual NO aumenta

UNEQUIP:
max HP -3
HP actual = min(HP actual, nuevo max HP)
```

No curación por swap.

## Return

`VOLVER A LA CONVERSACIÓN`:
- consume/cierra Comercio;
- revalida mismo actor/contexto;
- crea capability A07 NUEVA;
- no llama `cmd_hablar()`;
- no repite handler canónico;
- no reutiliza lease anterior.

Movimiento:
- cierra/invalida Comercio;
- luego resuelve movimiento normal;
- no tocar exits.

---

# 8. Auditoría Astra del Slice 1

Paquete recibido:

```text
ASTRA_SLICE1_A07_INTEGRATION_REVIEW_2026-10-02.zip
```

SHA-256 verificado:

```text
61ba796e18c8a8bf0146f634d4f5392e5cf11fe30846d1cf92f7f06ece3b28e6
```

Integridad verificada:
- tamaño: 144903 bytes;
- 79 entries;
- ZIP test limpio;
- manifest completo;
- diff vacío;
- runtime/HTML no modificados.

Resultado Astra:

```text
SLICE1_A07_INTEGRATION_BLOCKED
```

Blocker:

```text
B01_NEW_COMBAT_EQUIPMENT_CONSUMERS_NOT_CONNECTED
```

La auditoría fue revisada en esta conversación y queda:

```text
AUDIT_APPROVED
```

NO repetir la auditoría Slice 1 salvo cambio de autoridad.

## Qué sí quedó READY conceptualmente

```text
A07 / DOMAIN:COMMERCE binding
M04 gate
catalog UI
transaction request shape
transaction revalidation
durable boundary plan
return to conversation
movement invalidation
clean-slate direction
```

Lo único que impide declarar Slice1 listo es B01.

---

# 9. B01 — interpretación humana definitiva

MUY IMPORTANTE.

Autoridad de estadísticas vigente:

```text
NEW_COMBAT_STATS_V0_1
```

El modelo legacy físicamente presente en ver76 está:

```text
DEPRECATED
```

Documento específico:

```text
backups/ACLARACION_B01_NEW_COMBAT_STATS_DEPRECATED_LEGACY_2026-10-02.md
```

No usar como autoridad/fallback/bridge:

```text
ataque
defensa legacy
daño
qi_med legacy
slots legacy
p.equipado string-per-slot
efectivo() legacy
agregadores legacy
```

Dirección correcta:

```text
equipo nuevo
→ NEW_COMBAT_STATS_V0_1
→ binding productivo nuevo de jugador/equipo
```

Dirección prohibida:

```text
equipo nuevo
→ convertir a stats legacy
→ preservar runtime viejo
```

B01 significa:

> falta el consumidor productivo del nuevo sistema de estadísticas del jugador/equipo.

NO:

> adaptar el equipo nuevo al motor viejo.

---

# 10. Rama de combate / autoridad nueva

Existe:

```text
experiment/combat-stat-contract-v0.1
```

Documentación relevante:

```text
docs/experimentos/CONTRATO_COMBATE_ESTADISTICAS_DOT_V0_1.md
docs/experimentos/REGISTRO_UNIVERSAL_ESTADISTICAS_PROPIEDADES_COMBATE_V0_1.md
docs/experimentos/ETAPA19B_MOTOR_UNIFICADO_COMBATE_ARCO1_2026-09-30.md
```

El motor LAB:

```text
experimentos/balance_nuevo/etapa19b_combat_engine.py
```

ya modela conceptualmente stats nuevos, pero es:

```text
LAB / PROVISIONAL / NO RUNTIME
```

NO copiarlo al runtime automáticamente.

La autoridad formal vigente ya declaró:

```text
NEW_COMBAT_STATS_V0_1
```

y separa:

```text
ARQUITECTURA/IDENTIDAD CERRADA
≠ BALANCE NUMÉRICO READY
≠ INTEGRACIÓN PRODUCTIVA A08
```

A08 no se inicia por este frente.

---

# 11. Próximo bloque EXACTO

Nombre:

```text
NEW_PLAYER_STATS_EQUIPMENT_PRODUCTIVE_BINDING_PREFLIGHT
```

Objetivo:

Auditar cómo producir un consumer/vista autoritativa de:

```text
PLAYER BASE STATS
+
EQUIPMENT STATS
+
NEW_COMBAT_STATS_V0_1
```

sin:
- iniciar A08;
- integrar monstruos;
- integrar T1–T4;
- tocar Monster Combat AI;
- reabrir A07;
- implementar Comercio todavía;
- copiar el runner LAB;
- crear compatibilidad legacy.

Campos mínimos:

```text
precision
evasion
defense
tenacity
control
qi_max
hp_max
basic_attack_flat
technique_direct_damage_percent
percent_penetration_pp
crit_chance_pp
```

Para cada uno auditar:

```text
autoridad base del jugador
fuentes de equipo
unidad
orden de agregación
consumidor productivo
estado/readiness
GAP
```

Regla:

> Si una base sólo existe en LAB/provisional, marcar GAP. No promoverla, inferirla ni rellenarla con legacy.

---

# 12. Qué NO hacer al retomar

NO:
- repetir auditoría Astra Slice 1;
- implementar el catálogo;
- arreglar B01 con `efectivo()` legacy;
- escribir bridge ataque/defensa/daño;
- iniciar A08;
- modificar monstruos;
- importar números LAB como canon;
- implementar schema3 todavía sin preflight;
- desplegar los 68 items productivamente;
- tocar A07 cerrado;
- tocar main.

---

# 13. Primera acción del próximo chat

1. verificar HEAD real de `experiment/monster-loot-equipment-economy-v0.1`;
2. leer este handoff;
3. leer aclaración B01;
4. revisar si hubo cambios concurrentes en `experiment/combat-stat-contract-v0.1`;
5. recuperar autoridad exacta de stats base del jugador;
6. localizar consumidores runtime de stats del jugador y equipo;
7. producir matriz de:
   - CANON/AUTHORITY;
   - LAB;
   - LEGACY_DEPRECATED;
   - GAP;
   - propuesta mínima;
8. preparar el preflight `NEW_PLAYER_STATS_EQUIPMENT_PRODUCTIVE_BINDING_PREFLIGHT`.

No pedir información que pueda verificarse directamente en repo/archivos.

---

# 14. Prompt preparado

También queda guardado:

```text
backups/PROMPT_RETOMAR_CONVERSACION_GRULLA_COMERCIO_B01_2026-10-02.md
```

Ese prompt puede pegarse directamente al abrir el nuevo chat.

---

# 15. Resumen de una línea

```text
COMERCIO SLICE1 DISEÑADO + A07 AUDITADO
→ BLOQUEADO SÓLO POR B01
→ LEGACY STATS DEPRECATED
→ SIGUIENTE: NEW_PLAYER_STATS_EQUIPMENT_PRODUCTIVE_BINDING_PREFLIGHT
```
