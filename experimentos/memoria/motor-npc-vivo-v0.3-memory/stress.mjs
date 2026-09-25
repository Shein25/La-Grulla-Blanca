import assert from 'node:assert/strict';
import { createMemoryState, recordMemory, recallMemory } from './memory.mjs';

const N=Math.max(1,Number(process.argv[2]||10000));
let seed=Number(process.argv[3]||1337)>>>0;
const rnd=()=>{seed=(1664525*seed+1013904223)>>>0;return seed/2**32};
const ri=n=>Math.floor(rnd()*n);

function run(initialSeed){
  seed=initialSeed>>>0;
  let memory=createMemoryState();
  for(let turn=0;turn<N;turn++){
    const slot=ri(80);
    const ttl=ri(5)===0 ? turn+ri(30) : null;
    memory=recordMemory(memory,{
      key:`memory:${slot}`,
      kind:['PLAYER_HELPED_ME','PLAYER_LIED','ORDER_RECEIVED','SIGHTING_RELEVANT'][slot%4],
      subject:['player','superior','npc_a','npc_b'][slot%4],
      value:ri(2)===0,
      importance:ri(101),
      confidence:ri(101),
      turn,
      expiresTurn:ttl,
    },{maxEntries:32});
    assert.ok(memory.entries.length<=32);
    assert.equal(new Set(memory.entries.map(x=>x.key)).size,memory.entries.length);
  }
  const recalled=recallMemory(memory,N);
  return {memory,recalled,seed};
}

const start=seed;
const a=run(start);
const b=run(start);
assert.deepEqual(a,b);
assert.ok(a.memory.entries.length<=32);
console.log(`Stress memoria PASS: ${N} eventos · seed ${start} · activos ${a.recalled.length} · almacenados ${a.memory.entries.length}`);
