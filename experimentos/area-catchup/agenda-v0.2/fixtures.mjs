export const standardSlots = () => [
  { id: 'rest', start: 0, end: 20, roomId: 'room_dormitory', activity: 'REST' },
  { id: 'train', start: 20, end: 60, roomId: 'room_training', activity: 'TRAIN' },
  { id: 'study', start: 60, end: 80, roomId: 'room_library', activity: 'STUDY' },
  { id: 'meal', start: 80, end: 100, roomId: 'room_dining', activity: 'EAT' }
];

export function standardEntity(id = 'npc_a', offset = 0, turn = 10) {
  const phase = (turn + offset) % 100;
  const slot = standardSlots().find(s => s.start <= phase && phase < s.end);
  return { id, logicalRoomId: slot.roomId, currentActivity: slot.activity,
    agenda: { cycleLength: 100, offset, slots: standardSlots() } };
}

export function makeState(overrides = {}) {
  return { version: 1, areaId: 'area_alpha', syncedTurn: 10, entities: [standardEntity()], ...overrides };
}

export function makeCatchUp(overrides = {}) {
  return { areaId: 'area_alpha', fromTurn: 10, toTurn: 30, elapsedTurns: 20, ...overrides };
}

export function variedEntities(turn = 10) {
  const guard = { id: 'npc_guard', logicalRoomId: 'room_gate', currentActivity: 'GUARD',
    agenda: { cycleLength: 12, offset: 0, slots: [
      { id: 'guard', start: 0, end: 6, roomId: 'room_gate', activity: 'GUARD' },
      { id: 'rest', start: 6, end: 12, roomId: 'room_dormitory', activity: 'REST' }
    ] } };
  // turn 10 is REST for guard.
  guard.logicalRoomId = 'room_dormitory'; guard.currentActivity = 'REST';
  const scholar = { id: 'npc_scholar', logicalRoomId: 'room_library', currentActivity: 'STUDY',
    agenda: { cycleLength: 7, offset: 0, slots: [
      { id: 'work', start: 0, end: 4, roomId: 'room_library', activity: 'STUDY' },
      { id: 'meal', start: 4, end: 7, roomId: 'room_dining', activity: 'EAT' }
    ] } };
  const worker = { id: 'npc_worker', logicalRoomId: 'room_workshop', currentActivity: 'WORK',
    agenda: { cycleLength: 9, offset: 0, slots: [
      { id: 'rest', start: 0, end: 1, roomId: 'room_dormitory', activity: 'REST' },
      { id: 'work', start: 1, end: 9, roomId: 'room_workshop', activity: 'WORK' }
    ] } };
  const fixed = { id: 'npc_fixed', logicalRoomId: 'room_library', currentActivity: 'WORK',
    agenda: { cycleLength: 100, offset: 0, slots: [
      { id: 'always', start: 0, end: 100, roomId: 'room_library', activity: 'WORK' }
    ] } };
  if (turn !== 10) throw new TypeError('variedEntities fixture usa turn 10');
  return [worker, fixed, scholar, guard];
}
