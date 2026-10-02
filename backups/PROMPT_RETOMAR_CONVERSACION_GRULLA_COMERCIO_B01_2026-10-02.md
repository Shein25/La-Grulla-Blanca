# RETOMAR LA GRULLA BLANCA — COMERCIO / B01 / NEW PLAYER STATS

Continuamos una conversación larga del proyecto **La Grulla Blanca**.

## 0. Regla de continuidad

NO empieces desde cero.

Primero verifica el estado real del repositorio y lee el handoff actualizado:

```text
backups/HANDOFF_CONVERSACION_GRULLA_COMERCIO_B01_2026-10-02.md
backups/ACLARACION_B01_NEW_COMBAT_STATS_DEPRECATED_LEGACY_2026-10-02.md
```

Rama de trabajo:

```text
experiment/monster-loot-equipment-economy-v0.1
```

El último HEAD de diseño antes del cierre de conversación era:

```text
e77887b6901b049881669e6436652d6da2e0b248
```

Después se añadieron únicamente documentos de continuidad/autoridad. Verifica el HEAD actual de la rama antes de trabajar.

NO tocar `main`.
NO merge.
NO modificar `ROOMS.exits`.
NO inventar compatibilidad legacy.
NO implementar runtime salvo autorización humana explícita.

---

## 1. Comercio ya diseñado y ratificado

Autoridades vigentes:

```text
experimentos/balance_nuevo/loot_equipment_v0.1/ARC1_COMMERCE_AUTHORITY_V0_4.json
experimentos/balance_nuevo/loot_equipment_v0.1/ARC1_MERCHANT_CAPABILITIES_V0_1.json
experimentos/balance_nuevo/loot_equipment_v0.1/ARC1_COMMERCE_TRANSACTION_CONTRACT_V0_1.json
experimentos/balance_nuevo/loot_equipment_v0.1/ARC1_COMMERCE_CATALOG_UI_V0_1.json
experimentos/balance_nuevo/loot_equipment_v0.1/ARC1_CONTRIBUTION_CLEANSLATE_V0_1.json
experimentos/balance_nuevo/loot_equipment_v0.1/ARC1_EQUIPMENT_RUNTIME_BINDING_V0_1.json
experimentos/balance_nuevo/loot_equipment_v0.1/ARC1_COMMERCE_SLICE1_A07_PREFLIGHT_V0_1.json
```

Clean-slate:

```text
NO migration
NO aliases
NO fallback
NO old/new coexistence
NO legacy save compatibility
```

Contribution:
- una sola autoridad;
- acumulativa;
- nunca se gasta;
- SAVE_SCHEMA_VERSION objetivo 3;
- facciones_version 2.

Equipo:
- 11 slots canónicos;
- arrays por slot;
- ANILLO=2;
- TESORO_ESPIRITUAL=2;
- resto=1;
- stats directos al nuevo contrato.

---

## 2. Slice 1 ratificado

NPC:

```text
ning_cai
taller_ning_cai
ANCLADO
SELL + FULFILL
```

Oferta piloto:

```text
calzas_sendero_pinos
PIERNAS
8 piedras espirituales
ROUTINE_UNLIMITED
Contribution 0
sourceMission M04
minStage LianQi_II
hp_max +3
evasion +1
```

Disponibilidad:
- M04 debe estar realmente completada;
- minStage solo NO revela la oferta.

A07:
- handler canónico tiene prioridad;
- luego host general;
- Comercio entra como `DOMAIN:COMMERCE`;
- NO cuenta entre las 84 authored player entries;
- NO es intención A07;
- NO es utterance NPC;
- retorno crea capability A07 nueva;
- retorno NO ejecuta `cmd_hablar()` ni handler de misión.

HP:
- equipar hp_max +3 NO cura;
- desequipar reduce max y hace clamp de HP actual.

---

## 3. Auditoría Astra ya ejecutada

Paquete recibido:

```text
ASTRA_SLICE1_A07_INTEGRATION_REVIEW_2026-10-02.zip
```

SHA-256:

```text
61ba796e18c8a8bf0146f634d4f5392e5cf11fe30846d1cf92f7f06ece3b28e6
```

Integridad:
- 79 entradas;
- testzip limpio;
- manifest verificado;
- diff vacío;
- runtime no modificado;
- A07 no reabierto.

Veredicto de Astra:

```text
SLICE1_A07_INTEGRATION_BLOCKED
```

Blocker único relevante:

```text
B01_NEW_COMBAT_EQUIPMENT_CONSUMERS_NOT_CONNECTED
```

La auditoría fue revisada y **ACEPTADA**. No repetirla.

---

## 4. Interpretación humana definitiva de B01

MUY IMPORTANTE:

La autoridad vigente es:

```text
NEW_COMBAT_STATS_V0_1
```

El motor/agregador legacy de estadísticas/equipo que todavía aparece físicamente en ver76 está:

```text
DEPRECATED
```

No debe usarse como:
- autoridad;
- fallback;
- bridge;
- fuente de defaults;
- destino del equipo nuevo.

Consumidores legacy como:

```text
ataque
defensa legacy
daño
qi_med legacy
slots legacy
p.equipado string-per-slot
efectivo() legacy
```

son evidencia histórica, no modelo a preservar.

Dirección correcta:

```text
equipo nuevo
→ NEW_COMBAT_STATS_V0_1
→ binding productivo nuevo jugador/equipo
```

NO:

```text
equipo nuevo
→ traducción a legacy
→ runtime viejo
```

B01 significa:

> Falta el consumidor productivo del nuevo sistema de estadísticas del jugador/equipo.

No significa:

> Hay que hacer compatible el nuevo equipo con el agregador legacy.

---

## 5. Importante sobre el motor nuevo

Existe la rama:

```text
experiment/combat-stat-contract-v0.1
```

Contiene contratos y un motor LAB que ya entiende campos como:

```text
hp_max
qi_max
precision
evasion
defense
tenacity
control
crit_chance_pp
percent_penetration_pp
technique_direct_damage_percent
basic_attack_flat
```

Pero:

```text
etapa19b_combat_engine.py
```

es LAB / PROVISIONAL / NO RUNTIME.

NO copiarlo automáticamente a ver76.

La documentación vigente también deja claro:

```text
arquitectura/identidad cerrada
≠ balance numérico READY
≠ integración productiva A08
```

y A08 no debe iniciarse por este trabajo.

---

## 6. Próximo bloque exacto

Nombre:

```text
NEW_PLAYER_STATS_EQUIPMENT_PRODUCTIVE_BINDING_PREFLIGHT
```

Objetivo:

Auditar y cerrar exclusivamente cómo establecer una vista/consumer productivo de:

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
- copiar el runner LAB al runtime;
- introducir compatibilidad legacy.

Para cada stat nuevo determinar:

```text
autoridad base del jugador
fuentes de equipo
unidad
orden de agregación
consumidor productivo
readiness
GAP si falta autoridad
```

Campos mínimos a auditar:

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

Si un valor base sólo existe en LAB/provisional:
- marcar GAP;
- NO promoverlo;
- NO inferirlo;
- NO rellenarlo con legacy.

---

## 7. Qué hacer al retomar

1. Verificar rama/HEAD actual.
2. Leer handoff + aclaración B01.
3. Verificar que no hubo cambios concurrentes que alteren las autoridades.
4. NO repetir la auditoría Astra de Slice 1.
5. Empezar `NEW_PLAYER_STATS_EQUIPMENT_PRODUCTIVE_BINDING_PREFLIGHT`.
6. Revisar primero las autoridades vigentes de `NEW_COMBAT_STATS_V0_1`, los baselines del jugador, agregación de equipo y consumidores actuales.
7. Separar estrictamente:
   - autoridad cerrada;
   - LAB;
   - runtime legacy deprecated;
   - GAP;
   - propuesta.
8. Antes de implementación, preparar auditoría/plan para Astra u otro agente, como veníamos trabajando.

El objetivo inmediato es **cerrar B01**, no implementar Comercio todavía.
