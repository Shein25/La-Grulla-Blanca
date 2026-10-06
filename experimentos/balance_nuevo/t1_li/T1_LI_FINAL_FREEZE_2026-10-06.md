# LI — T1 final freeze

**Fecha:** 2026-10-06  
**Rama:** `experiment/li-monster-t0-final-t1-lab-v0.1`  
**Status:** `T1_LI_FINAL_FREEZE_2026-10-06`

## Alcance

Cierre humano del tier adaptativo T1 para los cinco monstruos LI.  
T0 permanece congelado. No se reabre balance por raíz. No se toca `main`. No merge.

## Autoridad de cierre

### Gate final conjunto V02

- Artefacto: `LI_MONSTER_T1_FINAL_EXHAUSTIVE_GATE_V02_REVIEW.zip`
- Combates representados: **3,033,600**
- 4,864 firmas mecánicas / 6,144 loadouts crudos
- R12 exhaustivo + perfiles R128 T1/T0 pareados + worst-tail R128 T1/T0 pareados
- 0 timeouts
- root spread calculado correctamente entre raíces después de promediar policies

El gate cerró directamente:
- Serpiente Qi
- Avispa Jade
- Mono Píldoras
- Lobo Espiritual

Rata Qi fue el único bloqueo del gate por `+60 EVA / CD6`: EXPECTED T1 quedó +2.265625 pp más fácil que su T0 pareado, apenas fuera del guardrail +2 pp.

### Suplemento focal Rata +70 V02

- Artefacto: `RATA_T1_PLUS70_FOCAL_V02_REVIEW.zip`
- SHA-256 review: `b6786f4880a38d30d2c2f101d1ae7fcd4068204bef1102de7e535aac521c9583`
- Combates representados: **133,120**
- Status: `RATA_T1_PLUS70_FOCAL_PASS_READY_TO_SUPPLEMENT_FINAL_GATE`
- Candidate ID: `48a4e5535db32cc5`
- Perfil EXPECTED_STAGE: T1 **78.6328125%** / T0 pareado **78.26171875%** / delta **+0.37109375 pp**
- root_min EXPECTED: **66.552734375%**
- root_spread EXPECTED corregido: **27.099609375 pp**
- procs EXPECTED: **1.0990234375**
- 0 timeouts en perfiles y tails

Todos los guardrails focales pasaron:
- expected band
- todos los perfiles <= T0 pareado +2 pp
- no cliff de dificultad
- root_min
- proc rate
- 0 timeouts

## T1 congelado

| Monstruo | Habilidad T1 | Mecánica congelada | Candidate ID |
|---|---|---|---|
| Rata Qi | Reflejo de Madriguera | EVADE_NEXT +70, 1 carga, CD6 | `48a4e5535db32cc5` |
| Serpiente Qi | Muda del Cauce | EVADE_NEXT +90, 1 carga, CD4 | `7a2540f89ce8ce77` |
| Avispa Jade | Quiebro de Jade | EVADE_NEXT +80, 1 carga, CD4 | `bfe391a7792f7ea2` |
| Mono Píldoras | Salto del Ladrón | EVADE_NEXT +75, 2 cargas, CD6 | `e51305999ebd3045` |
| Lobo Espiritual | Paso de la Cola Vigilante | DEFENSE_UP +10, CD3 | `7edde7aeb0a9e7c1` |

## Semántica común

- trigger por HP <=30% o golpe recibido >=20% del HP máximo;
- `SURVIVAL_ACTION` consume turno del monstruo;
- no balance por raíz;
- player stage es banda esperada, no hard gate;
- política de overreach: `ALLOWED_NATURAL_LIMIT_BY_COMBAT_AND_DECAY`;
- no tocar técnicas ordinarias;
- no inventar T2–T4 stats desde este freeze.

## Resultado

Con el gate final V02 más el suplemento focal aprobado de Rata +70/CD6, los cinco T1 quedan **cerrados y congelados para balance**.

**Siguiente estado permitido:** preparar T2 sobre esta autoridad congelada.  
T2 puede abrirse como laboratorio secuencial; T3–T4 siguen bloqueados hasta sus cierres correspondientes.
