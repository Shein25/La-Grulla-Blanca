# NPC equipment assignment v0.2

**Status:** LAB PROPOSAL / GATED / NOT CANON / COMBAT APPLICATION DEFERRED

This layer separates four questions that must not be collapsed:

1. can an existing player-catalog item type plausibly appear on an NPC?
2. does this NPC have enough role authority to auto-select combat gear?
3. does a senior/distinctive NPC require bespoke NPC-owned equipment?
4. when, if ever, do equipment stats modify NPC combat?

## Assignment modes

### AUTO_CATALOG_ROLE_GUIDED

Allowed only when the accepted NPC role supplies enough evidence for a combat/
field equipment family. Existing non-unique item types may be proposed, filtered
by stage, role tags and allowed slots.

### BESPOKE_NPC_GEAR_REQUIRED

Used for senior authorities. They are deliberately left without automatic
player-catalog loadouts. A Sect Master must not end up wearing “aspirant” gear
just because it is the only early-stage player item available.

### PERSONALIZATION_REQUIRED

Used for the six A07.9 companion/peer actors. Their accepted authoring corpus
does not close an individual combat profession. They therefore do not receive
six cloned specializations. Their equipment waits for an authorized combat/
build identity.

### WARDROBE_OR_COMBAT_ROLE_REQUIRED

Used for civil, administrative and logistical roles. Their occupation alone is
not evidence that they carry combat equipment. Wardrobe design and combat
loadout are separate decisions.

## Source boundaries

- Actor identity/role comes from the accepted A07.9 32-actor corpus.
- Item IDs, slots, stage and tags come only from `equipment_arc1_catalog.json`.
- No new equipment item is invented by the automatic assignment layer.
- `source_npc` describes player acquisition. It never means the NPC wears it.

## Unique-item guard

`unique=true` player items are excluded from automatic NPC assignment.

If a named NPC later receives a personal unique object, it must be a separate
NPC-owned design entry rather than a silent duplicate of the player's unique
reward/exploration item.

## Story-stage gate

LianQi I–IV means story/player progression visibility, not the NPC's cultivation
rank. It prevents automatic early spoilers of later player equipment.

For `AUTO_CATALOG_ROLE_GUIDED` the automatic layer begins at **LianQi II**
and only considers items whose `min_stage` exactly matches the current story
band. This deliberately prevents an established patrol captain, instructor or
craft specialist from carrying aspirant/practice pieces forever merely because
their tags score well.

LianQi I therefore remains empty for established auto-catalog NPCs. Their
ordinary clothing/older personal equipment belongs to wardrobe or bespoke NPC
design, not to the player's combat-progression catalog.

## Thematic family pools

Automatic assignment does not rank all 68 player items globally.

Each allowed equipment family has an explicit per-stage pool of item IDs whose
diegetic identity is compatible with that family. Statistical/build tags rank
items **inside** that curated pool only.

This prevents mechanically attractive but narratively implausible assignments,
for example:

- medical staff receiving patrol-specific gear solely for Tenacity/Qi;
- field workers receiving archive/formations garments solely for their stats;
- a weaponsmith receiving unrelated support gear because it scores well.

The pools are LAB proposal data and remain human-reviewable. They do not make
the resulting loadouts CANON.

## Sparse slots

NPCs are not MMO mannequins. Empty slots are valid and expected.

## Combat boundary

All assignments remain visual/inventory/loadout proposals. Item stats are not
added to NPC HP/Qi/DEF/etc. until an explicit NPC combat-stat/equipment adapter
is closed.

This avoids creating a second hidden combat engine.
