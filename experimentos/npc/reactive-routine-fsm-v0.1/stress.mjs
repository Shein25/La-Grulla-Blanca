import crypto from 'node:crypto';
import {createRuntime,stepFSM} from './engine.mjs';
import {GUARD_MACHINE,WORKER_MACHINE,PATROLLER_MACHINE} from './fixtures.mjs';

const N=Number(process.argv[2]||100000); const SEED=Number(process.argv[3]||1337)>>>0;
function rng(seed){let x=seed>>>0;return()=>{x^=x<<13;x^=x>>>17;x^=x<<5;return (x>>>0)/4294967296;};}
const machines=[GUARD_MACHINE,WORKER_MACHINE,PATROLLER_MACHINE];
const events=[
 {type:'TICK',facts:{patrolDue:true,phase:'SERVICE'}},{type:'TICK',facts:{patrolDue:false,phase:'PREP'}},
 {type:'SUSPICIOUS',facts:{}},{type:'PERSISTS',facts:{}},{type:'HOSTILE',facts:{}},{type:'CLEARED',facts:{}},
 {type:'COMPLIES',facts:{}},{type:'PATROL_COMPLETE',facts:{}},{type:'THREAT_ENDED',facts:{}},{type:'ARRIVED',facts:{}},
 {type:'TASK_COMPLETE',facts:{}},{type:'ALARM',facts:{}},{type:'CLEAR',facts:{}}
];
function run(seed){
 const random=rng(seed); const runtimes=machines.map(createRuntime); const trace=[];
 let nondeterministicMismatches=0,inputMutations=0,invalidStates=0,transitions=0;
 for(let i=0;i<N;i++){
   const mi=Math.floor(random()*machines.length), ei=Math.floor(random()*events.length);
   const m=machines[mi], rt=runtimes[mi], ev=events[ei];
   const before=JSON.stringify([m,rt,ev]);
   const a=stepFSM(m,rt,ev), b=stepFSM(m,rt,ev);
   if(JSON.stringify(a)!==JSON.stringify(b)) nondeterministicMismatches++;
   if(JSON.stringify([m,rt,ev])!==before) inputMutations++;
   runtimes[mi]=a.nextRuntime;
   if(!Object.hasOwn(m.states,a.nextRuntime.state)) invalidStates++;
   if(a.transitioned) transitions++;
   trace.push([mi,ei,a.from,a.to,a.emitted,a.nextRuntime.stateAge]);
 }
 const digest=crypto.createHash('sha256').update(JSON.stringify(trace)).digest('hex');
 return {digest,metrics:{transitions,nondeterministicMismatches,inputMutations,invalidStates}};
}
const a=run(SEED), b=run(SEED);
console.log(`TRANSITIONS TESTED: ${N}`);
console.log(`DIGEST 1: ${a.digest}`);console.log(`DIGEST 2: ${b.digest}`);
for(const [k,v] of Object.entries(a.metrics)) console.log(`${k}: ${v}`);
if(a.digest!==b.digest || a.metrics.nondeterministicMismatches || a.metrics.inputMutations || a.metrics.invalidStates) process.exitCode=1;
