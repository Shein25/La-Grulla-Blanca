import fs from 'node:fs';
import {runMonsterBenchmark} from './core.mjs';

const data=JSON.parse(fs.readFileSync(new URL('../canonical/MOBS_ver74.snapshot.json',import.meta.url),'utf8'));
const args=process.argv.slice(2);
const opt={tier:'smoke',runs:null,seed:1337,mob:'all',out:null};
for(let i=0;i<args.length;i++){
  const a=args[i];
  if(a==='--tier')opt.tier=args[++i];
  else if(a==='--runs')opt.runs=Number(args[++i]);
  else if(a==='--seed')opt.seed=Number(args[++i]);
  else if(a==='--mob')opt.mob=args[++i];
  else if(a==='--out')opt.out=args[++i];
  else if(a==='--help'){
    console.log('node benchmark/run-benchmark.mjs [--tier smoke|standard|deep|million] [--runs N] [--seed N] [--mob all|mob_id] [--out result.json]');
    process.exit(0);
  }else throw new Error(`argumento desconocido: ${a}`);
}
const result=runMonsterBenchmark(data.mobs,opt);
const json=JSON.stringify(result,null,2);
if(opt.out){fs.writeFileSync(opt.out,json+'\n','utf8');console.log('WROTE '+opt.out);}
console.log(json);
