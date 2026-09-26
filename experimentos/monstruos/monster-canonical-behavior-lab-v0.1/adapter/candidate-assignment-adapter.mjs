import {candidateAssignment} from '../profiles/candidate-assignments.mjs';
import {canonicalAbilityIds,techniqueDue} from './canonical-combat-adapter.mjs';

export function buildCandidateMonsterInput({mobId,def,round,mode='DECISION_EXPERIMENTAL',recentAbilityIds=[]}){
  if(!Number.isInteger(round)||round<0)throw new TypeError('round debe ser entero >= 0');
  const assignment=candidateAssignment(mobId);
  if(!assignment)throw new RangeError(`sin asignación candidata para ${mobId}`);
  const ids=canonicalAbilityIds(mobId);
  const due=techniqueDue(def,round);
  let effectiveKit;
  if(!def.tecnica) effectiveKit=[ids.basic];
  else if(mode==='CADENCE_COMPAT') effectiveKit=due?[ids.technique]:[ids.basic];
  else if(mode==='DECISION_EXPERIMENTAL') effectiveKit=due?[ids.basic,ids.technique]:[ids.basic];
  else throw new RangeError(`mode desconocido: ${mode}`);

  return {
    id:mobId,
    profileId:assignment.profileId,
    socialProfileId:assignment.socialProfileId,
    effectiveKit,
    preferences:{...assignment.preferences},
    recentAbilityIds:[...recentAbilityIds],
    cooldowns:{}
  };
}
