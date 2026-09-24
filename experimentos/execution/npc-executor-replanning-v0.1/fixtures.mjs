export function makeWorld(overrides = {}) {
  return { at: 'puesto', playerPresent: true, playerNeedsHelp: true, playerReachable: true,
    playerHelped: false, routeAOpen: true, routeBOpen: true, ...overrides };
}

export function makeActions() {
  return [
    { id: 'ir_a', cost: 1, preconditions: { at: 'puesto', routeAOpen: true }, effects: { at: 'a' } },
    { id: 'usar_a', cost: 1, preconditions: { at: 'a', routeAOpen: true, playerNeedsHelp: true }, effects: { playerHelped: true, playerNeedsHelp: false } },
    { id: 'volver', cost: 1, preconditions: { at: 'a' }, effects: { at: 'puesto' } },
    { id: 'ir_b', cost: 1, preconditions: { at: 'puesto', routeBOpen: true }, effects: { at: 'b' } },
    { id: 'usar_b', cost: 1, preconditions: { at: 'b', routeBOpen: true, playerNeedsHelp: true }, effects: { playerHelped: true, playerNeedsHelp: false } },
    { id: 'volver_b', cost: 1, preconditions: { at: 'b' }, effects: { at: 'puesto' } },
  ];
}

export function makeInitialConfig(overrides = {}) {
  return { goalId: 'HELP_PLAYER', goal: { playerHelped: true },
    relevance: { playerPresent: true, playerNeedsHelp: true },
    plan: ['ir_a', 'usar_a'], ...overrides };
}
