import assert from 'node:assert/strict';
import { createMemoryState, recordMemory } from '../motor-npc-vivo-v0.3-memory/memory.mjs';
import { deriveRelations } from './relation-deriver.mjs';

const BASE = Object.freeze({
  afinidad:50, confianza:50, respeto:50, deuda:50, temor:50, rivalidad:50,
});
const FIELDS = Object.keys(BASE);
let passed = 0;

function test(name, fn) {
  try { fn(); passed++; console.log('PASS ', name); }
  catch (error) { console.error('FAIL ', name, error); process.exitCode = 1; }
}

function event(key, kind, value=true, importance=100, confidence=100, turn=1, expiresTurn=null) {
  return { key, kind, subject:'jugador', value, importance, confidence, turn, expiresTurn };
}

function memoryOf(...events) {
  let memory=createMemoryState();
  for (const item of events) memory=recordMemory(memory,item);
  return memory;
}

function assertRelations(result, patch={}) {
  assert.deepEqual(result.relations,{...BASE,...patch});
  for (const field of FIELDS) {
    assert.ok(Number.isFinite(result.relations[field]));
    assert.ok(result.relations[field]>=0 && result.relations[field]<=100);
  }
}

test('sin memoria mantiene las seis relaciones base',()=>{
  const out=deriveRelations(BASE,createMemoryState(),0);
  assertRelations(out);assert.deepEqual(out.contributions,[]);assert.deepEqual(out.ignoredMemories,[]);
  assert.deepEqual(out.rawDeltas,Object.fromEntries(FIELDS.map(field=>[field,0])));
});

test('PLAYER_HELPED_ME verdadero aumenta sólo afinidad confianza y deuda',()=>{
  const out=deriveRelations(BASE,memoryOf(event('help','PLAYER_HELPED_ME')),1);
  assertRelations(out,{afinidad:62,confianza:60,deuda:58});
  assert.deepEqual(out.rawDeltas,{afinidad:12,confianza:10,respeto:0,deuda:8,temor:0,rivalidad:0});
  assert.deepEqual(out.contributions.map(c=>c.memoryKey),['help']);
});

test('PLAYER_LIED verdadero baja confianza y respeto y sube rivalidad',()=>{
  const out=deriveRelations(BASE,memoryOf(event('lie','PLAYER_LIED')),1);
  assertRelations(out,{confianza:32,respeto:44,rivalidad:62});
});

test('importance 50 y confidence 80 dan factor 0.4 y deltas decimales',()=>{
  const out=deriveRelations(BASE,memoryOf(event('help','PLAYER_HELPED_ME',true,50,80)),1);
  assert.equal(out.contributions[0].factor,0.4);
  assert.equal(out.rawDeltas.afinidad,12*0.4);
  assert.equal(out.rawDeltas.confianza,10*0.4);
  assert.equal(out.rawDeltas.deuda,8*0.4);
  assert.equal(out.relations.afinidad,50+12*0.4);
});

test('importance cero conserva base con contribución explícita de factor cero',()=>{
  const out=deriveRelations(BASE,memoryOf(event('help','PLAYER_HELPED_ME',true,0,90)),1);
  assertRelations(out);assert.equal(out.contributions[0].factor,0);
});

test('confidence cero conserva base',()=>{
  const out=deriveRelations(BASE,memoryOf(event('lie','PLAYER_LIED',true,90,0)),1);
  assertRelations(out);assert.equal(out.contributions[0].factor,0);
});

test('recuerdo expirado no influye ni aparece como activo',()=>{
  const memory=memoryOf(event('help','PLAYER_HELPED_ME',true,100,100,1,1));
  const out=deriveRelations(BASE,memory,2);
  assertRelations(out);assert.equal(out.contributions.length,0);assert.equal(out.ignoredMemories.length,0);
});

test('expiresTurn inclusivo conserva efecto en ese turno',()=>{
  const memory=memoryOf(event('help','PLAYER_HELPED_ME',true,100,100,1,2));
  assert.equal(deriveRelations(BASE,memory,2).relations.afinidad,62);
  assert.equal(deriveRelations(BASE,memory,3).relations.afinidad,50);
});

test('PLAYER_HELPED_ME false se ignora con razón',()=>{
  const out=deriveRelations(BASE,memoryOf(event('help','PLAYER_HELPED_ME',false)),1);
  assertRelations(out);assert.deepEqual(out.ignoredMemories,[{memoryKey:'help',kind:'PLAYER_HELPED_ME',reason:'VALUE_NOT_TRUE'}]);
});

test('PLAYER_LIED con value distinto de true se ignora',()=>{
  const out=deriveRelations(BASE,memoryOf(event('lie','PLAYER_LIED','sí')),1);
  assertRelations(out);assert.equal(out.ignoredMemories[0].reason,'VALUE_NOT_TRUE');
});

test('kinds ORDER_RECEIVED y SIGHTING_RELEVANT son ignorados',()=>{
  const out=deriveRelations(BASE,memoryOf(event('order','ORDER_RECEIVED'),event('sight','SIGHTING_RELEVANT')),1);
  assertRelations(out);assert.equal(out.ignoredMemories.length,2);
  assert.ok(out.ignoredMemories.every(x=>x.reason==='NO_SOCIAL_RULE'));
});

test('kinds heredados de Object.prototype no adquieren regla social',()=>{
  const out=deriveRelations(BASE,memoryOf(event('a','toString'),event('b','constructor'),event('c','__proto__')),1);
  assertRelations(out);assert.equal(out.ignoredMemories.length,3);assert.equal(out.contributions.length,0);
});

test('ayuda y mentira se agregan matemáticamente',()=>{
  const out=deriveRelations(BASE,memoryOf(event('help','PLAYER_HELPED_ME'),event('lie','PLAYER_LIED')),1);
  assertRelations(out,{afinidad:62,confianza:42,respeto:44,deuda:58,rivalidad:62});
  assert.equal(out.rawDeltas.confianza,-8);
});

test('orden inverso de entries produce resultado completo idéntico',()=>{
  const memory=memoryOf(event('b','PLAYER_LIED',true,80,70),event('a','PLAYER_HELPED_ME',true,70,90));
  const reversed={...memory,entries:[...memory.entries].reverse()};
  assert.deepEqual(deriveRelations(BASE,memory,1),deriveRelations(BASE,reversed,1));
});

test('clamp superior sólo después de agregar deltas',()=>{
  const base={...BASE,afinidad:99};
  const out=deriveRelations(base,memoryOf(event('help','PLAYER_HELPED_ME')),1);
  assert.equal(out.rawDeltas.afinidad,12);assert.equal(out.relations.afinidad,100);
});

test('clamp inferior sólo después de agregar deltas',()=>{
  const base={...BASE,confianza:2};
  const out=deriveRelations(base,memoryOf(event('lie','PLAYER_LIED')),1);
  assert.equal(out.rawDeltas.confianza,-18);assert.equal(out.relations.confianza,0);
});

test('clamp intermedio daría otro resultado: 95 + 10 - 18 = 87',()=>{
  const base={...BASE,confianza:95};
  const memory=memoryOf(event('help','PLAYER_HELPED_ME'),event('lie','PLAYER_LIED'));
  const out=deriveRelations(base,memory,1);
  assert.equal(out.rawDeltas.confianza,-8);assert.equal(out.relations.confianza,87);
  assert.notEqual(out.relations.confianza,82);
});

test('misma entrada produce snapshot idéntico sin acumulación',()=>{
  const memory=memoryOf(event('help','PLAYER_HELPED_ME'));
  const a=deriveRelations(BASE,memory,1),b=deriveRelations(BASE,memory,1);
  assert.deepEqual(a,b);assert.equal(BASE.confianza,50);assert.equal(a.relations.confianza,60);
});

test('count no multiplica la influencia',()=>{
  let memory=memoryOf(event('help','PLAYER_HELPED_ME'));
  memory=recordMemory(memory,event('help','PLAYER_HELPED_ME',true,100,100,2));
  assert.equal(memory.entries[0].count,2);
  assert.equal(deriveRelations(BASE,memory,2).rawDeltas.confianza,10);
});

test('no muta base, memoria, entradas ni resultados previos',()=>{
  const base={...BASE},memory=memoryOf(event('help','PLAYER_HELPED_ME'));
  const beforeBase=structuredClone(base),beforeMemory=structuredClone(memory);
  const first=deriveRelations(base,memory,1),firstBefore=structuredClone(first);
  const second=deriveRelations(base,memory,1);
  assert.deepEqual(base,beforeBase);assert.deepEqual(memory,beforeMemory);assert.deepEqual(first,firstBefore);
  second.relations.confianza=0;second.contributions[0].deltas.afinidad=999;
  assert.deepEqual(first,firstBefore);assert.deepEqual(base,beforeBase);assert.deepEqual(memory,beforeMemory);
});

test('base con prototipo null y seis datos propios es admitida',()=>{
  const base=Object.assign(Object.create(null),BASE);
  assertRelations(deriveRelations(base,createMemoryState(),0));
});

test('sin delta preserva exactamente -0 en una relación válida',()=>{
  const base={...BASE,temor:-0};
  const out=deriveRelations(base,createMemoryState(),0);
  assert.ok(Object.is(out.relations.temor,-0));
});

test('getter en confianza se rechaza sin ejecutarlo',()=>{
  let calls=0;const base={...BASE};
  Object.defineProperty(base,'confianza',{get(){calls++;throw new Error('getter ejecutado');},enumerable:true});
  assert.throws(()=>deriveRelations(base,createMemoryState(),0),TypeError);assert.equal(calls,0);
});

test('getter en otro campo se rechaza sin ejecutarlo',()=>{
  let calls=0;const base={...BASE};
  Object.defineProperty(base,'rivalidad',{get(){calls++;return 50;},enumerable:false});
  assert.throws(()=>deriveRelations(base,createMemoryState(),0),TypeError);assert.equal(calls,0);
});

test('setter-only y getter+setter son rechazados sin ejecutar accessor',()=>{
  for(const descriptor of [{set(){}},{get(){throw new Error('ejecutado');},set(){}}]){
    const base={...BASE};Object.defineProperty(base,'temor',{...descriptor,configurable:true});
    assert.throws(()=>deriveRelations(base,createMemoryState(),0),TypeError);
  }
});

test('propiedad heredada en lugar de propia se rechaza',()=>{
  const parent={confianza:50},base=Object.assign(Object.create(parent),BASE);
  delete base.confianza;
  assert.throws(()=>deriveRelations(base,createMemoryState(),0),TypeError);
});

test('campo faltante, undefined y extra se rechazan',()=>{
  const missing={...BASE};delete missing.deuda;
  assert.throws(()=>deriveRelations(missing,createMemoryState(),0),TypeError);
  assert.throws(()=>deriveRelations({...BASE,deuda:undefined},createMemoryState(),0),TypeError);
  assert.throws(()=>deriveRelations({...BASE,extra:1},createMemoryState(),0),TypeError);
  const symbol=Symbol('extra'),withSymbol={...BASE,[symbol]:1};
  assert.throws(()=>deriveRelations(withSymbol,createMemoryState(),0),TypeError);
});

test('NaN Infinity -Infinity strings objetos arrays y rango inválido se rechazan',()=>{
  for(const invalid of [NaN,Infinity,-Infinity,'50',{},[], -1,101,null]){
    assert.throws(()=>deriveRelations({...BASE,confianza:invalid},createMemoryState(),0),TypeError);
  }
  assert.throws(()=>deriveRelations([],createMemoryState(),0),TypeError);
});

test('Proxy con trap get hostil no se lee durante captura ni cálculo',()=>{
  let calls=0;
  const proxy=new Proxy({...BASE},{get(){calls++;throw new Error('get hostil');}});
  assertRelations(deriveRelations(proxy,createMemoryState(),0));assert.equal(calls,0);
});

test('memory inválida conserva rechazo de recallMemory',()=>{
  const memory=memoryOf(event('help','PLAYER_HELPED_ME'));
  memory.entries[0].importance=NaN;
  assert.throws(()=>deriveRelations(BASE,memory,1),TypeError);
  const good=memoryOf(event('help','PLAYER_HELPED_ME'));
  assert.throws(()=>deriveRelations(BASE,good,0),TypeError);
});

console.log(`${passed} pruebas PASS.`);
