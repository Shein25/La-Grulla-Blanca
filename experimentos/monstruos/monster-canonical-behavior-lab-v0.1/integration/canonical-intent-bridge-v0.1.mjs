import {canonicalAbilityIds,techniqueDue,techniqueWarning} from '../adapter/canonical-combat-adapter.mjs';

export const BRIDGE_STATUS='EXPERIMENTAL_INTEGRATION_CONTRACT_V01';

function clone(value){
  return value===undefined?undefined:JSON.parse(JSON.stringify(value));
}
function freeze(value){
  if(!value||typeof value!=='object')return value;
  for(const v of Object.values(value))freeze(v);
  return Object.freeze(value);
}
function assertDef(mobId,def){
  if(typeof mobId!=='string'||!mobId)throw new TypeError('mobId inválido');
  if(!def||typeof def!=='object'||typeof def.daño!=='string')throw new TypeError('def canónica inválida');
}
function assertRound(round){
  if(!Number.isInteger(round)||round<0)throw new TypeError('round debe ser entero >= 0');
}

export function canonicalTelegraph({mobId,def,round}){
  assertDef(mobId,def);assertRound(round);
  if(!def.tecnica||!techniqueWarning(def,round))return null;
  return freeze({
    kind:'TECHNIQUE_WARNING',
    mobId,
    round,
    executesOnRound:round+1,
    techniqueName:def.tecnica.name,
    cadence:def.tecnica.cada
  });
}

export function bindMonsterIntent({mobId,def,round,decision}){
  assertDef(mobId,def);assertRound(round);
  if(!decision||decision.status!=='INTENT_SELECTED'||typeof decision.abilityId!=='string'){
    throw new TypeError('decision INTENT_SELECTED inválida');
  }
  const ids=canonicalAbilityIds(mobId);

  if(decision.abilityId===ids.basic){
    return freeze({
      kind:'BASIC_ATTACK',
      mobId,
      round,
      abilityId:decision.abilityId,
      canonical:{
        ataque:def.ataque??0,
        daño:def.daño,
        elemento:def.elemento??null
      }
    });
  }

  if(decision.abilityId===ids.technique){
    if(!def.tecnica)throw new RangeError(`${mobId} no posee técnica canónica`);
    if(!techniqueDue(def,round)){
      const err=new RangeError(`CADENCE_VIOLATION: técnica de ${mobId} fuera de ronda ${round}`);
      err.code='CADENCE_VIOLATION';
      throw err;
    }
    return freeze({
      kind:'TECHNIQUE',
      mobId,
      round,
      abilityId:decision.abilityId,
      canonical:clone(def.tecnica)
    });
  }

  throw new RangeError(`UNKNOWN_CANONICAL_ABILITY: ${decision.abilityId}`);
}
