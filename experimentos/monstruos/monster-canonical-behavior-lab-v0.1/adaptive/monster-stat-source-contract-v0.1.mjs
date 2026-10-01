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

export function assertMonsterProfile(profile,{requireReady=true}={}){
  if(!profile||typeof profile!=='object')throw new TypeError('monster profile required');
  if(profile.engine_contract!==ENGINE_CONTRACT)throw new Error('wrong monster engine contract');
  if(!ARC1_MONSTER_IDS.includes(profile.id))throw new Error('unknown Arc 1 monster id');
  if(!profile.stats||typeof profile.stats!=='object')throw new Error('monster stats object required');

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
  }
  return true;
}
