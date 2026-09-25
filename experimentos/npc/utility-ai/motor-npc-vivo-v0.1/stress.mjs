import assert from 'node:assert/strict';
import { chooseAction, evaluateDialogueTopic, validateNpc } from './engine.mjs';

const N = Math.max(1, Number(process.argv[2] || 10000));
let seed = Number(process.argv[3] || 1337) >>> 0;
const rnd = () => { seed = (1664525 * seed + 1013904223) >>> 0; return seed / 2 ** 32; };
const r100 = () => Math.floor(rnd() * 101);
const pick = arr => arr[Math.floor(rnd() * arr.length)];

const actions = new Map();
for (let i = 0; i < N; i++) {
  const npc = {
    id: `stress_${i}`,
    traits: {
      disciplina: r100(), sociabilidad: r100(), curiosidad: r100(), prudencia: r100(),
      lealtad_institucional: r100(), empatia: r100(),
    },
    relationPlayer: {
      afinidad: r100(), confianza: r100(), respeto: r100(), deuda: r100(), temor: r100(), rivalidad: r100(),
    },
    knowledge: {
      R1: pick(['DESCONOCIDO', 'SOSPECHA', 'SABE', 'CONFIRMADO']),
    },
    lastAction: rnd() < 0.25 ? pick(['vigilar','trabajar','patrullar','hablar_jugador','ayudar_jugador','investigar','informar_superior','regresar_puesto','esperar']) : null,
  };
  assert.deepEqual(validateNpc(npc), []);

  const playerPresent = rnd() < 0.7;
  const context = {
    playerPresent,
    playerRequestsHelp: playerPresent && rnd() < 0.45,
    playerRank: Math.floor(rnd() * 7),
    dutyImportance: r100(),
    danger: r100(),
    missionUrgency: r100(),
    anomalyPresent: rnd() < 0.4,
    awayFromPost: rnd() < 0.25,
    superiorReachable: rnd() < 0.9,
    relevantKnowledge: pick(['DESCONOCIDO','SOSPECHA','SABE','CONFIRMADO']),
    topicSensitivity: r100(),
    formalRestriction: r100(),
  };

  const a = chooseAction(npc, context);
  const b = chooseAction(npc, context);
  assert.deepEqual(a, b, 'No determinista con mismo input');
  assert.ok(Number.isFinite(a.score) && a.score >= 0 && a.score <= 100);
  assert.ok(a.ranking.some(x => x.name === a.action && x.available));

  if (!playerPresent) {
    const talk = a.ranking.find(x => x.name === 'hablar_jugador');
    const help = a.ranking.find(x => x.name === 'ayudar_jugador');
    assert.equal(talk.available, false);
    assert.equal(help.available, false);
  }

  const d = evaluateDialogueTopic(npc, 'R1', context);
  if (npc.knowledge.R1 === 'DESCONOCIDO') {
    assert.equal(d.mode, 'NO_SABE');
    assert.equal(d.disclosure, 0);
  }
  if (npc.knowledge.R1 === 'SOSPECHA') assert.notEqual(d.mode, 'COMPARTE');

  actions.set(a.action, (actions.get(a.action) || 0) + 1);
}

console.log(`Stress PASS: ${N} casos · seed final ${seed}`);
console.log(Object.fromEntries([...actions.entries()].sort((a,b)=>b[1]-a[1])));
