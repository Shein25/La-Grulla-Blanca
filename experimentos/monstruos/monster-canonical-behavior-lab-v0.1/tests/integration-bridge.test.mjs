import assert from 'node:assert/strict';
import fs from 'node:fs';
import {chooseMonsterIntent} from '../vendor/monster-engine.mjs';
import {PROFILES} from '../vendor/profiles.mjs';
import {buildCandidateMonsterInput} from '../adapter/candidate-assignment-adapter.mjs';
import {buildCanonicalAbilityCatalog,canonicalAbilityIds,baseCombat,neutralSocial,seededRng,techniqueDue,techniqueWarning} from '../adapter/canonical-combat-adapter.mjs';
import {bindMonsterIntent,canonicalTelegraph} from '../integration/canonical-intent-bridge-v0.1.mjs';

const M=JSON.parse(fs.readFileSync(new URL('../canonical/MOBS_ver74.snapshot.json',import.meta.url),'utf8')).mobs;
const combatants=Object.keys(M).filter(id=>id!=='muneco_practica');
let pass=0,fail=0;
const T=(n,fn)=>{try{fn();pass++;console.log('PASS',n)}catch(e){fail++;console.error('FAIL',n);console.error(e.stack||e)}};

function decide(id,round){
  const def=M[id];
  const monster=buildCandidateMonsterInput({mobId:id,def,round,mode:'CADENCE_COMPAT'});
  const abilities=buildCanonicalAbilityCatalog(id,def);
  return chooseMonsterIntent({
    monster,profiles:PROFILES,abilities,
    combat:baseCombat(round),memory:[],social:neutralSocial(),rng:seededRng(1234+round)
  });
}

T('18 combatants covered',()=>assert.equal(combatants.length,18));
T('practice dummy excluded from combat AI integration',()=>assert.ok(!combatants.includes('muneco_practica')));

T('CADENCE_COMPAT binds exactly basic or canonical technique over rounds 1..12',()=>{
  for(const id of combatants){
    const def=M[id],ids=canonicalAbilityIds(id);
    for(let round=1;round<=12;round++){
      const d=decide(id,round);
      const bound=bindMonsterIntent({mobId:id,def,round,decision:d});
      const due=techniqueDue(def,round);
      if(def.tecnica&&due){
        assert.equal(d.abilityId,ids.technique,`${id} r${round}`);
        assert.equal(bound.kind,'TECHNIQUE',`${id} r${round}`);
        assert.deepEqual(bound.canonical,def.tecnica,`${id} r${round}`);
      }else{
        assert.equal(d.abilityId,ids.basic,`${id} r${round}`);
        assert.equal(bound.kind,'BASIC_ATTACK',`${id} r${round}`);
        assert.equal(bound.canonical.daño,def.daño,`${id} r${round}`);
      }
    }
  }
});

T('telegraph matches production formula on all techniques rounds 0..12',()=>{
  for(const id of combatants){
    const def=M[id];
    for(let round=0;round<=12;round++){
      const t=canonicalTelegraph({mobId:id,def,round});
      assert.equal(!!t,techniqueWarning(def,round),`${id} r${round}`);
      if(t){
        assert.equal(t.executesOnRound,round+1);
        assert.equal(t.techniqueName,def.tecnica.name);
        assert.equal(t.cadence,def.tecnica.cada);
      }
    }
  }
});

T('technique payload preserves poison/burn/qi-drain fields byte-semantically',()=>{
  for(const id of combatants){
    const def=M[id];
    if(!def.tecnica)continue;
    const round=def.tecnica.cada;
    const b=bindMonsterIntent({mobId:id,def,round,decision:decide(id,round)});
    assert.deepEqual(b.canonical,def.tecnica,id);
  }
});

T('basic binding never smuggles technique payload',()=>{
  for(const id of combatants){
    const def=M[id],ids=canonicalAbilityIds(id);
    const b=bindMonsterIntent({mobId:id,def,round:1,decision:{status:'INTENT_SELECTED',abilityId:ids.basic}});
    assert.equal(b.kind,'BASIC_ATTACK');
    assert.equal(Object.hasOwn(b.canonical,'tecnica'),false);
  }
});

T('off-cadence technique is rejected',()=>{
  for(const id of combatants){
    const def=M[id];if(!def.tecnica)continue;
    const ids=canonicalAbilityIds(id);
    let round=1;while(techniqueDue(def,round))round++;
    assert.throws(
      ()=>bindMonsterIntent({mobId:id,def,round,decision:{status:'INTENT_SELECTED',abilityId:ids.technique}}),
      /CADENCE_VIOLATION/
    );
  }
});

T('mob without technique rejects technique binding',()=>{
  const id='rata_qi',def=M[id],ids=canonicalAbilityIds(id);
  assert.throws(()=>bindMonsterIntent({mobId:id,def,round:3,decision:{status:'INTENT_SELECTED',abilityId:ids.technique}}),/no posee técnica/);
});

T('unknown ability is rejected',()=>{
  assert.throws(()=>bindMonsterIntent({mobId:'rata_qi',def:M.rata_qi,round:1,decision:{status:'INTENT_SELECTED',abilityId:'inventada'}}),/UNKNOWN_CANONICAL_ABILITY/);
});

T('bound orders are deep-frozen',()=>{
  const b=bindMonsterIntent({mobId:'serpiente_qi',def:M.serpiente_qi,round:3,decision:decide('serpiente_qi',3)});
  assert.equal(Object.isFrozen(b),true);
  assert.equal(Object.isFrozen(b.canonical),true);
  assert.throws(()=>{b.canonical.name='hack';},TypeError);
});

T('binding does not mutate canonical MOBS',()=>{
  const before=JSON.stringify(M);
  for(const id of combatants){
    for(let r=1;r<=6;r++)bindMonsterIntent({mobId:id,def:M[id],round:r,decision:decide(id,r)});
  }
  assert.equal(JSON.stringify(M),before);
});

T('binding contains no HP/status/cooldown mutation API',()=>{
  const source=bindMonsterIntent.toString().toLowerCase();
  for(const term of ['hp -=','hp +=','status.push','cooldowns[','loot','muerte'])assert.equal(source.includes(term),false,term);
});

console.log(`\nPASS: ${pass}`);
console.log(`FAIL: ${fail}`);
if(fail)process.exitCode=1;
