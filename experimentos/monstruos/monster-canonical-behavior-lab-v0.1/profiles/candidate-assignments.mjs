export const ASSIGNMENT_STATUS='EXPERIMENTAL_NON_CANONICAL';

const pref=(ofensiva=1,control=1)=>Object.freeze({OFENSIVA:ofensiva,CONTROL:control});

export const CANDIDATE_ASSIGNMENTS=Object.freeze({
  rata_qi:Object.freeze({profileId:'INSTINTIVO',socialProfileId:'COLONIA',preferences:pref(1,1),rationale:'fauna menor sin técnica; perfil mínimo de laboratorio'}),
  serpiente_qi:Object.freeze({profileId:'REACTIVO_1',socialProfileId:'SOLITARIO',preferences:pref(0.9,1.1),rationale:'técnica de veneno; reacción simple'}),
  lobo_espiritual:Object.freeze({profileId:'CAZADOR_2',socialProfileId:'MANADA',preferences:pref(1.05,1),rationale:'depredador descrito como cazador multidireccional'}),
  eco_caido:Object.freeze({profileId:'REACTIVO_1',socialProfileId:'SOLITARIO',preferences:pref(1,1),rationale:'conducta descrita como hábito persistente; sin técnica canónica'}),
  pez_lunar:Object.freeze({profileId:'CAZADOR_2',socialProfileId:'SOLITARIO',preferences:pref(1.05,1),rationale:'caza siguiendo el pulso del qi'}),
  sombra_ahogada:Object.freeze({profileId:'TACTICO_3',socialProfileId:'SOLITARIO',preferences:pref(0.9,1.1),rationale:'única, control por Ahogo y descripción asociada a memoria'}),
  centinela_pluma:Object.freeze({profileId:'REACTIVO_1',socialProfileId:'TERRITORIAL',preferences:pref(1.05,1),rationale:'guardián construido para custodiar'}),
  devorador_niebla:Object.freeze({profileId:'TACTICO_3',socialProfileId:'SOLITARIO',preferences:pref(1.05,1),rationale:'depredador de qi; representante táctico heredado'}),
  avispa_jade:Object.freeze({profileId:'INSTINTIVO',socialProfileId:'COLONIA',preferences:pref(0.9,1.1),rationale:'insecto menor con picadura de control'}),
  mono_pildoras:Object.freeze({profileId:'CAZADOR_2',socialProfileId:'OPORTUNISTA',preferences:pref(0.9,1.15),rationale:'robo selectivo de píldoras y drenaje de qi'}),
  sapo_ceniza:Object.freeze({profileId:'INSTINTIVO',socialProfileId:'TERRITORIAL',preferences:pref(0.9,1.1),rationale:'fauna elemental de hábitat localizado'}),
  sapo_caldera:Object.freeze({profileId:'REACTIVO_1',socialProfileId:'TERRITORIAL',preferences:pref(0.9,1.1),rationale:'criatura única con patrón de fuego periódico'}),
  escarabajo_hierro:Object.freeze({profileId:'INSTINTIVO',socialProfileId:'COLONIA',preferences:pref(1.1,1),rationale:'canon: embiste antes de pensarlo dos veces'}),
  rey_escarabajo:Object.freeze({profileId:'CAZADOR_2',socialProfileId:'COLONIA',preferences:pref(1.05,1),rationale:'único, mayor de su especie y asociado a diagrama defensivo'}),
  anguila_estelar:Object.freeze({profileId:'REACTIVO_1',socialProfileId:'SOLITARIO',preferences:pref(0.9,1.1),rationale:'técnica de drenaje de qi con patrón simple'}),
  guardian_coral:Object.freeze({profileId:'TACTICO_3',socialProfileId:'TERRITORIAL',preferences:pref(0.9,1.1),rationale:'guardián memorioso con técnica de drenaje'}),
  halcon_tormenta:Object.freeze({profileId:'CAZADOR_2',socialProfileId:'SOLITARIO',preferences:pref(1.1,1),rationale:'depredador aéreo descrito como cazador'}),
  mantis_nube:Object.freeze({profileId:'MASTER_4',socialProfileId:'SOLITARIO',preferences:pref(1.1,1),rationale:'única; precisión extrema y representante MASTER heredado'})
});

export function candidateAssignment(mobId){
  return CANDIDATE_ASSIGNMENTS[mobId]||null;
}
