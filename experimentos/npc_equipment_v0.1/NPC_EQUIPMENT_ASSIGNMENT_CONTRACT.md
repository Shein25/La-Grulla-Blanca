# NPC equipment assignment v0.1

**Status:** LAB PROPOSAL / NOT CANON / COMBAT APPLICATION DEFERRED

This layer answers a narrower question than NPC combat balance:

> Which already-existing Arc 1 equipment pieces are plausible for each of the
> 32 A07.9 actors to visibly carry/wear as story progression advances?

It does **not** yet add those item stats to NPC combat.

## Source boundaries

- Actor identity/role comes from the accepted A07.9 32-actor authoring corpus.
- Item IDs, slots, stages and tags come only from `equipment_arc1_catalog.json`.
- No new item is invented by this layer.
- `source_npc` means acquisition source for the player. It does **not** mean
  the source NPC automatically wears that item.

## Unique-item guard

Any player-catalog item with `unique=true` is excluded from automatic NPC
assignment. This prevents an NPC loadout from silently duplicating a unique
player reward/exploration object.

If a named NPC later needs a unique personal object, it must receive a distinct
NPC-owned item/identity through a separate design decision.

## Story-stage gate

`LianQi_I ... LianQi_IV` in this assignment means the current story/player
progression visibility band. It does **not** assert the NPC's cultivation realm.

Later-stage catalog pieces are not shown early by default. Explicit narrative
exceptions can be added only with human approval.

## Sparse loadouts

NPCs are not MMO mannequins. The policy deliberately leaves slots empty.

Four A07.9 groups receive different maximum visible item counts and every
selection still obeys the 13-slot architecture/capacity.

## Role families

The role text is mapped to broad equipment preferences such as MARTIAL,
MEDICAL, FORMATION, ADMIN or LOGISTICS. These preferences rank existing
`build_tags`; they do not change item stats.

The six Batch-1 companions use `BALANCED_PEER` because their accepted
authoring corpus does not supply a combat profession in the role field. No
specialization is invented for them here.

## Combat boundary

Until an NPC combat-stat contract is closed:

- item stats are not added to NPC HP/Qi/DEF/etc.;
- these assignments may drive appearance, inspect text, inventory or later
  combat loadout preparation;
- a future combat integration must decide whether NPCs share the player
  equipment formulas or use an adapter.

This prevents equipment work from silently becoming a second combat engine.
