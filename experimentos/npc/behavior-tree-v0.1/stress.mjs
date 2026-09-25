import crypto from 'node:crypto';
import {createRuntime,tickBehaviorTree} from './engine.mjs';
import {GUARD_TREE,WORKER_TREE,SUPERVISOR_TREE} from './fixtures.mjs';

const N=Number(process.argv[2]||100000);
const SEED=Number(process.argv[3]||1337)>>>0;

function rng(seed){let x=seed>>>0;return()=>{x^=x<<13;x^=x>>>17;x^=x<<5;return (x>>>0)/4294967296;};}

const trees=[GUARD_TREE,WORKER_TREE,SUPERVISOR_TREE];
const factPools=[
 [{},{suspicious:true},{hostile:true},{hostile:true,suspicious:true}],
 [{},{phase:'SERVICE'},{alarm:true},{phase:'SERVICE',alarm:true}],
 [{},{playerRequest:true},{crisis:true},{playerRequest:true,crisis:true}]
];

function run(seed){
 const random=rng(seed);
 const runtimes=trees.map(createRuntime);
 const trace=[];
 let nondeterministicMismatches=0,inputMutations=0,invalidRuntime=0,multiEmit=0,preemptions=0;
 for(let i=0;i<N;i++){
   const ti=Math.floor(random()*trees.length), tree=trees[ti], rt=runtimes[ti];
   const facts=factPools[ti][Math.floor(random()*factPools[ti].length)];
   let actionResults={};
   if(rt.runningAction!==null && random()<0.45){
     const p=random();
     actionResults={[rt.runningAction]:p<0.45?'RUNNING':p<0.8?'SUCCESS':'FAILURE'};
   }
   const input={facts,actionResults};
   const before=JSON.stringify([tree,rt,input]);
   const a=tickBehaviorTree(tree,rt,input), b=tickBehaviorTree(tree,rt,input);
   if(JSON.stringify(a)!==JSON.stringify(b)) nondeterministicMismatches++;
   if(JSON.stringify([tree,rt,input])!==before) inputMutations++;
   if(a.emitted.length>1) multiEmit++;
   if(a.nextRuntime.treeId!==tree.id || !Number.isSafeInteger(a.nextRuntime.tick) || a.nextRuntime.tick<0) invalidRuntime++;
   if(a.preemptedAction) preemptions++;
   runtimes[ti]=a.nextRuntime;
   trace.push([ti,facts,a.status,a.emitted,a.runningAction,a.preemptedAction,a.nextRuntime.tick]);
 }
 const digest=crypto.createHash('sha256').update(JSON.stringify(trace)).digest('hex');
 return {digest,metrics:{nondeterministicMismatches,inputMutations,invalidRuntime,multiEmit,preemptions}};
}

const a=run(SEED),b=run(SEED);
console.log(`TICKS: ${N}`);
console.log(`DIGEST 1: ${a.digest}`);
console.log(`DIGEST 2: ${b.digest}`);
for(const [k,v] of Object.entries(a.metrics)) console.log(`${k}: ${v}`);
if(a.digest!==b.digest||a.metrics.nondeterministicMismatches||a.metrics.inputMutations||a.metrics.invalidRuntime||a.metrics.multiEmit)process.exitCode=1;
