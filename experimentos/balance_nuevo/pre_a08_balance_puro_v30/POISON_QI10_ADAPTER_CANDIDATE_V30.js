/*
 * LA GRULLA BLANCA — PRE-A08 V30 · SOLO CANDIDATO DE INTEGRACIÓN
 * Efecto aprobado de diseño: veneno resta 10% a recuperación de Qi FUERA combate.
 * No insertado en el HTML, no usa legado, no manipula aflicciones ni guardados.
 */
const GB_V30_QI_POISON = (() => {
  'use strict';
  const SOURCES = new Set([
    'MEDITAR', 'MEDITAR_PROFUNDO', 'DORMIR',
    'CONSUMIBLE_QI', 'CONSUMIBLE_HIBRIDO_QI'
  ]);
  const isPoisoned = afflictions => Array.isArray(afflictions)
    && afflictions.some(a => a && a.tipo === 'veneno' && Number(a.duracion) > 0);
  const recovery = ({qiActual, qiMax, recuperacionBruta, fuente, enCombate=false, venenoAlInicio=false}) => {
    if (![qiActual, qiMax, recuperacionBruta].every(Number.isFinite)
        || qiActual < 0 || qiMax < 0 || qiActual > qiMax || recuperacionBruta < 0) {
      throw new RangeError('Qi inválido para recuperación');
    }
    const penaliza = SOURCES.has(fuente) && !enCombate && !!venenoAlInicio && recuperacionBruta > 0;
    // ROUND_HALF_UP, una vez, luego de los modificadores de fuente y ANTES del cap.
    const recuperacionPenalizada = Math.floor(recuperacionBruta * (penaliza ? 0.90 : 1) + 0.5);
    const recuperacionReal = Math.max(0, Math.min(qiMax - qiActual, recuperacionPenalizada));
    return Object.freeze({penaliza, recuperacionPenalizada, recuperacionReal,
      qiFinal:qiActual + recuperacionReal});
  };
  return Object.freeze({SOURCES, isPoisoned, recovery});
})();
if (typeof module !== 'undefined' && module.exports) module.exports = GB_V30_QI_POISON;
