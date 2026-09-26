import assert from 'node:assert/strict';
import fs from 'node:fs';

const data=JSON.parse(fs.readFileSync(new URL('../canonical/NPC_DEF_ver74.snapshot.json',import.meta.url),'utf8'));
const NPC=data.npc_def;

let pass=0,fail=0;
const T=(name,fn)=>{try{fn();pass++;console.log('PASS',name)}catch(e){fail++;console.error('FAIL',name);console.error(e.stack||e)}};

const STATES=new Set(['DESCONOCIDO','SOSPECHA','SABE','CONFIRMADO']);
const KNOW_KEYS=Array.from({length:10},(_,i)=>`R${i+1}`);
const normalize=s=>String(s??'').normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLowerCase().replace(/_/g,' ').replace(/\s+/g,' ').trim();

T('snapshot source blob is exact ver74 blob',()=>assert.equal(data.source.blob,'d34f7ea3f9de9344130aa072fac34d14a7a474d6'));
T('snapshot contains 32 NPC',()=>assert.equal(Object.keys(NPC).length,32));
T('declared count matches object count',()=>assert.equal(data.count,Object.keys(NPC).length));

T('every key matches def.id',()=>{
  for(const [id,def] of Object.entries(NPC)) assert.equal(def.id,id,id);
});
T('every sala_inicial is posicion_valida',()=>{
  for(const [id,def] of Object.entries(NPC)) assert.ok(def.posicion_valida.includes(def.sala_inicial),id);
});
T('every territorio_normal room is posicion_valida',()=>{
  for(const [id,def] of Object.entries(NPC)) for(const room of def.territorio_normal) assert.ok(def.posicion_valida.includes(room),`${id}:${room}`);
});
T('every transito_tecnico room is posicion_valida',()=>{
  for(const [id,def] of Object.entries(NPC)) for(const room of def.transito_tecnico) assert.ok(def.posicion_valida.includes(room),`${id}:${room}`);
});
T('every route node is posicion_valida',()=>{
  for(const [id,def] of Object.entries(NPC)) for(const route of def.rutas) for(const room of route) assert.ok(def.posicion_valida.includes(room),`${id}:${room}`);
});
T('ANCLADO NPC have no routes and one valid room',()=>{
  for(const [id,def] of Object.entries(NPC)) if(def.movilidad==='ANCLADO'){
    assert.equal(def.rutas.length,0,id);
    assert.equal(def.posicion_valida.length,1,id);
  }
});
T('RUTA NPC have at least one route',()=>{
  for(const [id,def] of Object.entries(NPC)) if(def.movilidad==='RUTA') assert.ok(def.rutas.length>=1,id);
});
T('knowledge is exactly R1-R10 with canonical states',()=>{
  for(const [id,def] of Object.entries(NPC)){
    assert.deepEqual(Object.keys(def.conocimiento_inicial).sort(),[...KNOW_KEYS].sort(),id);
    for(const [k,v] of Object.entries(def.conocimiento_inicial)) assert.ok(STATES.has(v),`${id}:${k}=${v}`);
  }
});
T('alias id_canonico matches canonical id',()=>{
  for(const [id,def] of Object.entries(NPC)) assert.equal(def.aliases.id_canonico,id,id);
});
T('all normalized aliases are globally unambiguous',()=>{
  const seen=new Map();
  for(const [id,def] of Object.entries(NPC)){
    const aliases=[id,def.nombre,...def.aliases.alias_cortos_inequivocos];
    for(const raw of aliases){
      const key=normalize(raw);
      if(seen.has(key)) assert.equal(seen.get(key),id,`alias ambiguo ${key}`);
      else seen.set(key,id);
    }
  }
});
T('category totals remain 7/7/12/6',()=>{
  const counts={};
  for(const def of Object.values(NPC)) counts[def.categoria]=(counts[def.categoria]||0)+1;
  assert.deepEqual(counts,{autoridad:7,intermedio:7,funcional:12,companero:6});
});
T('movement totals remain 3 ANCLADO / 29 RUTA',()=>{
  const counts={};
  for(const def of Object.values(NPC)) counts[def.movilidad]=(counts[def.movilidad]||0)+1;
  assert.deepEqual(counts,{ANCLADO:3,RUTA:29});
});

console.log(`\nPASS: ${pass}`);
console.log(`FAIL: ${fail}`);
if(fail)process.exitCode=1;
