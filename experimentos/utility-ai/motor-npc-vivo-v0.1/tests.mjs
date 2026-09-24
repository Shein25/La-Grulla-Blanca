import assert from 'node:assert/strict';
import { chooseAction, evaluateActions, evaluateDialogueTopic, KNOWLEDGE, simulateTurn, validateNpc } from './engine.mjs';
import { NPCS, cloneNpc } from './npc-fixtures.mjs';
import { BASE_CONTEXT, SCENARIOS } from './scenarios.mjs';

let passed = 0;
const test = (name, fn) => {
  try { fn(); passed++; console.log(`PASS  ${name}`); }
  catch (err) { console.error(`FAIL  ${name}\n      ${err.stack || err}`); process.exitCode = 1; }
};

for (const npc of Object.values(NPCS)) {
  test(`fixture ${npc.id} válido`, () => assert.deepEqual(validateNpc(npc), []));
}

test('misma entrada produce misma decisión', () => {
  const npc = cloneNpc('disciplinado');
  const a = chooseAction(npc, BASE_CONTEXT);
  const b = chooseAction(npc, BASE_CONTEXT);
  assert.deepEqual(a, b);
});

test('NPC disciplinado prioriza deber en puesto crítico', () => {
  const r = chooseAction(cloneNpc('disciplinado'), SCENARIOS.puesto_critico.context);
  assert.equal(r.action, 'vigilar');
});

test('NPC leal ayuda en crisis personal', () => {
  const r = chooseAction(cloneNpc('leal'), SCENARIOS.crisis_personal.context);
  assert.equal(r.action, 'ayudar_jugador');
});

test('NPC curioso investiga anomalía', () => {
  const r = chooseAction(cloneNpc('curioso'), SCENARIOS.anomalia.context);
  assert.equal(r.action, 'investigar');
});

test('disciplinado fuera de puesto prioriza regresar', () => {
  const r = chooseAction(cloneNpc('disciplinado'), SCENARIOS.retorno_puesto.context);
  assert.equal(r.action, 'regresar_puesto');
});

test('sin jugador hablar y ayudar están bloqueados', () => {
  const scores = evaluateActions(cloneNpc('leal'), { ...BASE_CONTEXT, playerPresent: false, playerRequestsHelp: true });
  const talk = scores.find(x => x.name === 'hablar_jugador');
  const help = scores.find(x => x.name === 'ayudar_jugador');
  assert.equal(talk.available, false);
  assert.equal(help.available, false);
});

test('conocimiento DESCONOCIDO jamás se revela', () => {
  const r = evaluateDialogueTopic(cloneNpc('leal'), 'R2', { playerRank: 6, topicSensitivity: 0, formalRestriction: 0 });
  assert.equal(r.state, 'DESCONOCIDO');
  assert.equal(r.mode, 'NO_SABE');
  assert.equal(r.disclosure, 0);
});

test('SOSPECHA nunca escala a COMPARTE como hecho confirmado', () => {
  const npc = cloneNpc('disciplinado');
  npc.relationPlayer.confianza = 100;
  npc.relationPlayer.afinidad = 100;
  npc.relationPlayer.respeto = 100;
  npc.relationPlayer.deuda = 100;
  npc.traits.prudencia = 0;
  const r = evaluateDialogueTopic(npc, 'R1', { playerRank: 6, topicSensitivity: 0, formalRestriction: 0 });
  assert.equal(r.state, 'SOSPECHA');
  assert.notEqual(r.mode, 'COMPARTE');
});

test('un tema conocido puede quedar reservado por sensibilidad y restricción', () => {
  const npc = cloneNpc('leal');
  npc.relationPlayer.confianza = 10;
  npc.relationPlayer.afinidad = 10;
  const r = evaluateDialogueTopic(npc, 'R1', { playerRank: 0, topicSensitivity: 100, formalRestriction: 100 });
  assert.equal(r.state, 'SABE');
  assert.equal(r.mode, 'RESERVA');
});

test('simular turno conserva input y devuelve nextNpc separado', () => {
  const npc = cloneNpc('curioso');
  const before = structuredClone(npc);
  const r = simulateTurn(npc, SCENARIOS.anomalia.context);
  assert.deepEqual(npc, before);
  assert.notEqual(r.nextNpc, npc);
  assert.equal(r.nextNpc.lastAction, r.action);
});

test('todas las puntuaciones disponibles quedan en 0..100', () => {
  for (const npc of Object.values(NPCS)) {
    for (const sc of Object.values(SCENARIOS)) {
      for (const x of evaluateActions(npc, sc.context)) {
        if (x.available) assert.ok(Number.isFinite(x.score) && x.score >= 0 && x.score <= 100, `${npc.id}/${x.name}=${x.score}`);
      }
    }
  }
});

test('tabla KNOWLEDGE conserva orden semántico', () => {
  assert.ok(KNOWLEDGE.DESCONOCIDO < KNOWLEDGE.SOSPECHA);
  assert.ok(KNOWLEDGE.SOSPECHA < KNOWLEDGE.SABE);
  assert.ok(KNOWLEDGE.SABE < KNOWLEDGE.CONFIRMADO);
});

console.log(`\n${passed} pruebas PASS${process.exitCode ? ' (hubo fallos)' : ''}.`);
if (process.exitCode) process.exit(process.exitCode);
