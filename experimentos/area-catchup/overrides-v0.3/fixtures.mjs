export const standardSlots = () => [
  { id: 'rest', start: 0, end: 20, roomId: 'room_dormitory', activity: 'REST' },
  { id: 'train', start: 20, end: 60, roomId: 'room_training', activity: 'TRAIN' },
  { id: 'study', start: 60, end: 80, roomId: 'room_library', activity: 'STUDY' },
  { id: 'meal', start: 80, end: 100, roomId: 'room_dining', activity: 'EAT' }
];

export function makeOverride(overrides = {}) {
  return { id: 'medical', kind: 'MEDICAL_RECOVERY', priority: 100,
    startTurn: 20, endTurn: 100, roomId: 'room_infirmary', activity: 'RECOVER', ...overrides };
}

export function makeEntity(overrides = {}) {
  return { id: 'npc_a', logicalRoomId: 'room_dormitory', currentActivity: 'REST',
    currentSourceType: 'AGENDA', currentSourceId: 'rest',
    agenda: { cycleLength: 100, offset: 0, slots: standardSlots() }, overrides: [], ...overrides };
}

export function makeState(overrides = {}) {
  return { version: 1, areaId: 'area_alpha', syncedTurn: 10, entities: [makeEntity()], ...overrides };
}

export function makeCatchUp(overrides = {}) {
  return { areaId: 'area_alpha', fromTurn: 10, toTurn: 30, elapsedTurns: 20, ...overrides };
}

export function entityAt(turn, overrides = [], changes = {}) {
  const slots = standardSlots();
  const phase = Number(BigInt(turn) % 100n);
  const slot = slots.find(s => s.start <= phase && phase < s.end);
  const active = overrides.filter(o => o.startTurn <= turn && (o.endTurn === null || turn < o.endTurn));
  active.sort((a, b) => b.priority - a.priority || b.startTurn - a.startTurn || (a.id < b.id ? -1 : a.id > b.id ? 1 : 0));
  const winner = active[0];
  return makeEntity({ logicalRoomId: winner?.roomId ?? slot.roomId,
    currentActivity: winner?.activity ?? slot.activity,
    currentSourceType: winner ? 'OVERRIDE' : 'AGENDA', currentSourceId: winner?.id ?? slot.id,
    overrides, ...changes });
}
