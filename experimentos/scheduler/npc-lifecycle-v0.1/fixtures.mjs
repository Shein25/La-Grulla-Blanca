export function goldenConfig(id = 'scheduler_a', overrides = {}) {
  return { id, interval: 10, minGap: 3, firstPeriodicTurn: 10, ...overrides };
}

export function syntheticConfigs(count = 64) {
  return Array.from({ length: count }, (_, index) => ({
    id: `scheduler_${String(index).padStart(3, '0')}`,
    interval: 7 + index % 17,
    minGap: index % 8,
    firstPeriodicTurn: 2 + index % 19,
  }));
}
