import assert from 'node:assert/strict';
import { ACTION_ORDER, chooseAction, evaluateActions, evaluateDialogueTopic, KNOWLEDGE, simulateTurn, validateActionContext, validateNpc } from './engine.mjs';
import { NPCS, cloneNpc } from './npc-fixtures.mjs';
import { BASE_CONTEXT, SCENARIOS } from './scenarios.mjs';

let passed = 0;
const test = (name, fn) => {
  try { fn(); passed++; console.log(`PASS  ${name}`); }
  catch (err) { console.error(`FAIL  ${name}\n      ${err.stack || err}`); process.exitCode = 1; }
};

for (const npc of Object.values(NPCS)) test(`fixture ${npc.id} válido`, () => assert.deepEqual(validateNpc(npc), []));
test('contexto base válido', () => assert.deepEqual(validateActionContext(BASE_CONTEXT), []));

test('validateNpc rechaza traits incompletos', () => {
  const n = cloneNpc('leal'); n.traits = {};
  assert.ok(validateNpc(n).some(x => x.includes('traits: faltan')));
  assert.throws(() => chooseAction(n, BASE_CONTEXT), /NPC inválido/);
});

test('validateNpc rechaza relationPlayer incompleto', () => {
  const n = cloneNpc('leal'); n.relationPlayer = {};
  assert.ok(validateNpc(n).some(x => x.includes('relationPlayer: faltan')));
});

test('validateNpc rechaza knowledge incompleto', () => {
  const n = cloneNpc('leal'); delete n.knowledge.R3;
  assert.ok(validateNpc(n).some(x => x.includes('knowledge: faltan R3')));
});

test('validateActionContext rechaza rango y dutyMode inválidos', () => {
  const c = { ...BASE_CONTEXT, playerRank: 7, dutyMode: 'inventado' };
  const e = validateActionContext(c);
  assert.ok(e.some(x => x.includes('playerRank')) && e.some(x => x.includes('dutyMode')));
});

test('misma entrada produce misma decisión', () => {
  const npc = cloneNpc('disciplinado');
  assert.deepEqual(chooseAction(npc, BASE_CONTEXT), chooseAction(npc, BASE_CONTEXT));
});

test('NPC disciplinado prioriza deber en puesto crítico', () => assert.equal(chooseAction(cloneNpc('disciplinado'), SCENARIOS.puesto_critico.context).action, 'vigilar'));
test('NPC leal ayuda en crisis personal', () => assert.equal(chooseAction(cloneNpc('leal'), SCENARIOS.crisis_personal.context).action, 'ayudar_jugador'));
test('NPC curioso investiga anomalía', () => assert.equal(chooseAction(cloneNpc('curioso'), SCENARIOS.anomalia.context).action, 'investigar'));
test('disciplinado fuera de puesto prioriza regresar', () => assert.equal(chooseAction(cloneNpc('disciplinado'), SCENARIOS.retorno_puesto.context).action, 'regresar_puesto'));
test('trabajar gana con tarea asignada y sin estímulos competidores', () => assert.equal(chooseAction(cloneNpc('disciplinado'), SCENARIOS.rutina_trabajo.context).action, 'trabajar'));
test('esperar gana sin tarea ni estímulos', () => assert.equal(chooseAction(cloneNpc('disciplinado'), SCENARIOS.espera_sin_tarea.context).action, 'esperar'));

test('dutyMode bloquea deberes no asignados', () => {
  const scores = evaluateActions(cloneNpc('disciplinado'), SCENARIOS.rutina_trabajo.context);
  assert.equal(scores.find(x=>x.name==='trabajar').available, true);
  assert.equal(scores.find(x=>x.name==='vigilar').available, false);
  assert.equal(scores.find(x=>x.name==='patrullar').available, false);
});

test('sin jugador hablar y ayudar están bloqueados', () => {
  const scores = evaluateActions(cloneNpc('leal'), { ...BASE_CONTEXT, playerPresent:false, playerRequestsHelp:true });
  assert.equal(scores.find(x=>x.name==='hablar_jugador').available, false);
  assert.equal(scores.find(x=>x.name==='ayudar_jugador').available, false);
});

test('DESCONOCIDO jamás se revela', () => {
  const r = evaluateDialogueTopic(cloneNpc('leal'), 'R2', { playerRank:6, topicSensitivity:0, formalRestriction:0 });
  assert.equal(r.mode, 'NO_SABE'); assert.equal(r.disclosure, 0);
});

test('SOSPECHA nunca escala a COMPARTE', () => {
  const n=cloneNpc('disciplinado');
  n.relationPlayer={afinidad:100,confianza:100,respeto:100,deuda:100,temor:0,rivalidad:0};
  n.traits.prudencia=0;
  assert.notEqual(evaluateDialogueTopic(n,'R1',{playerRank:6,topicSensitivity:0,formalRestriction:0}).mode,'COMPARTE');
});

test('tema conocido puede quedar reservado', () => {
  const n=cloneNpc('leal'); n.relationPlayer.confianza=10; n.relationPlayer.afinidad=10;
  assert.equal(evaluateDialogueTopic(n,'R1',{playerRank:0,topicSensitivity:100,formalRestriction:100}).mode,'RESERVA');
});

test('simulateTurn hace copia profunda independiente', () => {
  const original=cloneNpc('leal'), before=structuredClone(original);
  const next=simulateTurn(original, BASE_CONTEXT).nextNpc;
  assert.deepEqual(original,before); assert.notEqual(next,original);
  next.traits.disciplina=0; next.relationPlayer.confianza=0; next.knowledge.R1='DESCONOCIDO';
  assert.equal(original.traits.disciplina,before.traits.disciplina);
  assert.equal(original.relationPlayer.confianza,before.relationPlayer.confianza);
  assert.equal(original.knowledge.R1,before.knowledge.R1);
});

test('inercia decrece 6→4→2→0', () => {
  let n=cloneNpc('curioso');
  const c={...SCENARIOS.retorno_puesto.context, missionUrgency:0};
  n.behaviorState={lastAction:'regresar_puesto',consecutiveTurns:1};
  const bonuses=[];
  for(let i=0;i<4;i++){
    const ev=evaluateActions(n,c).find(x=>x.name==='regresar_puesto');
    bonuses.push(ev.contributions.find(x=>x.label==='inercia decreciente')?.value||0);
    n.behaviorState.consecutiveTurns++;
  }
  assert.deepEqual(bonuses,[6,4,2,0]);
});

test('empate a score 100 se resuelve por raw', () => {
  const n=cloneNpc('disciplinado');
  const c={...BASE_CONTEXT,dutyMode:'ninguno',awayFromPost:true,danger:100,missionUrgency:100,dutyImportance:100};
  const r=chooseAction(n,c);
  const tops=r.ranking.filter(x=>x.available&&x.score===100);
  if(tops.length>1) assert.equal(r.raw,Math.max(...tops.map(x=>x.raw)));
  assert.equal(r.tieBreak,'score > raw > ACTION_ORDER');
});

test('scores disponibles quedan en 0..100', () => {
  for(const npc of Object.values(NPCS)) for(const sc of Object.values(SCENARIOS)) for(const x of evaluateActions(npc,sc.context))
    if(x.available) assert.ok(Number.isFinite(x.score)&&x.score>=0&&x.score<=100,`${npc.id}/${x.name}=${x.score}`);
});

test('tabla KNOWLEDGE conserva orden semántico', () => {
  assert.ok(KNOWLEDGE.DESCONOCIDO<KNOWLEDGE.SOSPECHA&&KNOWLEDGE.SOSPECHA<KNOWLEDGE.SABE&&KNOWLEDGE.SABE<KNOWLEDGE.CONFIRMADO);
});

test('ACTION_ORDER contiene acciones únicas',()=>assert.equal(new Set(ACTION_ORDER).size,ACTION_ORDER.length));

console.log(`\n${passed} pruebas PASS${process.exitCode ? ' (hubo fallos)' : ''}.`);
if(process.exitCode) process.exit(process.exitCode);
