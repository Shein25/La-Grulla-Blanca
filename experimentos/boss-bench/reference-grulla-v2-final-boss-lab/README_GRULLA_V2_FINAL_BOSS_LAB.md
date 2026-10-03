# Grulla Blanca v2 · Final Boss Lab

**Estado:** LAB / PROVISIONAL / NO RUNTIME / NO MERGE  
**Rama:** `experiment/grulla-v2-final-boss-lab-v0.1`  
**Base:** `experiment/combat-stat-contract-v0.1` @ `b218bd60d4983091a9a327164c047bbb5ca8628c`

## Objetivo

Recalibrar a la Grulla Blanca como jefe final del Arco 1 usando el contrato nuevo de combate y suponiendo jugadores veteranos del género, preparados y capaces de explotar equipo, penetración, técnicas, consumibles y lectura de intenciones.

El laboratorio **no** cambia runtime, HTML, `main` ni los cierres previos de IA. Reutiliza el motor `etapa19b_combat_engine.py` y añade una capa exclusiva de simulación para la Grulla.

## Hipótesis que se ponen a prueba

1. La Grulla no debe sobrevivir apilando DEF indefinidamente: combina DEF, mitigación, absorción y evasión.
2. La DEF se evalúa **después** de la penetración real del jugador; Metal debe conservar su identidad antiarmadura.
3. La Grulla obtiene penetración propia para evitar que la DEF plana del jugador anule sus ataques.
4. Tormenta, Campana y Romper Ritmo deben forzar respuesta del jugador, no permitir rotaciones automáticas.
5. Consumibles forman parte del benchmark: beber consume acción, pero la Grulla puede reducir curación o recuperación de Qi.
6. Fase III conserva 50 HP, pero debe durar varias rondas mediante capas defensivas y cerebro, no inflando HP.
7. Fase III introduce **Reflejo** como anticipo de Arco 2. El reflejo no puede reflejar reflejo ni iniciar bucles.

## Baseline LAB

### Fases

| Fase | HP | PREC | EVA | DEF | TEN | CRIT |
|---|---:|---:|---:|---:|---:|---:|
| I · LA GRULLA ESPERA | 150 | 90 | 55 | 12 | 40 | 5% |
| II · LA GRULLA TE RECONOCE | 100 | 95 | 60 | 16 | 45 | 7% |
| III · LA GRULLA DESPLIEGA SUS ALAS | 50 | 100 | 65 | 20 | 50 | 10% |

F3 entra con **36 de absorción**, máximo **12 por impacto**, y reduce al 50% el **bonus** de daño crítico recibido. Al romper la absorción activa `Último Aliento` durante 3 rondas: +10 PREC / +10 EVA y mayor agresividad.

### Ataques

- F1 Golpe: `2d6+3`, 5% pen.
- F1 Tormenta: `2d8+5`, 15% pen, curación recibida ×0.80 durante 1 acción si alcanza HP.
- F2 Golpe: `2d6+4`, 10% pen.
- F2 Tormenta: `2d8+6`, 20% pen, drena 4 Qi, curación ×0.65 durante 2 acciones.
- F3 Picotazo: `2d6+5`, +15 PREC, 10% pen.
- F3 Campana: `2d10+6`, +10 PREC, 25% pen +2 plana, drena 6 Qi, curación y recuperación de Qi ×0.50 durante 2 acciones.
- F3 Romper Ritmo: `3d6+6`, +20 PREC, 35% pen +3 plana.

### Defensas activas

- `Pata Inmóvil`: mitigación del próximo directo visible: 25% / 35% / 45% por fase.
- `Ala Vacía`: +15 / +20 / +25 EVA durante la ventana visible.
- `Cerrar Alas` F2: reserva 18, máximo 8 absorbido por impacto.
- `Recordar` F2: +20 EVA durante la ventana de lectura.
- `Plumas del Espejo Roto` F3: refleja 50% del daño directo real a HP, cap 12.

### Reflejo LAB

Baseline `ABSORPTION_ONLY`:

1. se calcula el daño directo real que recibió la Grulla;
2. `min(cap, daño_real × ratio)` forma el paquete reflejado;
3. el paquete puede ser absorbido por el jugador;
4. no vuelve a pasar por DEF;
5. no puede reflejarse de nuevo ni activar otra represalia.

La sensibilidad permite comparar más adelante contra resolución `NORMAL_DIRECT`.

## Jugadores simulados

- `GREEDY`: baseline de spam.
- `VETERAN_BLIND`: veterano de primera lectura; responde a grandes ataques pero no conoce todos los planes.
- `MASTER_READER`: rompe Silencio/Buscar y usa defensivas ante telegraphs peligrosos.
- `PREPARED_MASTER`: además administra vida, Qi, consumibles, penetración y ventanas defensivas.

Consumibles:

- `none`
- `standard`: 1 vida estable + 1 Qi menor.
- `prepared`: 2 pociones superiores + 2 Tempestad +35 Qi.
- `max_reasonable`: 2 pociones excepcionales + 2 Tempestad excepcional +55 Qi.

Loadouts:

- `guaranteed`
- `veteran_balanced`
- `max_penetration` (especialmente para Metal)

Cada raíz tiene dos builds LIV de 6 puntos. Se incluye explícitamente Metal `pen_shred` para comprobar DEF real → shred → % pen → pen plana.

## Modos

Desde `experimentos/balance_nuevo`:

```bash
python grulla_v2_final_boss_lab.py --mode smoke --runs 200
python grulla_v2_final_boss_lab.py --mode matrix --runs 5000
python grulla_v2_final_boss_lab.py --mode sensitivity --runs 2000
python grulla_v2_final_boss_lab.py --mode trace --root metal --build pen_shred --seed 20260930
```

Los resultados se escriben en `experimentos/balance_nuevo/resultados_grulla_v2/`.

## Matriz principal

Por raíz y build se cruzan:

1. `VETERAN_BLIND + guaranteed + standard`
2. `MASTER_READER + veteran_balanced + standard`
3. `PREPARED_MASTER + veteran_balanced + prepared`
4. `PREPARED_MASTER + max reasonable`; Metal usa `max_penetration`.

## Sensibilidad

One-factor-at-a-time alrededor del baseline:

- DEF: 10/14/18 · 12/16/20 · 14/18/22
- absorción F3: 24 · 36 · 48
- cap por impacto F3: 8 · 12 · 16
- mitigación Pata F3: 35% · 45% · 55%
- reflejo: 35% · 50% · 65%
- anticuración Campana: ×0.65 · ×0.50 · ×0.35

Esto evita confundir qué variable produjo cada cambio antes de hacer una segunda fase factorial.

## Métricas obligatorias

- victoria total y doble KO;
- llegada a F2/F3;
- rondas totales y por fase;
- rondas F3 si se alcanza / si se gana;
- HP/Qi finales;
- hit rate jugador/Grulla;
- control intentos/éxitos;
- daño directo/DOT;
- DEF evitada y absorción de ambos;
- daño reflejado;
- absorción real del escudo F3 y ronda de ruptura;
- pociones de HP/Qi usadas;
- curación/Qi raw vs efectivos;
- aplicaciones de antiheal/anti-Qi;
- Tormentas, Campanas y Romper Ritmo;
- planes Silencio/Buscar activados o rotos;
- degradaciones de telegraph por Control o burst.

## Objetivos provisionales de aceptación

No son CANON; sirven para saber dónde mirar:

- veterano primera lectura: 10–25% victoria;
- Master Reader: 30–45%;
- Prepared Master: 35–55%;
- máximo razonable: no mucho más de 65%;
- F3: 5–9 rondas medias cuando se alcanza;
- ninguna raíz debe quedar hard-lockeada por debajo de 5% sólo por identidad elemental.

Si la Grulla falla estos objetivos no se corrige automáticamente subiendo HP. Primero se identifica **qué capa** falló: DEF efectiva, penetración, mitigación, absorción, memoria, anti-recuperación, daño o política del jugador.

## Guardias

- No tocar `main`.
- No merge.
- No runtime/HTML.
- No reabrir benchmarks cerrados salvo invalidación directa.
- Todo número de este documento es LAB hasta pasar smoke + matrix + sensitivity.
- Seeds y número de iteraciones deben quedar registrados en los CSV.
