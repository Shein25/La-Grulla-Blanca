# CODEX — ARMADURA DE PLATA F7 MICROLAB V01

Repositorio: `https://github.com/Shein25/La-Grulla-Blanca`  
Rama autorizada: `experiment/techniques-kaggle-heavy-v0.4`

## Guardias
- NO tocar `main`.
- NO merge.
- NO modificar runtime productivo.
- NO rediseñar fuera de F0/F1/F5/F7.
- NO Sobol/TPE/NSGA-II.
- NO búsqueda paramétrica.
- NO declarar CANON.
- NO cambiar seeds, CRN, policies, loadouts, monstruos, fórmulas ni contratos.
- NO tocar `adapt_tenacity_by_count/1 = 5`.
- Si falta autoridad/artefacto: ABORTAR, informar ruta/commit faltante y no inventar.

## Diseños exactos

F0 BASELINE:
- qi_cost = 7
- base_defense_per_plate = 3
- RESISTANCE_FIRST_DEF_INCREMENT_1 = 1
- RESISTANCE_LATER_DEF_INCREMENT = 2

F1 HEAVY:
- qi_cost = 7
- base_defense_per_plate = 3
- RESISTANCE_FIRST_DEF_INCREMENT_1 = 1
- RESISTANCE_LATER_DEF_INCREMENT = 1

Referencia:
- regret HIGH ~0.0711367985
- 0 pares universalmente dominados
- 13 pérdidas materiales profundas
- peor celda ~-0.101824

F5 HEAVY:
- qi_cost = 7
- base_defense_per_plate = 4
- RESISTANCE_FIRST_DEF_INCREMENT_1 = 1
- RESISTANCE_LATER_DEF_INCREMENT = 2

Referencia:
- regret HIGH ~0.1252726140
- 4 pares universalmente dominados
- 125 ganancias materiales profundas
- 0 pérdidas materiales profundas

F7 HUMANO NUEVO:
- qi_cost = 6
- base_defense_per_plate = 3
- RESISTANCE_FIRST_DEF_INCREMENT_1 = 1
- RESISTANCE_LATER_DEF_INCREMENT = 1

F7 es hipótesis humana NO aprobada.

## Paso 0 — Preflight

Antes de ejecutar:
- identifica HEAD actual;
- identifica runner exacto usado por Metal HEAVY;
- identifica authority fingerprint/config;
- verifica que las 40 rutas y contextos coinciden con campaña HEAVY;
- verifica seeds/CRN;
- registra hashes de inputs.

Si no puedes demostrar compatibilidad, ABORTA.

## Paso 1 — Reproducción HIGH R64

Ejecuta F0/F1/F5/F7 sobre:
- mismas 40 rutas legales;
- mismos contextos;
- mismas policies;
- mismos loadouts;
- mismos monstruos;
- mismas seeds;
- mismo CRN;
- R64.

Primero compara F0/F1/F5 contra los agregados HEAVY conocidos.

### ABORT GUARD

Si F0/F1/F5 no reproducen dentro de tolerancia numérica razonable:
- marca `CONTROL_REPRODUCTION_FAIL`;
- no interpretes F7;
- conserva evidencia;
- explica discrepancia;
- termina.

No ajustes parámetros para forzar reproducción.

## Paso 2 — Métricas HIGH

Para cada diseño:
- WORST_SIBLING_REGRET
- CONTEXT_POLARIZATION
- NORMALIZED_PARAMETER_DISTANCE_FROM_CURRENT_DESIGN
- pares UNIVERSALLY_DOMINATED exactos
- NON_DOMINATED
- NICHE
- STATISTICALLY_UNCLEAR
- utility delta vs F0
- hp_final
- qi_spent
- forced_basic
- damage_per_Qi
- damage_per_action
- player_damage_direct
- player_absorbed
- player_def_prevented
- rounds
- defense_procs

No usar una métrica auxiliar aislada como ganador.

## Paso 3 — Deep R256

Sólo si controles reproducen y F7 no es claramente inválido.

Rutas exactas:
`base, 000, 111, 222, 012, 120, 201`

R256 con la misma semántica incremental/CRN que HEAVY.

Reporta:
- media delta vs F0
- low/high con semántica original; no inventar nivel de confianza
- material gains: low > +0.02
- material losses: high < -0.02
- peor celda
- mejor celda
- stage/policy/loadout/targets/ruta
- máximo ancho
- polarización deep

## Paso 4 — R1000 condicional

Sólo si F7 sigue siendo razonable.

No repetir los cuatro diseños si no hace falta.
Usar F7 y controles mínimos necesarios.

Mantener réplicas incrementales:
- R64 = 0..63
- R256 añade 64..255
- R1000 añade 256..999

No tratarlos como experimentos independientes.

## Criterios de revisión humana

No son winner automático.

Buscamos idealmente:
- 0 pares universalmente dominados;
- regret cercano a F1 (~0.071) y claramente menor que baseline (~0.126);
- menos pérdidas materiales que las 13 de F1;
- peor celda bastante menos severa que ~-0.10;
- sin buff universal excesivo;
- preservar identidad Metal;
- no convertir Armadura en superior sistemática a Cuerpo-Horno.

Si F7 aumenta potencia en casi todos los contextos, señalar riesgo de overtuning aunque mejore la media.

## Entregable

Crear:
`ARMADURA_PLATA_F7_MICROLAB_REVIEW_V01.zip`

Contenido mínimo:
- `AUDITORIA_ARMADURA_F7.md`
- `PROVENANCE.json`
- `CONFIG_F0_F1_F5_F7.json`
- `CONTROL_REPRODUCTION.csv`
- `HIGH_METRICS.csv`
- `DOMINANCIAS.csv`
- `DEEP_R256.csv` si aplica
- `DEEP_R1000.csv` si aplica
- `ANOMALIAS_Y_LIMITACIONES.md`
- `HUMAN_REVIEW_SUMMARY.json`
- `MANIFEST_SHA256.txt`

Informe final:
1. HEAD y authority;
2. hashes inputs;
3. reproducción F0/F1/F5;
4. combates representados/ejecutados;
5. métricas HIGH;
6. pares universales exactos;
7. resultados deep;
8. gains/losses materiales;
9. peor/mejor celda;
10. anomalías;
11. SHA-256 y tamaño ZIP.

NO declarar ganador ni CANON.
