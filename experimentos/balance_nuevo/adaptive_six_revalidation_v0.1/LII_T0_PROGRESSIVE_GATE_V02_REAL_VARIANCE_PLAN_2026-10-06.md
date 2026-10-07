# LII T0 Progressive Gate V02 — Real Individual Variance

Fecha: 2026-10-06
Estado: READY_FOR_COLAB / T0 ONLY

## Finalistas

### Ancla LI
Lobo Espiritual T0 final + variación LI congelada.

### Sapo Ceniza
`S1R_STAGE_CONTINUITY`

Floor:
- HP 55
- PREC 98
- EVA 11
- DEF 0
- TEN 6
- BASIC `1d2+5`
- Nube de Hollín:
  - cadence 3
  - direct `1d2+4`
  - burn `1d2+2 ×3`

Upper envelope:
- HP 61
- PREC 102
- EVA 33
- DEF 3
- TEN 19

Ladders preservadas:
- BASIC: `1d2+5`, `1d3+5`, `1d3+6`, `1d2+7`
- technique direct: `1d2+4`, `1d2+5`, `1d2+8`
- burn permanece fijo en `1d2+2 ×3`

Regla:
no reducir máximos previamente medidos sin nueva evidencia.

### Escarabajo de Hierro
`E0_CURRENT_RETAINED`

Se conserva sin buff:
- floor: HP75 / PREC90 / EVA14 / DEF2 / TEN24 / basic 1d2+3
- upper: HP82 / PREC98 / EVA22 / DEF5 / TEN34
- BASIC ladder: 1d2+3 / 1d2+4 / 1d2+6
- Carga direct ladder: 1d2+8 / 1d4+9
- cadence 3

## Variación real

Cada eje variable recibe un q independiente UNIFORM[0,1].

Stats numéricos:
interpolación floor→upper con redondeo half-up.

Ladders discretas:
el q del eje selecciona una entrada por banda uniforme de la ladder.

El score Mutante se calcula como media de q de ejes variables con el threshold congelado por cantidad de ejes.

Para la decisión de progresión principal:
- se genera `NORMAL_POPULATION` rechazando individuos que crucen threshold Mutante;
- el sistema de sufijos no se activa en este gate;
- Mutantes/sufijos se validan después de congelar T0 LII.

Además:
- `FLOOR` determinista;
- `HIGH_VECTOR` determinista y diagnóstico únicamente.

## Equipo

Jugador siempre LianQi II.

- CARRY_OVER_FLOOR = HIGH_ROLL_STRESS LianQi I exacto.
- EXPECTED_STAGE = EXPECTED_STAGE LianQi II.
- HIGH_ROLL_STRESS = HIGH_ROLL_STRESS LianQi II.

## Matriz

Por especie:
- FLOOR
- NORMAL_POPULATION
- HIGH_VECTOR

Por brazo:
- 3 gear contexts
- 5 roots
- 4 policies
- 256 fights/context

NORMAL_POPULATION:
- 128 individuos no-mutantes
- 2 reps por individuo
- CRN pareado por índice/rep/contexto

FLOOR/HIGH:
- 256 reps/contexto
- CRN pareado.

Total:
**138.240 combates**.

## Métricas

- player win-rate;
- HP pressure;
- rounds;
- monster total/direct/DOT damage;
- hit-rate;
- technique/basic uses;
- root/policy spread;
- normal-population delta vs Lobo normal;
- floor delta vs Lobo floor;
- high-vector delta vs Lobo high.

Rounds NO se interpreta como amenaza monotónica:
- combate más largo puede indicar tanqueo;
- combate más corto con menor player-win puede indicar mayor letalidad.

## Gate humano

Sapo:
- debe mostrar progresión clara sobre Lobo en FLOOR y NORMAL_POPULATION;
- el salto debe seguir siendo moderado;
- Nube de Hollín debe conservar identidad de burn.

Escarabajo:
- se espera que E0 actual ya pase;
- no añadir stats si no son necesarios.

No target universal de win-rate.

## Hard guards

- no T1–T4;
- no T5;
- no Definitivas;
- no suffix abilities en este gate;
- no canonical write;
- no main;
- no merge;
- G04 Tierra correcto;
- exact profile schema;
- deep profile preflight;
- build_monster preflight;
- smoke fight por especie/clase antes del heavy;
- 0 timeout/NaN/Inf.

Si V02 pasa:
- freeze humano T0 LII;
- actualizar envelopes;
- luego recién reabrir T1 de Sapo/Escarabajo.
