import assert from 'node:assert/strict';
import { GOAP_ACTIONS } from './actions.mjs';
import { decideAndPlan } from './controller.mjs';
import { executeNext, executeWholePlan } from './executor.mjs';
import { GOALS, GOAL_RELEVANCE, selectGoal } from './goal-selector.mjs';
import { factsMatch, planGOAP } from './goap.mjs';
import { BASE_WORLD, WORLDS } from './world-fixtures.mjs';
import { cloneNpc } from '../../utility-ai/motor-npc-vivo-v0.1.1/npc-fixtures.mjs';

let passed=0;
const test=(name,fn)=>{
  try { fn(); passed++; console.log('PASS  '+name); }
  catch(err) { console.error('FAIL  '+name+'\n      '+(err.stack||err)); process.exitCode=1; }
};

test('planner devuelve plan vacío si objetivo ya está satisfecho',()=>{
  const r=planGOAP({done:true},{done:true},[{id:'x',cost:1,preconditions:{done:false},effects:{done:true}}]);
  assert.equal(r.status,'PLAN_FOUND'); assert.deepEqual(r.plan,[]); assert.equal(r.cost,0);
});

test('planner elige coste total mínimo',()=>{
  const actions=[
    {id:'caro',cost:5,preconditions:{start:true},effects:{done:true}},
    {id:'paso1',cost:1,preconditions:{start:true},effects:{mid:true}},
    {id:'paso2',cost:1,preconditions:{mid:true},effects:{done:true}},
  ];
  const r=planGOAP({start:true,mid:false,done:false},{done:true},actions);
  assert.deepEqual(r.plan,['paso1','paso2']); assert.equal(r.cost,2);
});

test('empate GOAP es determinista por id',()=>{
  const actions=[
    {id:'z',cost:1,preconditions:{start:true},effects:{done:true}},
    {id:'a',cost:1,preconditions:{start:true},effects:{done:true}},
  ];
  const r=planGOAP({start:true,done:false},{done:true},actions);
  assert.deepEqual(r.plan,['a']);
});

test('desempate lexicográfico usa secuencia de IDs y no JSON serializado',()=>{
  const actions=[
    {id:'a!',cost:1,preconditions:{x:0},effects:{x:1}},
    {id:'a',cost:1,preconditions:{x:0},effects:{x:1}},
  ];
  const r=planGOAP({x:0},{x:1},actions);
  assert.deepEqual(r.plan,['a']);
});

test('desempate lexicográfico por secuencia es estable con puntuación y longitudes distintas',()=>{
  const actions=[
    {id:'a!',cost:1,preconditions:{stage:0},effects:{stage:1,route:'bang'}},
    {id:'a',cost:1,preconditions:{stage:0},effects:{stage:1,route:'plain'}},
    {id:'z',cost:1,preconditions:{stage:1,route:'plain'},effects:{done:true}},
    {id:'b',cost:1,preconditions:{stage:1,route:'bang'},effects:{done:true}},
  ];
  const r=planGOAP({stage:0,route:'',done:false},{done:true},actions);
  assert.deepEqual(r.plan,['a','z']);
  assert.equal(r.cost,2);
});

test('empate de coste prefiere menos pasos',()=>{
  const actions=[
    {id:'directo',cost:2,preconditions:{start:true},effects:{done:true}},
    {id:'p1',cost:1,preconditions:{start:true},effects:{mid:true}},
    {id:'p2',cost:1,preconditions:{mid:true},effects:{done:true}},
  ];
  const r=planGOAP({start:true,mid:false,done:false},{done:true},actions);
  assert.deepEqual(r.plan,['directo']);
});

test('planner devuelve NO_PLAN cuando no existe camino',()=>{
  const r=planGOAP({a:false},{a:true},[{id:'x',cost:1,preconditions:{a:true},effects:{a:false}}]);
  assert.equal(r.status,'NO_PLAN');
});

test('-0 y 0 conservan identidad compatible con Object.is',()=>{
  const r=planGOAP({x:-0},{x:0},[{id:'set_zero',cost:1,preconditions:{},effects:{x:0}}]);
  assert.equal(r.status,'PLAN_FOUND');
  assert.deepEqual(r.plan,['set_zero']);
  assert.equal(r.cost,1);
});

test('costes deben ser enteros seguros positivos',()=>{
  for (const bad of [0,-1,1.5,Number.MIN_VALUE,1e308,NaN,Infinity,-Infinity]) {
    assert.throws(
      ()=>planGOAP({a:true},{b:true},[{id:'x',cost:bad,preconditions:{a:true},effects:{b:true}}]),
      /Acción inválida/
    );
  }
});

test('desborde acumulado devuelve COST_OVERFLOW y nunca Infinity',()=>{
  const actions=[
    {id:'stage1',cost:Number.MAX_SAFE_INTEGER,preconditions:{stage:0},effects:{stage:1}},
    {id:'stage2',cost:1,preconditions:{stage:1},effects:{stage:2}},
  ];
  const r=planGOAP({stage:0},{stage:2},actions);
  assert.equal(r.status,'COST_OVERFLOW');
  assert.equal(r.cost,null);
});

test('maxExpansions negativo se rechaza',()=>{
  assert.throws(()=>planGOAP({a:false},{a:true},[{id:'x',cost:1,preconditions:{a:false},effects:{a:true}}],{maxExpansions:-1}),/maxExpansions/);
});

test('maxExpansions cero no consume una expansión',()=>{
  const r=planGOAP({a:false},{a:true},[{id:'x',cost:1,preconditions:{a:false},effects:{a:true}}],{maxExpansions:0});
  assert.equal(r.status,'SEARCH_LIMIT');
  assert.equal(r.expansions,0);
});

test('límite exacto permite encontrar goal generado por última expansión',()=>{
  const r=planGOAP({a:false},{a:true},[{id:'x',cost:1,preconditions:{a:false},effects:{a:true}}],{maxExpansions:1});
  assert.equal(r.status,'PLAN_FOUND');
  assert.equal(r.expansions,1);
});

test('caminos equivalentes no explotan exponencialmente',()=>{
  const actions=[];
  for(let i=0;i<12;i++){
    actions.push({id:`a_${i}`,cost:1,preconditions:{stage:i},effects:{stage:i+1}});
    actions.push({id:`b_${i}`,cost:1,preconditions:{stage:i},effects:{stage:i+1}});
  }
  const r=planGOAP({stage:0},{stage:12},actions,{maxExpansions:100});
  assert.equal(r.status,'PLAN_FOUND');
  assert.equal(r.cost,12);
  assert.ok(r.expansions<=12,`expansions=${r.expansions}`);
  assert.ok(r.maxFrontier<=1,`maxFrontier=${r.maxFrontier}`);
});

test('flags irrelevantes no multiplican identidad de estado',()=>{
  const state={done:false,blocked:true};
  for(let i=0;i<12;i++) state['noise'+i]=false;
  const actions=[{id:'x',cost:1,preconditions:{blocked:false},effects:{done:true}}];
  const r=planGOAP(state,{done:true},actions,{maxExpansions:10});
  assert.equal(r.status,'NO_PLAN');
  assert.equal(r.expansions,1);
  assert.deepEqual(r.relevantFacts,['blocked','done']);
});

test('maxFrontier inválido se rechaza',()=>{
  assert.throws(()=>planGOAP({a:false},{a:true},[{id:'x',cost:1,preconditions:{a:false},effects:{a:true}}],{maxFrontier:0}),/maxFrontier/);
});

test('maxFrontier corta la búsqueda sin exceder el límite',()=>{
  const actions=[
    {id:'a',cost:1,preconditions:{stage:0},effects:{stage:1}},
    {id:'b',cost:1,preconditions:{stage:0},effects:{stage:2}},
    {id:'finish1',cost:1,preconditions:{stage:1},effects:{stage:3}},
    {id:'finish2',cost:1,preconditions:{stage:2},effects:{stage:3}},
  ];
  const r=planGOAP({stage:0},{stage:3},actions,{maxExpansions:10,maxFrontier:1});
  assert.equal(r.status,'FRONTIER_LIMIT');
  assert.ok(r.maxFrontier<=1);
});

test('FRONTIER_LIMIT es inconcluso y no equivale a NO_PLAN',()=>{
  const actions=[
    ...GOAP_ACTIONS,
    {id:'ruido_a',cost:1,preconditions:{at:'puesto'},effects:{playerHelped:false,at:'jugador'}},
    {id:'ruido_b',cost:1,preconditions:{at:'puesto'},effects:{playerHelped:false,at:'superior'}},
  ];
  const r=decideAndPlan(cloneNpc('leal'),WORLDS.crisis_jugador,actions,{maxExpansions:100,maxFrontier:1});
  assert.equal(r.status,'PLANNING_DEFERRED');
  assert.equal(r.reason,'FRONTIER_LIMIT');
  assert.equal(r.selectedGoal.id,'HELP_PLAYER');
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

test('SEARCH_LIMIT no hace fallback a objetivo inferior',()=>{
  const r=decideAndPlan(cloneNpc('leal'),WORLDS.comun,GOAP_ACTIONS,{maxExpansions:0});
  assert.equal(r.status,'PLANNING_DEFERRED');
  assert.equal(r.reason,'SEARCH_LIMIT');
  assert.equal(r.selectedGoal.id,'HELP_PLAYER');
  assert.equal(r.attempts.length,1);
});

test('NO_PLAN sí permite fallback legítimo',()=>{
  const r=decideAndPlan(cloneNpc('leal'),WORLDS.ayuda_inalcanzable,GOAP_ACTIONS);
  assert.equal(r.status,'PLAN_READY');
  assert.notEqual(r.selectedGoal.id,'HELP_PLAYER');
  assert.equal(r.attempts[0].goalId,'HELP_PLAYER');
  assert.equal(r.attempts[0].status,'NO_PLAN');
});

test('executor ejecuta plan completo y alcanza objetivo',()=>{
  const c=decideAndPlan(cloneNpc('leal'),WORLDS.crisis_jugador,GOAP_ACTIONS);
  const x=executeWholePlan(c.plan,WORLDS.crisis_jugador,c.selectedGoal.goal,GOAP_ACTIONS,30,c.selectedGoal.relevance);
  assert.equal(x.status,'GOAL_REACHED');
  assert.equal(x.world.playerHelped,true);
  assert.equal(x.world.playerNeedsHelp,false);
});

test('executor exige replanning si cambian precondiciones',()=>{
  const c=decideAndPlan(cloneNpc('disciplinado'),WORLDS.reporte,GOAP_ACTIONS);
  const changed={...WORLDS.reporte,passageOpen:false};
  const x=executeNext(c.plan,changed,c.selectedGoal.goal,GOAP_ACTIONS,c.selectedGoal.relevance);
  assert.equal(x.status,'REPLAN_REQUIRED');
  assert.equal(x.executed,null);
  assert.equal(x.goalObsolete,false);
});

test('plan del controller lleva goal y relevancia vinculados',()=>{
  const c=decideAndPlan(cloneNpc('leal'),WORLDS.crisis_jugador,GOAP_ACTIONS);
  assert.deepEqual(c.plan.goal,c.selectedGoal.goal);
  assert.deepEqual(c.plan.relevance,c.selectedGoal.relevance);
  assert.equal(c.plan.goalId,'HELP_PLAYER');
});

test('relevancia vinculada protege aunque se omita el quinto argumento',()=>{
  const c=decideAndPlan(cloneNpc('leal'),WORLDS.crisis_jugador,GOAP_ACTIONS);
  const changed={...WORLDS.crisis_jugador,playerNeedsHelp:false};
  const x=executeNext(c.plan,changed,c.selectedGoal.goal,GOAP_ACTIONS);
  assert.equal(x.status,'REPLAN_REQUIRED');
  assert.equal(x.goalObsolete,true);
  assert.equal(x.executed,null);
  assert.equal(x.world.at,'puesto');
});

test('executeWholePlan usa relevancia vinculada aunque se omita el sexto argumento',()=>{
  const c=decideAndPlan(cloneNpc('leal'),WORLDS.crisis_jugador,GOAP_ACTIONS);
  const changed={...WORLDS.crisis_jugador,playerNeedsHelp:false};
  const x=executeWholePlan(c.plan,changed,c.selectedGoal.goal,GOAP_ACTIONS,30);
  assert.equal(x.status,'REPLAN_REQUIRED');
  assert.equal(x.trace.length,1);
  assert.equal(x.trace[0].executed,null);
  assert.equal(x.trace[0].goalObsolete,true);
  assert.equal(x.world.at,'puesto');
});

test('plan no vinculado sin relevance se rechaza antes de efectos',()=>{
  const plan={status:'PLAN_FOUND',plan:['ir_jugador']};
  assert.throws(
    ()=>executeNext(plan,WORLDS.crisis_jugador,GOALS.HELP_PLAYER,GOAP_ACTIONS),
    /relevance es obligatoria/
  );
});

test('contrato vinculado rechaza relevance explícita contradictoria',()=>{
  const c=decideAndPlan(cloneNpc('leal'),WORLDS.crisis_jugador,GOAP_ACTIONS);
  assert.throws(
    ()=>executeNext(c.plan,WORLDS.crisis_jugador,c.selectedGoal.goal,GOAP_ACTIONS,{playerNeedsHelp:false}),
    /relevance explícita no coincide/
  );
});

test('objetivo obsoleto se detecta antes de movimiento aún legal',()=>{
  const c=decideAndPlan(cloneNpc('leal'),WORLDS.crisis_jugador,GOAP_ACTIONS);
  const changed={...WORLDS.crisis_jugador,playerNeedsHelp:false};
  const x=executeNext(c.plan,changed,c.selectedGoal.goal,GOAP_ACTIONS,c.selectedGoal.relevance);
  assert.equal(x.status,'REPLAN_REQUIRED');
  assert.equal(x.goalObsolete,true);
  assert.equal(x.executed,null);
  assert.equal(x.world.at,changed.at);
});

test('replanning encuentra mensajero después del cierre del paso',()=>{
  const changed={...WORLDS.reporte,passageOpen:false};
  const c=decideAndPlan(cloneNpc('disciplinado'),changed,GOAP_ACTIONS);
  assert.equal(c.status,'PLAN_READY');
  assert.deepEqual(c.plan.plan,['enviar_mensajero']);
});

test('planificador no muta el estado inicial',()=>{
  const world=structuredClone(WORLDS.reporte), before=structuredClone(world);
  planGOAP(world,GOALS.REPORT_SUPERIOR,GOAP_ACTIONS);
  assert.deepEqual(world,before);
});

test('executor no muta el mundo de entrada',()=>{
  const world=structuredClone(WORLDS.deber), before=structuredClone(world);
  const c=decideAndPlan(cloneNpc('disciplinado'),world,GOAP_ACTIONS);
  executeNext(c.plan,world,c.selectedGoal.goal,GOAP_ACTIONS,c.selectedGoal.relevance);
  assert.deepEqual(world,before);
});

test('finalState del planner satisface el objetivo',()=>{
  const r=planGOAP(WORLDS.reporte,GOALS.REPORT_SUPERIOR,GOAP_ACTIONS);
  assert.equal(r.status,'PLAN_FOUND');
  assert.equal(factsMatch(r.finalState,GOALS.REPORT_SUPERIOR),true);
});

test('executor detecta acción inexistente',()=>{
  const x=executeNext({status:'PLAN_FOUND',plan:['fantasma']},BASE_WORLD,GOALS.WAIT_SAFE,GOAP_ACTIONS,GOAL_RELEVANCE.WAIT_SAFE);
  assert.equal(x.status,'REPLAN_REQUIRED');
});

test('executor sin plan activo responde NO_ACTIVE_PLAN',()=>{
  assert.equal(executeNext(null,BASE_WORLD,GOALS.WAIT_SAFE,GOAP_ACTIONS,GOAL_RELEVANCE.WAIT_SAFE).status,'NO_ACTIVE_PLAN');
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

test('rechaza hechos numéricos no finitos',()=>{
  assert.throws(()=>planGOAP({a:NaN},{done:true},GOAP_ACTIONS),/debe ser finito/);
});

test('maxSteps cero devuelve STEP_LIMIT sin ejecutar',()=>{
  const c=decideAndPlan(cloneNpc('leal'),WORLDS.crisis_jugador,GOAP_ACTIONS);
  const x=executeWholePlan(c.plan,WORLDS.crisis_jugador,c.selectedGoal.goal,GOAP_ACTIONS,0,c.selectedGoal.relevance);
  assert.equal(x.status,'STEP_LIMIT');
  assert.equal(x.trace.length,0);
});

test('maxSteps negativo se rechaza',()=>{
  const c=decideAndPlan(cloneNpc('leal'),WORLDS.crisis_jugador,GOAP_ACTIONS);
  assert.throws(
    ()=>executeWholePlan(c.plan,WORLDS.crisis_jugador,c.selectedGoal.goal,GOAP_ACTIONS,-1,c.selectedGoal.relevance),
    /maxSteps/
  );
});

console.log('\n'+passed+' pruebas PASS'+(process.exitCode?' (hubo fallos)':'')+'.');
if (process.exitCode) process.exit(process.exitCode);
