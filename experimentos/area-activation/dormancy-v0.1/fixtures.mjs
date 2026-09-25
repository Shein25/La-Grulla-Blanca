export function labAreas() {
  return [
    { id: 'area_alpha' },
    { id: 'area_beta' },
    { id: 'area_gamma' },
    { id: 'area_delta' },
    { id: 'area_isolated' },
  ];
}

export function syntheticAreas(count = 32) {
  return Array.from({ length: count }, (_, index) => ({
    id: `area_${String(index).padStart(3, '0')}`,
  }));
}
