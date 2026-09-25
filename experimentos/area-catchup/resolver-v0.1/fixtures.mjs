export function makeState(overrides = {}) {
  return {
    version: 1, areaId: 'area_alpha', syncedTurn: 100,
    entities: [{ id: 'entity_a', timers: [{ id: 'cooldown', remainingTurns: 50 }],
      meters: [{ id: 'energy', value: 30, ratePerTurn: 2, min: 0, max: 100 }] }],
    scheduledEvents: [], ...overrides
  };
}

export function makeCatchUp(overrides = {}) {
  return { areaId: 'area_alpha', fromTurn: 100, toTurn: 120, elapsedTurns: 20, ...overrides };
}

export function goldenEvents() {
  return makeState({ scheduledEvents: [
    { id: 'event_b', targetId: null, kind: 'SYNTHETIC_EVENT', dueTurn: 300 },
    { id: 'event_c', targetId: 'entity_a', kind: 'SYNTHETIC_EVENT', dueTurn: 200 },
    { id: 'event_a', targetId: 'entity_a', kind: 'SYNTHETIC_EVENT', dueTurn: 150 }
  ] });
}
