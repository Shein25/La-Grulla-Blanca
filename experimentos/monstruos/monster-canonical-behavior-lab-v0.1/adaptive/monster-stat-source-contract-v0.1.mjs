export const MONSTER_STAT_CONTRACT_STATUS='NEW_ENGINE_ONLY_V1';
export const ENGINE_CONTRACT='NEW_COMBAT_STATS_V0_1';
export const READY='READY';

export const ARC1_MONSTER_IDS=Object.freeze([
  'rata_qi','avispa_jade','serpiente_qi','mono_pildoras','lobo_espiritual',
  'sapo_ceniza','escarabajo_hierro','eco_caido','sapo_caldera','rey_escarabajo',
  'pez_lunar','anguila_estelar','sombra_ahogada','guardian_coral',
  'devorador_niebla','halcon_tormenta','mantis_nube','centinela_pluma'
].sort());

export const PROFILE_FIELDS=Object.freeze([
  'id','name','native_stage','native_stage_index','role','region','element','unique',
  'engine_contract','stats_status','stats','technique','ai','adaptive'
].sort());

export const REQUIRED_STATS=Object.freeze([
  'hp','qi_max','precision','evasion','defense',
  'tenacity','control','crit_chance','crit_damage','basic_damage'
].sort());

export const TECHNIQUE_FIELDS=Object.freeze([
  'name','mechanics','params_status','params'
].sort());

export const AI_FIELDS=Object.freeze(['cognition','social'].sort());
export const ADAPTIVE_FIELDS=Object.freeze(['status','rule'].sort());

function assertExactKeys(obj,expected,label){
  const actual=Object.keys(obj).sort();
  if(JSON.stringify(actual)!==JSON.stringify(expected)){
    throw new Error(`${label}: schema mismatch`);
  }
}

export function assertMonsterProfile(profile,{requireReady=true}={}){
  if(!profile||typeof profile!=='object')throw new TypeError('monster profile required');
  assertExactKeys(profile,PROFILE_FIELDS,'monster profile');

  if(profile.engine_contract!==ENGINE_CONTRACT)throw new Error('wrong monster engine contract');
  if(!ARC1_MONSTER_IDS.includes(profile.id))throw new Error('unknown Arc 1 monster id');

  if(!profile.stats||typeof profile.stats!=='object')throw new Error('monster stats object required');
  assertExactKeys(profile.stats,REQUIRED_STATS,`${profile.id}.stats`);

  if(!profile.ai||typeof profile.ai!=='object')throw new Error('monster ai object required');
  assertExactKeys(profile.ai,AI_FIELDS,`${profile.id}.ai`);

  if(!profile.adaptive||typeof profile.adaptive!=='object')throw new Error('monster adaptive object required');
  assertExactKeys(profile.adaptive,ADAPTIVE_FIELDS,`${profile.id}.adaptive`);

  if(profile.technique!==null){
    if(typeof profile.technique!=='object')throw new Error('monster technique must be object or null');
    assertExactKeys(profile.technique,TECHNIQUE_FIELDS,`${profile.id}.technique`);
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
