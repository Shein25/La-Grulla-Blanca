# LAB — Golpe simple vs técnicas · LianQi I NAKED

Fecha: 2026-09-29  
Rama: `experiment/combat-stat-contract-v0.1`  
Estado: **LAB / NO CANON**

## Objetivo

Crear una primera base numérica para el ataque básico de coste 0 Qi antes de
cerrar las cinco técnicas iniciales.

Este ensayo NO fija:
- daño básico definitivo;
- DEF/Evasión de enemigos reales;
- distribuciones definitivas de técnicas;
- HP, Qi máximo, TTK, daño enemigo ni equipo.

No se usó ninguna cifra legacy.

## Aislamiento del ensayo

Se prueba únicamente el paquete directo:

`tirada -> modificadores generales -> crítico -> DEF/penetración -> ROUND_HALF_UP`

El personaje incluye sólo:
- LianQi I;
- raíz principal;
- ataque básico o técnica base.

Se excluyen:
- equipo;
- injerto;
- Concordancias;
- Tramos;
- consumibles;
- HP/TTK;
- economía total de Qi;
- Control/Peso como valor adicional de utilidad.

Por tanto, el premium de técnica de este documento es **sólo de daño directo**.
Agua y Tierra, por ejemplo, todavía no reciben aquí el valor adicional de
Arrastre/Peso.

## Candidatos LAB del ataque básico

| ID | Dados | Media | Función |
|---|---:|---:|---|
| B5_NARROW | 2d4 | 5.0 | control bajo |
| B6_NARROW | 2d4+1 | 6.0 | candidato medio |
| B6_5_STABLE | 1d4+4 | 6.5 | media 6.5 con piso alto |
| B6_5_MEDIUM | 1d6+3 | 6.5 | media 6.5 con dispersión media |
| B6_5_BELL | 3d4-1 | 6.5 | misma media con cola baja posible |
| B7_NARROW | 2d4+2 | 7.0 | control alto |

## Targets centrales LAB

Se eligieron dos puntos de sensibilidad deliberadamente abstractos:

- `E20_D2`: Evasión 20 / DEF 2.
- `E20_D3`: Evasión 20 / DEF 3.

No representan monstruos concretos ni una propuesta de estadísticas para
LianQi I. Sólo sirven para observar la transición producida por la DEF plana.

## Monte Carlo inicial

Validación: 100.000 acciones por combinación, semillas reproducibles.

Para comparar el fallback con Qi agotado se usa:

`Technique Premium = daño esperado técnica / daño esperado ataque básico`

Técnicas: candidato `narrow` actual, conservando sus presupuestos
PROVISIONAL 10/9/8/9/8.

### Resumen por candidato

| Target | Ataque | Daño básico medio observado* | Premium medio técnica | Rango del premium entre raíces |
|---|---|---:|---:|---:|
| E20_D2 | B5 | 2.66 | 2.25x | 1.98–2.45x |
| E20_D2 | B6 | 3.53 | 1.69x | 1.49–1.86x |
| E20_D2 | B6.5 estable/medio | ~3.95 | ~1.51x | ~1.33–1.69x |
| E20_D2 | B7 | 4.38 | 1.36x | 1.20–1.51x |
| E20_D3 | B5 | 1.90 | 2.81x | 2.37–3.29x |
| E20_D3 | B6 | 2.72 | 1.96x | 1.65–2.29x |
| E20_D3 | B6.5 estable/medio | ~3.14 | ~1.69x | ~1.42–1.96x |
| E20_D3 | B7 | 3.57 | 1.49x | 1.24–1.72x |

\* Promedio descriptivo entre las cinco raíces; no es una estadística de
personaje CANON.

## Hallazgos

### 1. Media 5 queda demasiado abajo como fallback

En los dos targets centrales, las técnicas entregan aproximadamente
2.0–3.3 veces el daño directo del ataque B5 según raíz y DEF.

No se descarta del universo de diseño, pero deja de ser el foco del siguiente
barrido porque no cumple bien el objetivo de que quedarse sin Qi siga
permitiendo combatir de forma funcional.

### 2. La zona útil aparece aproximadamente entre 6 y 6.5

B6 mantiene una ventaja clara para gastar Qi:

- E20_D2: premium aproximado 1.49–1.86x.
- E20_D3: premium aproximado 1.65–2.29x.

B6.5 reduce la separación sin borrar la ventaja:

- E20_D2: aproximadamente 1.33–1.69x.
- E20_D3: aproximadamente 1.42–1.96x.

Esto convierte 6–6.5 en la primera **zona de interés LAB**, no en una cifra
cerrada.

### 3. Media 7 funciona como control alto

B7 deja a algunas técnicas relativamente cerca en daño bruto, especialmente
Agua, antes de valorar sus efectos secundarios.

No queda descartado, porque una técnica también compra Control/Peso,
precisión, penetración u otras propiedades. Se conserva como límite alto para
comprobar después si el coste de Qi sigue sintiéndose valioso.

### 4. La distribución importa tanto como la media

Con media 6.5:

- `1d4+4` y `1d6+3` no produjeron anulaciones por DEF en impactos
  conectados contra DEF 2 ni DEF 3; los 0 observados corresponden a fallos por
  Evasión.
- `3d4-1` puede alcanzar una tirada suficientemente baja para que DEF 2/3
  cree paquetes de 0.
- una distribución muy ancha aumentaría todavía más ese problema.

Esto sugiere que, si el ataque básico debe ser el recurso fiable cuando no
queda Qi, conviene estudiar explícitamente un **piso de tirada razonable** en
vez de balancearlo sólo por media.

### 5. Las raíces ya diferencian el golpe simple

Sin añadir reglas nuevas:

- Fuego mejora daño directo y crítico.
- Metal mejora precisión y penetración general.
- Viento mejora daño crítico.
- Agua y Tierra no reciben una bonificación ofensiva directa al golpe simple.

Por ello el ataque básico no tendrá exactamente el mismo rendimiento entre
raíces. Esto deberá evaluarse más adelante junto con la economía de Qi de Agua
y la supervivencia de Tierra; no debe corregirse artificialmente en PHASE A.

## Próxima ronda recomendada

Mantener como candidatos principales:

- `B6_NARROW = 2d4+1`;
- `B6_5_STABLE = 1d4+4`;
- `B6_5_MEDIUM = 1d6+3`;

Mantener `B7_NARROW` como control superior.

Luego barrerlos contra la parrilla completa:

- Evasión: 0 / 10 / 20 / 30 / 40.
- DEF: 0 / 1 / 2 / 3 / 4 / 5 / 6.

La finalidad no es escoger un ganador por promedio, sino localizar:

1. dónde el ataque básico deja de ser un fallback funcional;
2. dónde las técnicas dejan de justificar Qi;
3. cuándo DEF comienza a producir demasiados paquetes de 0;
4. cómo cambia la separación entre raíces;
5. qué distribución mantiene mejor la identidad de “recurso fiable sin Qi”.

## Cambios de framework

`sim_core.py` ahora reporta adicionalmente:

- `zero_damage_rate_per_action`;
- `zero_damage_rate_on_hit`.

Esto permite separar un 0 producido por fallo de Precisión/Evasión de un
impacto conectado completamente absorbido por DEF.

Runner reproducible:

`experimentos/balance_nuevo/basic_attack_phase_a_lab.py`

El runner no modifica ninguna configuración CANON/PROVISIONAL.


---

## Barrido completo PHASE A — 200.000 acciones por combinación

Se ejecutó una segunda validación sobre la parrilla completa:

- Evasión: 0 / 10 / 20 / 30 / 40.
- DEF: 0 / 1 / 2 / 3 / 4 / 5 / 6.
- raíces: Fuego / Metal / Agua / Tierra / Viento.
- candidatos básicos principales: B6, B6.5 estable, B6.5 medio y B7.
- técnica de comparación: variante `narrow` de cada técnica inicial.

Se mantuvieron todas las propiedades CANON de raíz y las propiedades
PROVISIONAL de las técnicas. El equipo permaneció totalmente excluido.

### Premium de técnica y anulaciones por DEF

Los porcentajes de cero de la tabla siguiente son **impactos que sí acertaron
pero cuya DEF dejó el paquete final en 0**; no incluyen fallos por Evasión.

| DEF | B6 premium medio | B6 cero/hit | B6.5 estable premium | B6.5 estable cero/hit | B6.5 medio premium | B6.5 medio cero/hit | B7 premium | B7 cero/hit |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 0 | 1.48x | 0% | 1.36x | 0% | 1.37x | 0% | 1.27x | 0% |
| 1 | 1.57x | 0% | 1.42x | 0% | 1.43x | 0% | 1.31x | 0% |
| 2 | 1.69x | 0% | 1.50x | 0% | 1.51x | 0% | 1.36x | 0% |
| 3 | 1.96x | ~5.9% | 1.68x | 0% | 1.69x | 0% | 1.49x | 0% |
| 4 | 2.31x | ~17.6% | 1.92x | 0% | 1.93x | ~15.7% | 1.63x | ~5.9% |
| 5 | 2.62x | ~28.7% | 2.18x | ~14.2% | 2.07x | ~25.2% | 1.71x | ~13.0% |
| 6 | 3.48x | ~50.2% | 2.91x | ~37.8% | 2.45x | ~41.3% | 1.98x | ~28.5% |

Los premiums son promedios descriptivos del barrido de raíces/Evasión; no
representan una criatura concreta.

### Lectura del barrido

1. **B6 empieza a romperse en DEF 3.**
   Ya aparecen impactos conectados anulados. En DEF 4 el fenómeno deja de ser
   excepcional.

2. **B6.5_STABLE = 1d4+4 posee una frontera muy limpia.**
   Mantiene 0% de impactos conectados anulados hasta DEF 4 inclusive.
   Recién en DEF 5 la armadura empieza a vencer realmente al ataque básico.

3. **B6.5_MEDIUM = 1d6+3 es más dramático, pero menos fiable.**
   Funciona igual de bien hasta DEF 3, pero en DEF 4 ya puede tirar 4 y quedar
   completamente anulado. Su cola superior, a cambio, sobrevive algo mejor
   cuando la DEF alcanza 5–6.

4. **B7 es claramente el control alto.**
   Tolera mejor DEF elevada, pero contra DEF baja deja demasiado poco espacio
   de daño bruto para justificar ciertas técnicas antes de valorar sus
   propiedades secundarias.

5. **DEF 4 es el punto de discriminación más útil del laboratorio.**
   Permite separar con claridad la identidad de un fallback fiable
   (`1d4+4`) de uno más variable (`1d6+3`) sin introducir todavía una
   criatura real.

### Hipótesis de diseño que emerge

Si el ataque básico debe representar una acción marcial fiable cuando falta
Qi, mientras que una defensa realmente alta debe exigir técnicas, penetración
o recursos especiales, `B6_5_STABLE = 1d4+4` es actualmente el candidato LAB
más informativo:

- media 6.5;
- rango 5–8;
- coste 0 Qi;
- no activa propiedades elementales por sí mismo;
- conserva modificadores generales de la raíz;
- ningún impacto acertado queda a 0 hasta DEF 4 en este barrido;
- DEF 5+ empieza a actuar como una barrera real al daño marcial común.

Esto **NO lo convierte en CANON**. La interpretación depende de dónde
terminemos ubicando la DEF ordinaria y la DEF de enemigos especialmente
acorazados de LianQi I.

`1d6+3` se conserva como alternativa si decidimos que el golpe simple debe
tener más oscilación y alguna posibilidad de superar mejor defensas altas.

## Regla para las etapas II–IV

Este resultado no anticipa estadísticas de equipo.

El orden se mantiene:

1. cerrar LianQi I NAKED;
2. cerrar economía de Qi y combate completo de LianQi I;
3. recién después diseñar el equipo de LianQi II–IV;
4. reejecutar por etapa NAKED / MINIMAL / EXPECTED / HIGH_ROLL.

No se reducirá artificialmente el poder base de LianQi I para reservar
"espacio" a estadísticas futuras. Las capas de equipo y Tramos deberán
demostrar su propio presupuesto marginal cuando sean incorporadas.
