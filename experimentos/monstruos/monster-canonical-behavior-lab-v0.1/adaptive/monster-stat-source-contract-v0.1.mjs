export const MONSTER_STAT_SOURCE_CONTRACT_STATUS='EXPERIMENTAL_BRIDGE_NEW_ENGINE_REQUIRED_V01';

export const ARC1_MONSTER_IDS=Object.freeze([
  'rata_qi','avispa_jade','serpiente_qi','mono_pildoras','lobo_espiritual',
  'sapo_ceniza','escarabajo_hierro','eco_caido','sapo_caldera','rey_escarabajo',
  'pez_lunar','anguila_estelar','sombra_ahogada','guardian_coral',
  'devorador_niebla','halcon_tormenta','mantis_nube','centinela_pluma'
].sort());

export const NEW_ENGINE_MONSTER_STAT_POLICY=Object.freeze({
  numericSource:'NEW_ENGINE_T0_ONLY',
  legacyNumericImport:'FORBIDDEN',
  legacyFormulaTranslation:'FORBIDDEN',
  ver74SnapshotUse:Object.freeze([
    'IDENTITY',
    'NAME',
    'LORE',
    'REGION',
    'ELEMENT',
    'TECHNIQUE_IDENTITY',
    'MECHANIC_FAMILY'
  ]),
  forbiddenVer74NumericUse:Object.freeze([
    'hp','qi','ataque','defensa','daño',
    'technique_damage','technique_attack','technique_cadence',
    'dot_damage','dot_duration','qi_drain'
  ]),
  requiredBaseStats:Object.freeze([
    'hp','qi_max','precision','evasion','defense','tenacity','control',
    'crit_chance','crit_damage','basic_damage'
  ]),
  adaptiveOrder:'NEW_ENGINE_T0 -> T1_T4_ADAPTATION -> EFFECTIVE_KIT -> MONSTER_AI -> NEW_ENGINE_RESOLVER'
});

export function assertNewEngineMonsterBase(profile){
  if(!profile||typeof profile!=='object')throw new TypeError('monster base profile required');
  if(profile.engine_contract!=='NEW_COMBAT_STATS_V0_1'){
    throw new Error('monster base must declare NEW_COMBAT_STATS_V0_1');
  }
  if(profile.stats_status!=='READY_NEW_ENGINE_T0'){
    throw new Error('monster base stats are not READY_NEW_ENGINE_T0');
  }
  if(profile.numeric_source!=='NEW_ENGINE_ONLY'){
    throw new Error('monster numeric source must be NEW_ENGINE_ONLY');
  }
  for(const legacyKey of ['ataque','defensa','daño']){
    if(Object.hasOwn(profile,legacyKey)){
      throw new Error('legacy numeric field forbidden in adaptive base: '+legacyKey);
    }
  }
  for(const key of NEW_ENGINE_MONSTER_STAT_POLICY.requiredBaseStats){
    if(profile[key]===null||profile[key]===undefined){
      throw new Error('missing new-engine monster stat: '+key);
    }
  }
  return true;
}
