export const MONSTER_STAT_CONTRACT_STATUS='NEW_ENGINE_ONLY_V1';
export const ENGINE_CONTRACT='NEW_COMBAT_STATS_V0_1';
export const READY='READY';

export const ARC1_MONSTER_IDS=Object.freeze([
  'rata_qi','avispa_jade','serpiente_qi','mono_pildoras','lobo_espiritual',
  'sapo_ceniza','escarabajo_hierro','eco_caido','sapo_caldera','rey_escarabajo',
  'pez_lunar','anguila_estelar','sombra_ahogada','guardian_coral',
  'devorador_niebla','halcon_tormenta','mantis_nube','centinela_pluma'
].sort());

export const REQUIRED_STATS=Object.freeze([
  'hp','qi_max','precision','evasion','defense',
  'tenacity','control','crit_chance','crit_damage','basic_damage'
]);

const FORBIDDEN_PROFILE_FIELDS=Object.freeze([
  'legacy','legacy_attack','legacy_defense','attack','ataque','daño','damage'
]);

const FORBIDDEN_TECHNIQUE_FIELDS=Object.freeze([
  'cada','daño','drenaQi','veneno','quemadura',
  'attack','ataque','defense','defensa','attackBonus'
]);

function rejectFields(obj,fields,label){
  for(const key of fields){
    if(Object.hasOwn(obj,key))throw new Error(`${label}: forbidden retired field ${key}`);
  }
}

export function assertMonsterProfile(profile,{requireReady=true}={}){
  if(!profile||typeof profile!=='object')throw new TypeError('monster profile required');
  rejectFields(profile,FORBIDDEN_PROFILE_FIELDS,'monster profile');

  if(profile.engine_contract!==ENGINE_CONTRACT)throw new Error('wrong monster engine contract');
  if(!ARC1_MONSTER_IDS.includes(profile.id))throw new Error('unknown Arc 1 monster id');
  if(!profile.stats||typeof profile.stats!=='object')throw new Error('monster stats object required');

  const statKeys=Object.keys(profile.stats).sort();
  if(JSON.stringify(statKeys)!==JSON.stringify([...REQUIRED_STATS].sort())){
    throw new Error('monster stats schema must match NEW_COMBAT_STATS_V0_1 exactly');
  }

  if(profile.technique){
    if(typeof profile.technique!=='object')throw new Error('monster technique must be object');
    rejectFields(profile.technique,FORBIDDEN_TECHNIQUE_FIELDS,'monster technique');
    if(!Array.isArray(profile.technique.mechanics))throw new Error('monster technique mechanics required');
  }

  if(requireReady){
    if(profile.stats_status!==READY)throw new Error('monster T0 stats are not READY');
    for(const key of REQUIRED_STATS){
      if(profile.stats[key]===null||profile.stats[key]===undefined){
        throw new Error('missing monster stat: '+key);
      }
    }
    if(profile.technique&&profile.technique.params_status!==READY){
      throw new Error('monster technique params are not READY');
    }
    if(profile.technique&&(!profile.technique.params||typeof profile.technique.params!=='object')){
      throw new Error('monster technique READY params object required');
    }
  }
  return true;
}
