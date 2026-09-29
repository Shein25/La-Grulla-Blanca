# Checkpoint — Benchmark LianQi I NAKED bajo sistema nuevo

Fecha: 2026-09-29
Rama: experiment/combat-stat-contract-v0.1
HEAD auditado de entrada: ed7728f759e20743adfedabf0c3b6de00bb8825c
Estado: PRE-BENCHMARK / SIN CIFRAS LEGACY

## Guardia

- No tocar main.
- No merge.
- No runtime/HTML.
- No convertir ATQ, DEF, HP, Qi, Evasión, probabilidades, daño de monstruos, objetos ni perfiles de ver74.
- Todo número del benchmark debe ser CANON, PROVISIONAL, LAB o PENDIENTE.
- PENDIENTE bloquea la fase que lo necesita.

## Estado real al retomar

La comparación entre ed7728f7 y experiment/combat-stat-contract-v0.1 dio identical.
El HEAD real de entrada fue exactamente ed7728f759e20743adfedabf0c3b6de00bb8825c.

El handoff original nació desde 4da38c1b, pero la rama avanzó después con el
laboratorio nuevo, PASS0, progresión/equipo y la actualización del propio handoff.

## Cerrado de verdad

CANON global:

- Precisión normal: 100.
- Impacto: clamp(Precisión efectiva - Evasión, 5, 100).
- Crítico base: 5%.
- Daño crítico base: x1.50.
- DEF: reducción plana de daño directo.
- Orden: DEF real -> shred -> penetración % -> penetración plana -> DEF efectiva.
- Directo: DEF -> Absorción -> Vida.
- DOT ignora DEF pero no Absorción.
- Redondeo: mantener decimal hasta post-DEF y aplicar ROUND_HALF_UP una sola vez.

Raíces principales CANON:

- Fuego: +10% daño directo general y +5 pp crítico.
- Metal: +10 pp Penetración % general y +5 Precisión.
- Agua: -10% coste de Qi de técnicas y +5 Control.
- Tierra: +10% HP máximo y +5 Tenacidad.
- Viento: +10 Evasión y +5 pp Daño Crítico.

El injerto tiene contrato propio, pero queda fuera de NAKED.

Cinco técnicas iniciales ofensivas, cifras PROVISIONAL:

- Palma Ardiente: media nominal 10, coste 6.
- Destello de Plata: media 9, coste 6, +10 pp Penetración % propia.
- Latigazo de Marea: media 8, coste 7, Arrastre; base_control pendiente.
- Golpe de Montaña: media 9, coste 6, Peso.
- Lanza que Parte Nubes: media 8, coste 6, +5 Precisión y +5 pp crítico.

Las medias nominales no son daño fijo.

El paquete de Arco 1 está actualmente en 15/15 técnicas diseñadas, incluido
Viento 3/3. El archivo de hooks conserva un rótulo antiguo que dice 12, pero su
contenido y su conclusión auditan 15/15 y 60 relaciones. Es editorial, no bloqueante.

## Pendiente para LianQi I NAKED

Actor base antes de raíz:

- HP máximo.
- Qi máximo.
- Evasión base no-root.
- DEF base desnuda.
- Control base no-root.
- Tenacidad base no-root.

No se convierten en cero por conveniencia: el notebook serio ya los deja sin definir.

Daño variable:

- elegir una distribución nueva para cada una de las cinco técnicas iniciales.
- los candidatos narrow/wide existentes son LAB, no dados canónicos.

Primer enemigo de referencia LianQi I nuevo:

- HP.
- Precisión.
- Evasión.
- DEF.
- Tenacidad.
- distribución de daño por acción.
- Qi/Control sólo si ese perfil realmente los usa.

Agua:

- base_control de Arrastre.

Qi:

- piso global de coste.

Duelo completo:

- orden/alternancia de acciones.
- política de acción del jugador.
- política de acción del enemigo.
- alcance de técnicas permitido en cada subtest.

## Alcance del primer gate

El benchmark inaugural se limita a las cinco técnicas iniciales ofensivas, una
por elemento. No se inventa que las 15 técnicas deban estar todas disponibles
desde el minuto inicial del prólogo.

Orden de trabajo:

A. cinco iniciales ofensivas.
B. presupuesto de Qi.
C. presión enemiga / duelo.
D. defensivas base.
E. resto de técnicas base que realmente estén disponibles en LianQi I.

## Hallazgo de framework

sim_core.py entregaba damage_after_def como decimal.

El contrato nuevo exige:

post-DEF decimal -> redondeo único -> paquete discreto -> Absorción/Vida.

Se corrigió el laboratorio para conservar dos campos:

- damage_after_def_decimal: diagnóstico.
- damage_after_def: paquete entero tras ROUND_HALF_UP.

No se tocó runtime.

## Nuevas compuertas

Archivos:

- experimentos/balance_nuevo/config_lianqi1_naked.py
- experimentos/balance_nuevo/lianqi1_naked_benchmark.py

PHASE_A_DIRECT_PACKET requiere:

- enemy.evasion.
- enemy.defense.
- una distribución de daño para cada técnica inicial.

PHASE_B_QI_BUDGET requiere:

- player.qi_max.
- qi_cost_floor.

PHASE_C_FULL_DUEL requiere además:

- player.hp_max/evasion/defense/control/tenacity.
- enemy.hp_max/precision/evasion/defense/tenacity/damage_model.
- arrastre.base_control.
- combat_policy.turn_order.
- combat_policy.enemy_action.
- combat_policy.player_action.
- engine.full_duel_loop.

## Resultado de este checkpoint

Todavía no existe un benchmark numérico LianQi I válido.

Eso es deliberado: completar huecos con defaults silenciosos recrearía la
contaminación que se está eliminando.

El armazón ya permite saber exactamente qué falta y se niega a correr una fase
si el parámetro necesario continúa PENDIENTE.

## Próximo paso exacto

Cerrar PHASE_A:

1. seleccionar una distribución nueva por cada técnica, manteniendo o revisando
   explícitamente su media provisional;
2. fijar desde cero Evasión + DEF del primer perfil de referencia LianQi I;
3. ejecutar Monte Carlo reproducible;
4. revisar hit rate, crítico, media/mediana/p10/p90 y efecto de DEF/Penetración;
5. después pasar a HP/Qi y duelo completo.

Ningún resultado LAB se vuelve CANON por ser ejecutado.


---

## Actualización — PHASE A cerrada provisionalmente

Resultado:

**PHASE_A_DIRECT_PACKET = PASS PROVISIONAL**

Baseline actual:

- enemigo de referencia: Evasión 20 / DEF 2;
- ataque básico: 1d4+4;
- técnicas iniciales: distribuciones narrow;
- 300.000 acciones por combinación en Monte Carlo;
- cross-check determinístico por enumeración exacta;
- desviación máxima Monte Carlo vs exacto <0.25%;
- 0% de impactos conectados anulados por DEF en el baseline.

Documento:

`docs/experimentos/TEST_LIANQI_I_NAKED_PHASE_A_2026-09-29.md`

PHASE A no se eleva todavía a CANON. El objetivo es congelar un baseline sano
para avanzar a PHASE B sin reabrir continuamente el paquete directo.

Siguiente bloque activo:

**PHASE_B_QI_BUDGET**
