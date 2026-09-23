export const NPCS = Object.freeze({
  disciplinado: {
    id: 'disciplinado', name: 'El Disciplinado', role: 'Guardián de puesto crítico',
    traits: { disciplina: 95, sociabilidad: 25, curiosidad: 20, prudencia: 85, lealtad_institucional: 95, empatia: 40 },
    relationPlayer: { afinidad: 35, confianza: 40, respeto: 65, deuda: 0, temor: 5, rivalidad: 5 },
    knowledge: { R1: 'SOSPECHA', R2: 'DESCONOCIDO', R3: 'SABE' },
    behaviorState: { lastAction: null, consecutiveTurns: 0 },
  },
  leal: {
    id: 'leal', name: 'El Leal', role: 'Compañero orientado al vínculo',
    traits: { disciplina: 50, sociabilidad: 75, curiosidad: 50, prudencia: 45, lealtad_institucional: 45, empatia: 95 },
    relationPlayer: { afinidad: 90, confianza: 90, respeto: 75, deuda: 45, temor: 0, rivalidad: 0 },
    knowledge: { R1: 'SABE', R2: 'DESCONOCIDO', R3: 'SOSPECHA' },
    behaviorState: { lastAction: null, consecutiveTurns: 0 },
  },
  curioso: {
    id: 'curioso', name: 'El Curioso', role: 'Investigador impulsado por anomalías',
    traits: { disciplina: 38, sociabilidad: 55, curiosidad: 98, prudencia: 25, lealtad_institucional: 50, empatia: 55 },
    relationPlayer: { afinidad: 45, confianza: 45, respeto: 45, deuda: 0, temor: 5, rivalidad: 5 },
    knowledge: { R1: 'CONFIRMADO', R2: 'SOSPECHA', R3: 'DESCONOCIDO' },
    behaviorState: { lastAction: null, consecutiveTurns: 0 },
  },
});

export function cloneNpc(id) {
  const npc = NPCS[id];
  if (!npc) throw new Error(`NPC fixture desconocido: ${id}`);
  return structuredClone(npc);
}
