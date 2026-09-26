import fs from 'node:fs';
import {runBenchmark} from './core.mjs';

const args=process.argv.slice(2);
const opt={tier:'smoke',runs:null,seed:1337,npc:'all',out:null};
for(let i=0;i<args.length;i++){
  const a=args[i];
  if(a==='--tier')opt.tier=args[++i];
  else if(a==='--runs')opt.runs=Number(args[++i]);
  else if(a==='--seed')opt.seed=Number(args[++i]);
  else if(a==='--npc')opt.npc=args[++i];
  else if(a==='--out')opt.out=args[++i];
  else if(a==='--help'){
    console.log('node benchmark/run-benchmark.mjs [--tier smoke|standard|deep|million] [--runs N] [--seed N] [--npc all|gao_shun|pei_luo|jiang_rui] [--out file.json]');
    process.exit(0);
  }else throw new Error(`Argumento desconocido: ${a}`);
}
const result=runBenchmark(opt);
const json=JSON.stringify(result,null,2);
if(opt.out){fs.writeFileSync(opt.out,json+'\n','utf8');console.log(`WROTE ${opt.out}`);}
console.log(json);
