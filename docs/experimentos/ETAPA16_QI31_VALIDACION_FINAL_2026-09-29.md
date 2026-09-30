> **NOTA DE SUPERSESIÓN:** ETAPA17B conserva Qi31 como frontera matemática mínima, pero eleva el baseline jugable de LianQi I a Qi37 para dar mayor reserva entre meditaciones. La progresión vigente es 37→43→49→55.

# ETAPA 16 — Validación final de Qi31

Fecha: 2026-09-29  
Rama: experiment/combat-stat-contract-v0.1  
Estado: **CERRADA / QI31 LAB → PROVISIONAL**

## Objetivo

Cerrar el valor de Qi máximo de LianQi I después de estabilizar las cinco
defensivas.

Runner reproducible:

experimentos/balance_nuevo/etapa16_qi31_validacion_final.py

No se modifica runtime/HTML.

---

# 1. Costes relevantes en LianQi I

Ofensivas iniciales:

- Fuego: 6 Qi;
- Metal: 6 Qi;
- Agua: coste nominal7, efectivo6 por raíz Agua;
- Tierra: 6 Qi;
- Viento: 6 Qi.

Defensivas base:

- Fuego: 7 Qi;
- Metal: 7 Qi;
- Agua: nominal7, efectivo6;
- Tierra: 7 Qi;
- Viento: 7 Qi.

Por tanto el problema de Qi máximo es discreto.

---

# 2. Barrido 29–37

| Qi | ofensivas6 | def7 + ofensivas6 | def6 + ofensivas6 |
|---:|---:|---:|---:|
| 29 | 4 | 1+3 | 1+3 |
| 30 | 5 | **1+3** | 1+4 |
| 31 | 5 | **1+4** | 1+4 |
| 32 | 5 | 1+4 | 1+4 |
| 33 | 5 | 1+4 | 1+4 |
| 34 | 5 | 1+4 | 1+4 |
| 35 | 5 | 1+4 | 1+4 |
| 36 | 6 | **1+4** | 1+5 |
| 37 | 6 | **1+5** | 1+5 |

## Qi30

Produce una asimetría artificial:

- ofensiva pura: 5 técnicas;
- Agua: 1 defensiva +4 ofensivas;
- Fuego/Metal/Tierra/Viento: 1 defensiva +3 ofensivas.

Una defensiva7 no sólo sustituye una acción ofensiva: además pierde otra por
aritmética y deja 5 Qi sin utilidad para otra técnica de coste6.

## Qi31

Es la primera frontera limpia:

- ofensiva pura: 5 ofensivas;
- Agua: 1 defensiva +4 ofensivas;
- resto: 1 defensiva +4 ofensivas.

La defensiva sustituye exactamente una acción ofensiva para las cinco raíces.

## Qi32–35

Son una meseta.

No añaden:

- nueva ofensiva;
- nueva técnica total después de defensiva;
- nueva capacidad base de secuencia.

Sólo dejan más residuo.

## Qi36

Abre el siguiente acantilado:

- ofensiva pura sube a 6;
- Agua puede hacer defensiva +5 ofensivas;
- defensivas7 siguen en defensiva +4.

Reaparece la asimetría.

## Qi37

Restaura paridad, pero a costa de elevar LianQi I al presupuesto de seis
ofensivas.

Es un salto mayor de economía y no hace falta para resolver el problema actual.

---

# 3. Evidencia previa ya satisfecha

El documento LAB original exigía antes de promoción cruzar Qi31 con:

- HP/DEF/EVA base del jugador;
- enemigo de referencia;
- stress multi-enemigo;
- todas las defensivas base;
- resto de técnicas LianQi I.

Desde entonces se cerraron:

- enemigo ordinario HP28 / PREC90 / EVA20 / DEF2 / 2d4+1 como marco LAB;
- ofensivas base;
- ataque básico;
- Arrastre;
- Peso;
- cinco defensivas base;
- cinco defensivas completas;
- stress 2 y 3 enemigos;
- screen conjunto final ETAPA15C.

Por tanto el bloqueo experimental ya no existe.

---

# 4. Sensibilidad de combate

Los tests anteriores ya mostraron que el salto 30→31 es real en combate para
Fuego/Metal/Tierra/Viento porque habilita una ofensiva de coste6 adicional
después de abrir con defensiva.

Entre 31 y 35, con la misma política y los mismos costes, la secuencia de
acciones disponible es idéntica.

Por tanto los resultados de combate sólo pueden diferir por ruido Monte Carlo;
no existe una nueva decisión de gasto.

En 36, Agua y ofensiva pura reciben antes que las defensivas7 el siguiente
incremento de acciones.

Esto confirma que Qi31 no es una optimización de una técnica concreta: es una
frontera del sistema de costes.

---

# 5. Decisión

Promover:

~~~text
LianQi I
Qi máximo = 31
PROVISIONAL
~~~

No CANON.

Razón formal:

~~~text
5 × 6 = 30
7 + 4 × 6 = 31
6 + 4 × 6 = 30
~~~

Qi31 es el mínimo que permite simultáneamente:

- cinco ofensivas base;
- defensiva normal7 + cuatro ofensivas;
- defensiva Agua6 + cuatro ofensivas.

---

# 6. Qué NO implica

La promoción de Qi31 no fija:

- Qi de LianQi II;
- Qi de LianQi III;
- Qi de LianQi IV;
- regeneración pasiva de Qi;
- piso global de coste;
- costes futuros de técnicas avanzadas.

Esos valores siguen PENDIENTE.

---

# 7. Guardias

1. no aumentar LianQi I a Qi36 sin rebenchmark: abre una nueva acción antes para
   ofensiva pura/Agua;
2. Qi32–35 no tienen justificación mecánica actual frente a31;
3. si cambia cualquier coste base6/7, reabrir la frontera;
4. ramas de Eficiencia de LianQi II–IV deben validarse con sus Qi máximos futuros;
5. no introducir regeneración pasiva universal para “compensar” residuos.

---

# 8. Estado

~~~text
QI31
LAB → PROVISIONAL

LianQi I Qi máximo
31

runtime/HTML
SIN CAMBIOS
~~~

## Siguiente bloque

Con Qi31 cerrado, el siguiente hueco del baseline LianQi I es revisar cuáles de
los stats desnudos que siguen PENDIENTE deben promoverse formalmente:

- HP base30;
- DEF base1;
- EVA base5;

y sincronizar el perfil enemigo ordinario completo antes de avanzar a perfiles
LianQi II.
