import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, resolve } from 'node:path';

import {
  absorptionOutcomeFromResolvedHit,
  recoveryOutcomeFromResolvedDelta
} from '../integration/resolved-combat-signal-adapter-v0.1.mjs';
import { recordSemanticOutcome } from '../integration/semantic-memory-recorder-v0.1.mjs';

const here=dirname(fileURLToPath(import.meta.url));
const ver74Path=resolve(here,'../../../../grulla-blanca_ver74.html');
const html=readFileSync(ver74Path,'utf8');

function extractBetween(startNeedle,endNeedle,label){
  const start=html.indexOf(startNeedle);
  const end=html.indexOf(endNeedle,start);
  assert.ok(start>=0,`${label}: inicio no encontrado`);
  assert.ok(end>start,`${label}: fin no encontrado`);
  return html.slice(start,end);
}

function exactCombateClass(){
  const src=extractBetween(
    'class Combate {',
    '// ============================================================================\n//  SECCIÓN 7',
    'class Combate'
  ).trim();

  return new Function(
    'atacar','ESQUIVA_INNATA','capacidadGuardia','etiquetaMob','barra',
    'ESTADO_LABEL','restoEstadoActivo','dadoARango','Azar',
    `return ${src};`
  )(
    ()=>['   Mob prueba golpea: 4 de daño.',4],
    5,
    (reduccion,duracion)=>reduccion*duracion,
    mob=>mob.name,
    ()=>'',
    {},
    ()=>'',
    x=>String(x),
    {random:()=>0.5}
  );
}

function exactBeber(){
  const start=html.indexOf('\n  beber(args) {');
  const end=html.indexOf('\n  cmd_beber(args) {',start);
  assert.ok(start>=0 && end>start,'beber(): no se pudo aislar desde ver74');
  const method=html.slice(start+3,end).trim();

  const ITEMS={
    elixir_qi:{name:'elixir de qi menor',tipo:'consumible',recupera_qi:20,impureza:1},
    pocion_refinada:{name:'poción de sangre refinada',tipo:'consumible',cura:'3d4+4',impureza:0}
  };

  const fn=new Function(
    'ITEMS','agruparObjetos','nombreCantidad','capitalizarUI','tirar',
    `return ({${method}}).beber;`
  )(
    ITEMS,
    ()=>[],
    ()=>'',
    x=>x,
    ()=>10
  );

  return {fn,ITEMS};
}

function juegoParaBeber(item,beber){
  const j={
    player:{
      inventario:[item], qi:0, qi_max:20,
      hp:10, max_hp:20, impurezas:0, heridas_meridianos:0
    },
    resolverItem(args){
      const id=args.join('_');
      return this.player.inventario.includes(id)?id:null;
    },
    tratarAfliccion(){ return {ok:false,mensaje:''}; },
    aprenderManual(){ return [[],false]; }
  };
  j.beber=beber;
  return j;
}

let pass=0,fail=0;
const T=(name,fn)=>{
  try{ fn(); pass++; console.log('PASS',name); }
  catch(err){ fail++; console.error('FAIL',name); console.error(err.stack||err); }
};

T('ver74 absorption hook -> adapter -> semantic memory',()=>{
  const Combate=exactCombateClass();
  let memory=[];
  const j={
    player:{hp:100,max_hp:100,qi:10,qi_max:10,esquiva:5,aflicciones:[]},
    recordarCriatura(){},
    efectivo(){ return {name:'Jugador',defensa:0,ataque:0}; },
    onPlayerAbsorptionResolved(signal){
      const outcome=absorptionOutcomeFromResolvedHit(signal);
      memory=recordSemanticOutcome(memory,outcome);
    }
  };
  const mob={
    name:'Mob prueba',hp:20,max_hp:20,ataque:100,defensa:0,
    daño:'4',tecnica:null,mob_id:'mob_prueba'
  };
  const c=new Combate(j,mob,'mob_prueba');
  c.round=3;
  c.estados.jugador.push({
    tipo:'guardia',nombre:'Hook test',duracion:1,
    params:{reduccion:2,capacidad:2,capacidadMax:2},
    expira:'fin'
  });

  c.respuestaEnemigos([]);

  assert.equal(j.player.hp,98);
  assert.deepEqual(memory,[
    {category:'DEFENSA_ABSORCION',result:'EFECTIVA',round:3}
  ]);
});

T('ver74 beber exposes resolved qi delta at the mutation point',()=>{
  const {fn}=exactBeber();
  const j=juegoParaBeber('elixir_qi',fn);
  j.player.qi=1;

  const [msgs,bebido,delta]=j.beber(['elixir','qi']);

  assert.equal(bebido,true);
  assert.equal(j.player.qi,20);
  assert.deepEqual(delta,{vidaRecuperada:0,qiRecuperado:19});
  assert.equal(Object.isFrozen(delta),true);
  assert.ok(msgs.length>0);
});

T('ver74 beber exposes capped hp delta, not the raw heal roll',()=>{
  const {fn}=exactBeber();
  const j=juegoParaBeber('pocion_refinada',fn);
  j.player.hp=18;

  const [,bebido,delta]=j.beber(['pocion','refinada']);

  assert.equal(bebido,true);
  assert.equal(j.player.hp,20);
  assert.deepEqual(delta,{vidaRecuperada:2,qiRecuperado:0});
  assert.equal(Object.isFrozen(delta),true);
});

T('ver74 recovery hook -> adapter -> semantic memory',()=>{
  const Combate=exactCombateClass();
  let memory=[];
  const j={
    player:{hp:100,max_hp:100,qi:10,qi_max:10,esquiva:5,aflicciones:[]},
    recordarCriatura(){},
    efectivo(){ return {name:'Jugador',defensa:0,ataque:0}; },
    onPlayerRecoveryResolved(signal){
      const outcome=recoveryOutcomeFromResolvedDelta(signal);
      memory=recordSemanticOutcome(memory,outcome);
    }
  };
  const mob={
    name:'Mob prueba',hp:20,max_hp:20,ataque:0,defensa:0,
    daño:'1',tecnica:null,mob_id:'mob_prueba'
  };
  const c=new Combate(j,mob,'mob_prueba');
  c.round=1;
  c.emitirRecuperacionResuelta({vidaRecuperada:0,qiRecuperado:19});

  assert.deepEqual(memory,[
    {category:'RECUPERACION',result:'EFECTIVA',round:1}
  ]);
});

T('combat turn emits recovery only after incrementing round',()=>{
  const turno=extractBetween(
    '  turno(verbo, args) {',
    '\n  intentarUnionCombate(out) {',
    'Combate.turno'
  );
  const consume=turno.slice(
    turno.indexOf('if (consume) {'),
    turno.indexOf('if (consume && verbo !==')
  );
  const inc=consume.indexOf('this.round++');
  const emit=consume.indexOf('this.emitirRecuperacionResuelta(recuperacionResuelta)');
  assert.ok(inc>=0,'incremento de ronda ausente');
  assert.ok(emit>inc,'recuperación se emite antes de fijar la ronda');
});

console.log(`\nPASS: ${pass}`);
console.log(`FAIL: ${fail}`);
if(fail) process.exitCode=1;
