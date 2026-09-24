import assert from 'node:assert/strict';
import {
  createMemoryState, recordMemory, recallMemory, pruneMemory,
  forgetMemory, memoryStats,
} from './memory.mjs';

let passed=0;
const test=(name,fn)=>{
  try { fn(); passed++; console.log('PASS  '+name); }
  catch(err) { console.error('FAIL  '+name+'\n      '+(err.stack||err)); process.exitCode=1; }
};

const event=(overrides={})=>({
  key:'player:helped_me',
  kind:'PLAYER_HELPED_ME',
  subject:'player',
  value:true,
  importance:80,
  confidence:100,
  turn:10,
  ...overrides,
});

test('estado inicial vacío y versionado',()=>{
  assert.deepEqual(createMemoryState(),{version:1,entries:[]});
});

test('registra un recuerdo semántico',()=>{
  const m=recordMemory(createMemoryState(),event());
  assert.equal(m.entries.length,1);
  assert.deepEqual(m.entries[0],{
    key:'player:helped_me',kind:'PLAYER_HELPED_ME',subject:'player',value:true,
    importance:80,confidence:100,firstTurn:10,lastTurn:10,count:1,expiresTurn:null,
  });
});

test('upsert por key no duplica y conserva firstTurn',()=>{
  let m=recordMemory(createMemoryState(),event());
  m=recordMemory(m,event({value:false,importance:70,confidence:90,turn:14}));
  assert.equal(m.entries.length,1);
  assert.equal(m.entries[0].firstTurn,10);
  assert.equal(m.entries[0].lastTurn,14);
  assert.equal(m.entries[0].count,2);
  assert.equal(m.entries[0].value,false);
  assert.equal(m.entries[0].importance,70);
});

test('misma key no puede cambiar kind ni subject',()=>{
  const m=recordMemory(createMemoryState(),event());
  assert.throws(()=>recordMemory(m,event({kind:'PLAYER_LIED',turn:11})),/identidad semántica/);
  assert.throws(()=>recordMemory(m,event({subject:'npc_x',turn:11})),/identidad semántica/);
});

test('evento antiguo para la misma key se rechaza',()=>{
  const m=recordMemory(createMemoryState(),event({turn:20}));
  assert.throws(()=>recordMemory(m,event({turn:19})),/no puede retroceder/);
});

test('expiración explícita elimina recuerdo al avanzar más allá del turno',()=>{
  const m=recordMemory(createMemoryState(),event({expiresTurn:12}));
  assert.equal(recallMemory(m,12).length,1);
  assert.equal(recallMemory(m,13).length,0);
  assert.equal(pruneMemory(m,13).entries.length,0);
});

test('recordMemory purga expirados antes de insertar',()=>{
  let m=recordMemory(createMemoryState(),event({key:'old',expiresTurn:10}));
  m=recordMemory(m,event({key:'new',turn:11}));
  assert.deepEqual(m.entries.map(x=>x.key),['new']);
});

test('capacidad expulsa el recuerdo más débil de forma determinista',()=>{
  let m=createMemoryState();
  m=recordMemory(m,event({key:'a',importance:10,confidence:100}),{maxEntries:2});
  m=recordMemory(m,event({key:'b',importance:90,confidence:10,turn:11}),{maxEntries:2});
  m=recordMemory(m,event({key:'c',importance:50,confidence:50,turn:12}),{maxEntries:2});
  assert.deepEqual(m.entries.map(x=>x.key),['b','c']);
});

test('empate de retención usa confianza, recencia y key',()=>{
  let m=createMemoryState();
  m=recordMemory(m,event({key:'a',importance:50,confidence:50,turn:1}),{maxEntries:2});
  m=recordMemory(m,event({key:'b',importance:50,confidence:60,turn:1}),{maxEntries:2});
  m=recordMemory(m,event({key:'c',importance:50,confidence:60,turn:2}),{maxEntries:2});
  assert.deepEqual(m.entries.map(x=>x.key),['b','c']);
});

test('empate total conserva key lexicográficamente menor',()=>{
  let m=createMemoryState();
  for(const key of ['c','b','a']) m=recordMemory(m,event({key,importance:50,confidence:50,turn:1}),{maxEntries:2});
  assert.deepEqual(m.entries.map(x=>x.key),['a','b']);
});

test('recall ordena por fuerza y no por almacenamiento canónico',()=>{
  let m=createMemoryState();
  m=recordMemory(m,event({key:'a',importance:30,turn:3}));
  m=recordMemory(m,event({key:'b',importance:90,turn:1}));
  m=recordMemory(m,event({key:'c',importance:60,turn:2}));
  assert.deepEqual(m.entries.map(x=>x.key),['a','b','c']);
  assert.deepEqual(recallMemory(m,3).map(x=>x.key),['b','c','a']);
});

test('recall filtra por key kind subject y mínimos',()=>{
  let m=createMemoryState();
  m=recordMemory(m,event({key:'p1',kind:'PLAYER_HELPED_ME',subject:'player',importance:80,confidence:90}));
  m=recordMemory(m,event({key:'p2',kind:'PLAYER_LIED',subject:'player',importance:95,confidence:40,turn:11}));
  m=recordMemory(m,event({key:'n1',kind:'ORDER_RECEIVED',subject:'superior',importance:70,confidence:100,turn:12}));
  assert.deepEqual(recallMemory(m,12,{subject:'player',minConfidence:80}).map(x=>x.key),['p1']);
  assert.deepEqual(recallMemory(m,12,{kind:'ORDER_RECEIVED'}).map(x=>x.key),['n1']);
  assert.deepEqual(recallMemory(m,12,{key:'p2'}).map(x=>x.key),['p2']);
});

test('recall respeta limit',()=>{
  let m=createMemoryState();
  for(let i=0;i<5;i++) m=recordMemory(m,event({key:'k'+i,importance:50+i,turn:i}));
  assert.equal(recallMemory(m,10,{limit:2}).length,2);
});

test('forget elimina sólo la key pedida',()=>{
  let m=createMemoryState();
  m=recordMemory(m,event({key:'a'}));
  m=recordMemory(m,event({key:'b',turn:11}));
  const n=forgetMemory(m,'a');
  assert.deepEqual(n.entries.map(x=>x.key),['b']);
  assert.deepEqual(m.entries.map(x=>x.key),['a','b']);
});

test('stats distingue activos y expirados',()=>{
  let m=createMemoryState();
  m=recordMemory(m,event({key:'a',expiresTurn:10}));
  m=recordMemory(m,event({key:'b',turn:10,expiresTurn:20}));
  assert.deepEqual(memoryStats(m,11),{total:2,active:1,expired:1});
});

test('no muta memory ni event de entrada',()=>{
  const base=createMemoryState();
  const e=event();
  const beforeBase=structuredClone(base), beforeEvent=structuredClone(e);
  const out=recordMemory(base,e);
  assert.deepEqual(base,beforeBase);
  assert.deepEqual(e,beforeEvent);
  assert.notEqual(out,base);
});

test('recall devuelve copias, no referencias internas',()=>{
  const m=recordMemory(createMemoryState(),event());
  const r=recallMemory(m,10);
  r[0].importance=0;
  assert.equal(m.entries[0].importance,80);
});

test('rechaza accessors en event antes de negocio',()=>{
  const e=event();
  Object.defineProperty(e,'importance',{get(){throw new Error('getter ejecutado');},enumerable:true});
  assert.throws(()=>recordMemory(createMemoryState(),e),/propiedad de datos propia/);
});

test('rechaza objetos heredados como evento',()=>{
  const inherited=Object.create(event());
  assert.throws(()=>recordMemory(createMemoryState(),inherited),/objeto plano/);
});

test('rechaza NaN Infinity y valores no primitivos',()=>{
  assert.throws(()=>recordMemory(createMemoryState(),event({value:NaN})),/finito/);
  assert.throws(()=>recordMemory(createMemoryState(),event({value:Infinity})),/finito/);
  assert.throws(()=>recordMemory(createMemoryState(),event({value:{x:1}})),/primitivo/);
});

test('preserva identidad de -0 como valor',()=>{
  const m=recordMemory(createMemoryState(),event({value:-0}));
  assert.equal(Object.is(m.entries[0].value,-0),true);
});

test('valida turnos, scores, expiración y capacidad',()=>{
  assert.throws(()=>recordMemory(createMemoryState(),event({turn:-1})),/turn/);
  assert.throws(()=>recordMemory(createMemoryState(),event({importance:101})),/importance/);
  assert.throws(()=>recordMemory(createMemoryState(),event({confidence:-1})),/confidence/);
  assert.throws(()=>recordMemory(createMemoryState(),event({turn:10,expiresTurn:9})),/expiresTurn/);
  assert.throws(()=>recordMemory(createMemoryState(),event(),{maxEntries:0}),/maxEntries/);
});

test('misma secuencia produce salida determinista',()=>{
  const build=()=>{
    let m=createMemoryState();
    for(let i=0;i<20;i++) m=recordMemory(m,event({key:'k'+(i%7),turn:i,importance:(i*17)%101,confidence:(i*29)%101}),{maxEntries:5});
    return m;
  };
  assert.deepEqual(build(),build());
});

console.log('\n'+passed+' pruebas PASS'+(process.exitCode?' (hubo fallos)':'')+'.');
if (process.exitCode) process.exit(process.exitCode);
