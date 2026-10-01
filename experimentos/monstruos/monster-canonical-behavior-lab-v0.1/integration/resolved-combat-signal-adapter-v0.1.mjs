export const RESOLVED_COMBAT_SIGNAL_ADAPTER_STATUS='EXPERIMENTAL_NEW_ENGINE_ADAPTER_V02';

function plainExact(input, fields, label) {
  if (!input || typeof input !== 'object' || Array.isArray(input)) {
    throw new TypeError(`${label} debe ser objeto plano`);
  }
  const proto=Object.getPrototypeOf(input);
  if (proto!==Object.prototype && proto!==null) throw new TypeError(`${label} debe ser objeto plano`);
  const keys=Reflect.ownKeys(input);
  if (keys.some(k=>typeof k!=='string')) throw new TypeError(`${label} no admite Symbols`);
  const sorted=[...keys].sort();
  const expected=[...fields].sort();
  if (sorted.join('|')!==expected.join('|')) throw new TypeError(`${label} shape inválido`);
  const out={};
  for (const key of fields) {
    const d=Object.getOwnPropertyDescriptor(input,key);
    if (!d || !Object.hasOwn(d,'value')) throw new TypeError(`${label}.${key} debe ser propiedad de datos propia`);
    out[key]=d.value;
  }
  return out;
}
function roundOf(v){
  if (!Number.isSafeInteger(v) || v<0) throw new TypeError('round debe ser entero seguro >= 0');
  return v;
}
function nonNegative(v,label){
  if (typeof v!=='number' || !Number.isFinite(v) || v<0) throw new TypeError(`${label} debe ser número finito >= 0`);
  return v;
}
function freeze(x){return Object.freeze(x);}

/**
 * Adapta un resultado estructurado ya resuelto por el motor nuevo.
 * No calcula impacto, daño, DEF ni Absorción: sólo traduce el resultado a memoria semántica.
 */
export function absorptionOutcomeFromResolvedHit(input) {
  const x=plainExact(input,['round','absorbido'],'absorption');
  const round=roundOf(x.round);
  const absorbido=nonNegative(x.absorbido,'absorption.absorbido');
  return freeze({
    type:'PLAYER_ABSORPTION_RESOLVED',
    round,
    effective:absorbido>0
  });
}

/**
 * Adapta deltas de recuperación ya resueltos por el motor nuevo.
 * No infiere valores desde logs ni vuelve a calcular curación/Qi.
 */
export function recoveryOutcomeFromResolvedDelta(input) {
  const x=plainExact(input,['round','vidaRecuperada','qiRecuperado'],'recovery');
  const round=roundOf(x.round);
  const vidaRecuperada=nonNegative(x.vidaRecuperada,'recovery.vidaRecuperada');
  const qiRecuperado=nonNegative(x.qiRecuperado,'recovery.qiRecuperado');
  return freeze({
    type:'PLAYER_RECOVERY_RESOLVED',
    round,
    effective:(vidaRecuperada+qiRecuperado)>0
  });
}
