import {candidateAssignment} from '../profiles/candidate-assignments.mjs';

export const TACTICAL_OVERLAY_STATUS='EXPERIMENTAL_NON_CANONICAL_REUSE_AUDITED_WEIGHTS';

function cloneAbility(a){
  return {
    ...a,
    tags:[...(a.tags||[])],
    requirements:{...(a.requirements||{}),signalsAll:[...((a.requirements||{}).signalsAll||[])]},
    utility:{
      ...a.utility,
      signalWeights:{...(a.utility?.signalWeights||{})},
      memoryWeights:{...(a.utility?.memoryWeights||{})},
      socialWeights:{...(a.utility?.socialWeights||{})}
    }
  };
}

export function applyTacticalOverlay(mobId,catalog){
  const assignment=candidateAssignment(mobId);
  if(!assignment)throw new RangeError(`sin asignación candidata para ${mobId}`);
  const out={};

  for(const [id,raw] of Object.entries(catalog)){
    const a=cloneAbility(raw);
    const isBasic=a.tags.includes('CANON_BASE_ATTACK');
    const isTechnique=a.tags.includes('CANON_TECHNIQUE');

    if(isBasic && a.intentCategory==='OFENSIVA'){
      a.utility.signalWeights.PLAYER_LOW_HP=5;
    }

    if(isTechnique && a.intentCategory==='OFENSIVA'){
      a.utility.signalWeights.PLAYER_LOW_HP=6;
    }

    if(isTechnique && a.intentCategory==='CONTROL'){
      a.utility.memoryWeights.DEFENSA_ABSORCION=-8;
    }

    if(isTechnique && assignment.socialProfileId==='MANADA'){
      a.utility.socialWeights.MANADA_WITH_ALLY=5;
    }

    if(isTechnique && assignment.socialProfileId==='OPORTUNISTA'){
      a.utility.socialWeights.OPORTUNISTA_LOW_HP=15;
    }

    out[id]=a;
  }

  return out;
}
