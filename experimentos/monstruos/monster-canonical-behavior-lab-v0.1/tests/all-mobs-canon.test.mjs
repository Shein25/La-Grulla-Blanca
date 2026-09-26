import assert from 'node:assert/strict';
import fs from 'node:fs';

const data=JSON.parse(fs.readFileSync(new URL('../canonical/MOBS_ver74.snapshot.json',import.meta.url),'utf8'));
const M=data.mobs;
let pass=0,fail=0;
const T=(n,fn)=>{try{fn();pass++;console.log('PASS',n)}catch(e){fail++;console.error('FAIL',n);console.error(e.stack||e)}};

T('source blob is exact ver74',()=>assert.equal(data.source.blob,'d34f7ea3f9de9344130aa072fac34d14a7a474d6'));
T('catalog has 19 mobs',()=>assert.equal(Object.keys(M).length,19));
T('declared count matches',()=>assert.equal(data.count,Object.keys(M).length));
T('all mobs have core combat fields',()=>{
  for(const [id,m] of Object.entries(M)){
    assert.equal(typeof m.name,'string',id);
    assert.equal(typeof m.corto,'string',id);
    assert.ok(Number.isFinite(m.hp)&&m.hp>0,id);
    assert.ok(Number.isFinite(m.ataque),id);
    assert.ok(Number.isFinite(m.defensa),id);
    assert.equal(typeof m.daño,'string',id);
    assert.ok(Number.isFinite(m.qi)&&m.qi>=0,id);
    assert.ok(Array.isArray(m.loot),id);
  }
});
T('loot probabilities are in [0,1]',()=>{
  for(const [id,m] of Object.entries(M)) for(const d of m.loot) assert.ok(Number.isFinite(d.prob)&&d.prob>=0&&d.prob<=1,`${id}:${d.item}`);
});
T('16 mobs have canonical techniques',()=>assert.equal(Object.values(M).filter(x=>x.tecnica).length,16));
T('technique cadence is integer >= 1',()=>{
  for(const [id,m] of Object.entries(M)) if(m.tecnica) assert.ok(Number.isInteger(m.tecnica.cada)&&m.tecnica.cada>=1,id);
});
T('7 mobs are canonically unique',()=>assert.equal(Object.values(M).filter(x=>x.unico===true).length,7));
T('practice dummy is the only practica mob',()=>{
  assert.equal(M.muneco_practica.practica,true);
  assert.deepEqual(Object.entries(M).filter(([,x])=>x.practica===true).map(([id])=>id),['muneco_practica']);
});
T('canonical poison techniques preserve families',()=>{
  assert.equal(M.serpiente_qi.tecnica.veneno.familia,'jade');
  assert.equal(M.avispa_jade.tecnica.veneno.familia,'jade');
  assert.equal(M.sombra_ahogada.tecnica.veneno.familia,'marea');
});
T('canonical burn techniques preserve ceniza family',()=>{
  assert.equal(M.sapo_ceniza.tecnica.quemadura.familia,'ceniza');
  assert.equal(M.sapo_caldera.tecnica.quemadura.familia,'ceniza');
});
T('Qi-drain techniques preserve exact drain values',()=>{
  assert.equal(M.mono_pildoras.tecnica.drenaQi,5);
  assert.equal(M.anguila_estelar.tecnica.drenaQi,7);
  assert.equal(M.guardian_coral.tecnica.drenaQi,8);
});
T('element set stays limited to current canon',()=>{
  const set=[...new Set(Object.values(M).map(x=>x.elemento).filter(Boolean))].sort();
  assert.deepEqual(set,['agua','fuego','metal','viento']);
});
T('no canonical mob entry contains AI profile fields',()=>{
  for(const [id,m] of Object.entries(M)){
    assert.equal(Object.hasOwn(m,'profileId'),false,id);
    assert.equal(Object.hasOwn(m,'socialProfileId'),false,id);
    assert.equal(Object.hasOwn(m,'effectiveKit'),false,id);
  }
});

console.log(`\nPASS: ${pass}`);
console.log(`FAIL: ${fail}`);
if(fail)process.exitCode=1;
