import assert from 'node:assert/strict';
import { GOAP_ACTIONS } from './actions.mjs';
import { decideAndPlan } from './controller.mjs';
import { executeNext, executeWholePlan } from './executor.mjs';
import { GOALS, selectGoal } from './goal-selector.mjs';
import { factsMatch, planGOAP } from './goap.mjs';
import { BASE_WORLD, WORLDS } from './world-fixtures.mjs';
import { cloneNpc } from '../motor-npc-vivo-v0.1.1/npc-fixtures.mjs';

let passed=0;
const test=(name,fn)=>{
  try { fn(); passed++; console.log('PASS  '+name); }
  catch(err) { console.error('FAIL  '+name+'\n      '+(err.stack||err)); process.exitCode=1; }
};

test('planner devuelve plan vacío si objetivo ya está satisfecho',()=>{
  const r=planGOAP({done:true},{done:true},[{id:'x',cost:1,preconditions:{done:false},effects:{done:true}}]);
  assert.equal(r.status,'PLAN_FOUND'); assert.deepEqual(r.plan,[]); assert.equal(r.cost,0);
});

test('planner elige coste total mínimo y no el primer goal generado',()=>{
  const actions=[
    {id:'caro',cost:5,preconditions:{start:true},effects:{done:true}},
    {id:'paso1',cost:1,preconditions:{start:true},effects:{mid:true}},
    {id:'paso2',cost:1,preconditions:{mid:true},effects:{done:true}},
  ];
  const r=planGOAP({start:true,mid:false,done:false},{done:true},actions);
  assert.deepEqual(r.plan,['paso1','paso2']); assert.equal(r.cost,2);
});

test('empate GOAP es determinista por id de acción',()=>{
  const actions=[
    {id:'b',cost:1,preconditions:{start:true},effects:{done:true}},
    {id:'a',cost:1,preconditions:{start:true},effects:{done:true}},
  ];
  assert.deepEqual(planGOAP({start:true,done:false},{done:true},actions).plan,['a']);
});

test('planner devuelve NO_PLAN cuando no existe camino',()=>{
  const r=planGOAP({a:false},{a:true},[{id:'x',cost:1,preconditions:{a:true},effects:{a:false}}]);
  assert.equal(r.status,'NO_PLAN');
});

test('personalidades eligen objetivos distintos en el mismo mundo',()=>{
  assert.equal(selectGoal(cloneNpc('disciplinado'),WORLDS.comun).id,'FULFILL_DUTY');
  assert.equal(selectGoal(cloneNpc('leal'),WORLDS.comun).id,'HELP_PLAYER');
  assert.equal(selectGoal(cloneNpc('curioso'),WORLDS.comun).id,'INVESTIGATE_ANOMALY');
});

test('leal convierte HELP_PLAYER en plan de dos pasos',()=>{
  const r=decideAndPlan(cloneNpc('leal'),WORLDS.crisis_jugador,GOAP_ACTIONS);
  assert.equal(r.selectedGoal.id,'HELP_PLAYER');
  assert.deepEqual(r.plan.plan,['ir_jugador','ayudar_jugador']);
  assert.equal(r.plan.cost,2);
});

test('disciplinado convierte FULFILL_DUTY en acción planificada',()=>{
  const r=decideAndPlan(cloneNpc('disciplinado'),WORLDS.deber,GOAP_ACTIONS);
  assert.equal(r.selectedGoal.id,'FULFILL_DUTY');
  assert.deepEqual(r.plan.plan,['cumplir_deber']);
});

test('curioso convierte INVESTIGATE_ANOMALY en plan',()=>{
  const r=decideAndPlan(cloneNpc('curioso'),WORLDS.anomalia,GOAP_ACTIONS);
  assert.equal(r.selectedGoal.id,'INVESTIGATE_ANOMALY');
  assert.deepEqual(r.plan.plan,['investigar_anomalia']);
});

test('reporte usa camino barato por superior cuando está abierto',()=>{
  const r=decideAndPlan(cloneNpc('disciplinado'),WORLDS.reporte,GOAP_ACTIONS);
  assert.equal(r.selectedGoal.id,'REPORT_SUPERIOR');
  assert.deepEqual(r.plan.plan,['ir_superior','informar_superior']);
  assert.equal(r.plan.cost,2);
});

test('reporte usa mensajero si el paso está cerrado',()=>{
  const r=decideAndPlan(cloneNpc('disciplinado'),WORLDS.reporte_paso_cerrado,GOAP_ACTIONS);
  assert.equal(r.selectedGoal.id,'REPORT_SUPERIOR');
  assert.deepEqual(r.plan.plan,['enviar_mensajero']);
  assert.equal(r.plan.cost,4);
});

test('executor ejecuta plan completo y alcanza objetivo',()=>{
  const c=decideAndPlan(cloneNpc('leal'),WORLDS.crisis_jugador,GOAP_ACTIONS);
  const x=executeWholePlan(c.plan,WORLDS.crisis_jugador,c.selectedGoal.goal,GOAP_ACTIONS);
  assert.equal(x.status,'GOAL_REACHED');
  assert.equal(x.world.playerHelped,true);
  assert.equal(x.world.playerNeedsHelp,false);
});

test('executor exige replanning si cambian precondiciones',()=>{
  const c=decideAndPlan(cloneNpc('disciplinado'),WORLDS.reporte,GOAP_ACTIONS);
  const changed={...WORLDS.reporte,passageOpen:false};
  const x=executeNext(c.plan,changed,c.selectedGoal.goal,GOAP_ACTIONS);
  assert.equal(x.status,'REPLAN_REQUIRED');
  assert.equal(x.executed,null);
});

test('replanning encuentra mensajero después del cierre del paso',()=>{
  const changed={...WORLDS.reporte,passageOpen:false};
  const c=decideAndPlan(cloneNpc('disciplinado'),changed,GOAP_ACTIONS);
  assert.equal(c.status,'PLAN_READY');
  assert.deepEqual(c.plan.plan,['enviar_mensajero']);
});

test('controlador salta objetivo imposible y prueba el siguiente',()=>{
  const c=decideAndPlan(cloneNpc('leal'),WORLDS.ayuda_inalcanzable,GOAP_ACTIONS);
  assert.notEqual(c.selectedGoal.id,'HELP_PLAYER');
  assert.ok(c.attempts.some(x=>x.goalId==='HELP_PLAYER' && x.status==='NO_PLAN'));
  assert.equal(c.status,'PLAN_READY');
});

test('planificador no muta el estado inicial',()=>{
  const world=structuredClone(WORLDS.reporte);
  const before=structuredClone(world);
  planGOAP(world,GOALS.REPORT_SUPERIOR,GOAP_ACTIONS);
  assert.deepEqual(world,before);
});

test('executor no muta el mundo de entrada',()=>{
  const world=structuredClone(WORLDS.deber), before=structuredClone(world);
  const c=decideAndPlan(cloneNpc('disciplinado'),world,GOAP_ACTIONS);
  executeNext(c.plan,world,c.selectedGoal.goal,GOAP_ACTIONS);
  assert.deepEqual(world,before);
});

test('finalState del planner satisface el objetivo',()=>{
  const r=planGOAP(WORLDS.reporte,GOALS.REPORT_SUPERIOR,GOAP_ACTIONS);
  assert.equal(r.status,'PLAN_FOUND');
  assert.equal(factsMatch(r.finalState,GOALS.REPORT_SUPERIOR),true);
});

test('executor detecta acción inexistente',()=>{
  const x=executeNext({status:'PLAN_FOUND',plan:['fantasma']},BASE_WORLD,GOALS.WAIT_SAFE,GOAP_ACTIONS);
  assert.equal(x.status,'REPLAN_REQUIRED');
});

test('executor sin plan activo responde NO_ACTIVE_PLAN',()=>{
  assert.equal(executeNext(null,BASE_WORLD,GOALS.WAIT_SAFE,GOAP_ACTIONS).status,'NO_ACTIVE_PLAN');
});

test('RETURN_POST genera regreso desde superior',()=>{
  const world={...BASE_WORLD,at:'superior',playerNeedsHelp:false,anomalyPresent:false,dutyPending:false,hasEvidence:false};
  const c=decideAndPlan(cloneNpc('disciplinado'),world,GOAP_ACTIONS);
  assert.equal(c.selectedGoal.id,'RETURN_POST');
  assert.deepEqual(c.plan.plan,['volver_puesto_desde_superior']);
});

test('WAIT_SAFE es objetivo de último recurso',()=>{
  const world={...BASE_WORLD,playerPresent:false,playerNeedsHelp:false,playerHelped:true,anomalyPresent:false,anomalyInvestigated:true,hasEvidence:false,superiorInformed:true,dutyPending:false,dutySatisfied:true,urgency:0,danger:0};
  const c=decideAndPlan(cloneNpc('disciplinado'),world,GOAP_ACTIONS);
  assert.equal(c.selectedGoal.id,'WAIT_SAFE');
  assert.deepEqual(c.plan.plan,['esperar']);
});

test('deber desde jugador requiere volver antes de cumplir',()=>{
  const world={...WORLDS.deber,at:'jugador'};
  const r=planGOAP(world,GOALS.FULFILL_DUTY,GOAP_ACTIONS);
  assert.deepEqual(r.plan,['volver_puesto_desde_jugador','cumplir_deber']);
});

test('ids de acciones GOAP son únicos',()=>{
  assert.equal(new Set(GOAP_ACTIONS.map(x=>x.id)).size,GOAP_ACTIONS.length);
});

test('rechaza costes no finitos',()=>{
  assert.throws(()=>planGOAP({a:true},{b:true},[{id:'x',cost:Infinity,preconditions:{a:true},effects:{b:true}}]),/Acción inválida/);
});

test('rechaza hechos numéricos no finitos',()=>{
  assert.throws(()=>planGOAP({a:NaN},{done:true},GOAP_ACTIONS),/debe ser finito/);
});

console.log('\n'+passed+' pruebas PASS'+(process.exitCode?' (hubo fallos)':'')+'.');
if (process.exitCode) process.exit(process.exitCode);
