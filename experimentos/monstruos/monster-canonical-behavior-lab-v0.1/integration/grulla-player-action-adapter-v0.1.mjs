export const GRULLA_PLAYER_ACTION_ADAPTER_STATUS='EXPERIMENTAL_INTEGRATION_READY_PLAYER_ACTION_ADAPTER_V01';

const ROLES=new Set(['ofensiva','guardia','fortificacion','esquiva','control']);

function freeze(x){return Object.freeze(x);}
function nonNegative(v,label){
  if(typeof v!=='number'||!Number.isFinite(v)||v<0)throw new TypeError(label+' debe ser número finito >= 0');
  return v;
}
function safeString(v,label){
  if(typeof v!=='string'||!v)throw new TypeError(label+' debe ser string no vacío');
  return v;
}
function resolvedElementOf({element=null,elements=null,resolvedElement=null}){
  if(resolvedElement!==null){
    safeString(resolvedElement,'resolvedElement');
    return resolvedElement;
  }
  if(element!==null){
    safeString(element,'element');
    return element;
  }
  if(elements!==null){
    if(!Array.isArray(elements)||elements.some(x=>typeof x!=='string'||!x)){
      throw new TypeError('elements debe ser array de strings');
    }
    // Una híbrida sin elemento realmente resuelto no debe inventar uno para memoria.
    return null;
  }
  return null;
}

export function damageBandFromResolvedDamage(damage){
  damage=nonNegative(damage,'damage');
  if(damage<=0)return 'NONE';
  if(damage>=8)return 'HEAVY';
  return 'NORMAL';
}

export function basicActionFromResolved({damage=0}={}){
  return freeze({
    type:'BASIC',
    techniqueId:null,
    techniqueRole:null,
    element:null,
    qiSpent:0,
    damageBand:damageBandFromResolvedDamage(damage)
  });
}

export function defendActionFromResolved(){
  return freeze({
    type:'DEFEND',
    techniqueId:null,
    techniqueRole:null,
    element:null,
    qiSpent:0,
    damageBand:'NONE'
  });
}

export function recoverActionFromResolved({vidaRecuperada=0,qiRecuperado=0}={}){
  nonNegative(vidaRecuperada,'vidaRecuperada');
  nonNegative(qiRecuperado,'qiRecuperado');
  return freeze({
    type:'RECOVER',
    techniqueId:null,
    techniqueRole:null,
    element:null,
    qiSpent:0,
    damageBand:'NONE'
  });
}

export function techniqueActionFromResolved({
  techniqueId,
  techniqueType,
  element=null,
  elements=null,
  resolvedElement=null,
  qiSpent,
  damage=0
}){
  safeString(techniqueId,'techniqueId');
  if(!ROLES.has(techniqueType))throw new TypeError('techniqueType inválido: '+techniqueType);
  nonNegative(qiSpent,'qiSpent');
  nonNegative(damage,'damage');

  return freeze({
    type:techniqueType==='control'?'CONTROL':'TECHNIQUE',
    techniqueId,
    techniqueRole:techniqueType,
    element:resolvedElementOf({element,elements,resolvedElement}),
    qiSpent,
    damageBand:damageBandFromResolvedDamage(damage)
  });
}

export function playerActionFromResolvedCombat(signal){
  if(!signal||typeof signal!=='object'||Array.isArray(signal))throw new TypeError('signal debe ser objeto');

  switch(signal.kind){
    case 'BASIC':
      return basicActionFromResolved({damage:signal.damage??0});
    case 'DEFEND':
      return defendActionFromResolved();
    case 'RECOVER':
      return recoverActionFromResolved({
        vidaRecuperada:signal.vidaRecuperada??0,
        qiRecuperado:signal.qiRecuperado??0
      });
    case 'TECHNIQUE':
      return techniqueActionFromResolved({
        techniqueId:signal.techniqueId,
        techniqueType:signal.techniqueType,
        element:signal.element??null,
        elements:signal.elements??null,
        resolvedElement:signal.resolvedElement??null,
        qiSpent:signal.qiSpent,
        damage:signal.damage??0
      });
    default:
      throw new RangeError('resolved combat kind inválido: '+signal.kind);
  }
}
