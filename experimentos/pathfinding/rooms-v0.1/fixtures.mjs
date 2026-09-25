export function exits(overrides = {}) {
  return { norte: null, este: null, sur: null, oeste: null,
    arriba: null, abajo: null, ...overrides };
}

// Trece rooms inventadas para este laboratorio. Ninguna pertenece al mapa real.
export function labGraph() {
  return {
    version: 1,
    rooms: [
      { id: 'lab_a', exits: exits({ norte: 'lab_b', este: 'lab_c', sur: 'lab_long_1' }) },
      { id: 'lab_b', exits: exits({ este: 'lab_d' }) },
      { id: 'lab_c', exits: exits({ norte: 'lab_d', oeste: 'lab_a' }) },
      { id: 'lab_d', exits: exits({ sur: 'lab_c', arriba: 'lab_upper_1' }) },
      { id: 'lab_long_1', exits: exits({ este: 'lab_long_2' }) },
      { id: 'lab_long_2', exits: exits({ norte: 'lab_d' }) },
      { id: 'lab_upper_1', exits: exits({ arriba: 'lab_tower', abajo: 'lab_d' }) },
      { id: 'lab_tower', exits: exits({ abajo: 'lab_upper_1' }) },
      { id: 'lab_oneway_a', exits: exits({ norte: 'lab_oneway_b' }) },
      { id: 'lab_oneway_b', exits: exits() },
      { id: 'lab_isolated', exits: exits() },
      { id: 'lab_x', exits: exits({ este: 'lab_y' }) },
      { id: 'lab_y', exits: exits({ oeste: 'lab_x' }) },
    ],
  };
}
