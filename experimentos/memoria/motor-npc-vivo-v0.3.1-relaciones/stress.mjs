import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import { createMemoryState, recordMemory } from '../motor-npc-vivo-v0.3-memory/memory.mjs';
import { deriveRelations } from './relation-deriver.mjs';

const rounds=Number(process.argv[2] ?? 1000);
const seedArg=Number(process.argv[3] ?? 1337);
if (!Number.isSafeInteger(rounds) || rounds < 1) throw new TypeError('rounds debe ser entero seguro >= 1');
if (!Number.isSafeInteger(seedArg) || seedArg < 0 || seedArg > 0xffffffff) {
  throw new TypeError('seed debe ser entero entre 0 y 2^32-1');
}

const FIELDS=['afinidad','confianza','respeto','deuda','temor','rivalidad'];
const KINDS=['PLAYER_HELPED_ME','PLAYER_LIED','ORDER_RECEIVED','SIGHTING_RELEVANT'];

function simulate(seed) {
  let state=seed>>>0;
  const random=()=>{state=(Math.imul(state,1664525)+1013904223)>>>0;return state/2**32;};
  const int=max=>Math.floor(random()*max);
  const npcs=Array.from({length:32},()=>({
    base:Object.fromEntries(FIELDS.map(field=>[field,int(101)])),
    memory:createMemoryState(),
  }));
  const metrics={calls:0,events:0,expiringEvents:0,contributions:0,ignored:0};
  const digest=createHash('sha256');

  for(let turn=1;turn<=rounds;turn++)for(let index=0;index<npcs.length;index++){
    const npc=npcs[index];
    if(random()<0.55){
      const kindIndex=int(KINDS.length),variant=int(8),expiresTurn=random()<0.35?turn+int(8):null;
      const event={
        key:`${kindIndex}-${variant}`,kind:KINDS[kindIndex],subject:'jugador',
        value:random()<0.75,importance:int(101),confidence:int(101),
        turn,expiresTurn,
      };
      npc.memory=recordMemory(npc.memory,event);
      metrics.events++;
      if(expiresTurn!==null)metrics.expiringEvents++;
    }

    const baseBefore=JSON.stringify(npc.base),memoryBefore=JSON.stringify(npc.memory);
    const result=deriveRelations(npc.base,npc.memory,turn);
    assert.equal(JSON.stringify(npc.base),baseBefore);
    assert.equal(JSON.stringify(npc.memory),memoryBefore);
    assert.deepEqual(Object.keys(result.relations),FIELDS);
    assert.deepEqual(Object.keys(result.rawDeltas),FIELDS);
    for(const field of FIELDS){
      assert.ok(Number.isFinite(result.relations[field]));
      assert.ok(result.relations[field]>=0 && result.relations[field]<=100);
      assert.ok(Number.isFinite(result.rawDeltas[field]));
    }
    for(const contribution of result.contributions){
      assert.ok(Number.isFinite(contribution.factor));
      assert.ok(contribution.factor>=0 && contribution.factor<=1);
    }
    metrics.calls++;
    metrics.contributions+=result.contributions.length;
    metrics.ignored+=result.ignoredMemories.length;
    digest.update(JSON.stringify([turn,index,result]));
  }
  return {...metrics,seedFinal:state,digest:digest.digest('hex')};
}

const first=simulate(seedArg),second=simulate(seedArg);
assert.deepEqual(first,second,'misma seed debe reproducir resultado completo');
console.log(`Stress relaciones PASS: 32 NPC ficticios × ${rounds} rondas · seed ${seedArg}`);
console.log(first);
