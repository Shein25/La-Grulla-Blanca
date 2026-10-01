import {
  canonicalAbilityIds,techniqueDue,techniqueWarning,assertMonsterCombatReady
} from '../adapter/canonical-combat-adapter.mjs';

export const BRIDGE_STATUS='EXPERIMENTAL_NEW_ENGINE_INTEGRATION_V1';

function clone(value){
  return value===undefined?undefined:JSON.parse(JSON.stringify(value));
}
function freeze(value){
  if(!value||typeof value!=='object')return value;
  for(const v of Object.values(value))freeze(v);
  return Object.freeze(value);
}
function assertDef(mobId,def){
  if(typeof mobId!=='string'||!mobId)throw new TypeError('invalid mobId');
  assertMonsterCombatReady(mobId,def);
}
function assertRound(round){
  if(!Number.isInteger(round)||round<0)throw new TypeError('round must be integer >= 0');
}

export function canonicalTelegraph({mobId,def,round}){
  assertDef(mobId,def);assertRound(round);
  if(!def.technique||!techniqueWarning(def,round))return null;
  return freeze({
    kind:'TECHNIQUE_WARNING',
    mobId,
    round,
    executesOnRound:round+1,
    techniqueName:def.technique.name,
    cadence:def.technique.params.cadence
  });
}

export function bindMonsterIntent({mobId,def,round,decision}){
  assertDef(mobId,def);assertRound(round);
  if(!decision||decision.status!=='INTENT_SELECTED'||typeof decision.abilityId!=='string'){
    throw new TypeError('invalid INTENT_SELECTED decision');
  }
  const ids=canonicalAbilityIds(mobId);

  if(decision.abilityId===ids.basic){
    return freeze({
      kind:'BASIC_ATTACK',
      mobId,
      round,
      abilityId:decision.abilityId,
      combat:{
        precision:def.stats.precision,
        damage:def.stats.basic_damage,
        critChance:def.stats.crit_chance,
        critDamage:def.stats.crit_damage,
        element:def.element??null
      }
    });
  }

  if(decision.abilityId===ids.technique){
    if(!def.technique)throw new RangeError(`${mobId} has no monster technique`);
    if(!techniqueDue(def,round)){
      const err=new RangeError(`CADENCE_VIOLATION: ${mobId} technique outside round ${round}`);
      err.code='CADENCE_VIOLATION';
      throw err;
    }
    return freeze({
      kind:'TECHNIQUE',
      mobId,
      round,
      abilityId:decision.abilityId,
      combat:clone(def.technique)
    });
  }

  throw new RangeError(`UNKNOWN_MONSTER_ABILITY: ${decision.abilityId}`);
}
