const assert=require('node:assert/strict');
const fx=require('./POISON_QI10_ADAPTER_CANDIDATE_V30.js');
const poison=[{tipo:'veneno',familia:'jade',grado:1,duracion:3}];
const burn=[{tipo:'quemadura',familia:'ceniza',grado:1,duracion:3}];
const cfg=(raw,aff=poison,extra={})=>fx.recovery({qiActual:0,qiMax:1000,recuperacionBruta:raw,
    fuente:'MEDITAR',enCombate:false,venenoAlInicio:fx.isPoisoned(aff),...extra});
assert.equal(cfg(20).recuperacionPenalizada,18);
assert.equal(cfg(15).recuperacionPenalizada,14);
assert.equal(cfg(5).recuperacionPenalizada,5);
assert.equal(cfg(22).recuperacionPenalizada,20);
assert.equal(cfg(20,burn).recuperacionPenalizada,20);
assert.equal(cfg(20,[]).recuperacionPenalizada,20);
assert.equal(cfg(20,[...poison,...poison]).recuperacionPenalizada,18);
assert.equal(cfg(20,poison,{enCombate:true}).recuperacionPenalizada,20);
assert.equal(cfg(20,poison,{fuente:'RECOMPENSA_MISION'}).recuperacionPenalizada,20);
assert.equal(cfg(20,poison,{fuente:'BOTIN_COMBATE'}).recuperacionPenalizada,20);
assert.equal(fx.recovery({qiActual:43,qiMax:45,recuperacionBruta:20,fuente:'DORMIR',venenoAlInicio:true}).qiFinal,45);
for (let n=0;n<=500;n++) {
  const x=cfg(n).recuperacionPenalizada;
  assert.ok(Math.abs(x-n*.9)<=.50001&&x>=0&&x<=n);
}
// Poison snapshot at start of action, even if the tick first removes the status.
let afflicted=[{tipo:'veneno',familia:'jade',grado:1,duracion:1}];
const snapshot=fx.isPoisoned(afflicted);
afflicted=[];
assert.equal(fx.recovery({qiActual:0,qiMax:45,recuperacionBruta:20,fuente:'MEDITAR',venenoAlInicio:snapshot}).qiFinal,18);
assert.equal(fx.isPoisoned(afflicted),false);
let random=123456789;
function rand(){random=(Math.imul(random,1664525)+1013904223)>>>0;return random/4294967296}
for(let i=0;i<15000;i++) {
  const max=1+Math.floor(rand()*120),cur=Math.floor(rand()*(max+1)),raw=Math.floor(rand()*180);
  const burnt=rand()<.5;
  const o=fx.recovery({qiActual:cur,qiMax:max,recuperacionBruta:raw,
    fuente:rand()<.5?'DORMIR':'MEDITAR',enCombate:false,venenoAlInicio:!burnt});
  assert.ok(o.qiFinal>=cur&&o.qiFinal<=max&&o.recuperacionReal>=0);
}
console.log(JSON.stringify({status:'PASS',node_version:process.version,cases:15513,mode:'JS candidate module only / no HTML'}));
