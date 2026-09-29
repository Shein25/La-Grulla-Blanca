# ETAPA 9A — Estratos Compactos · screen estructural 1v1

Fecha: 2026-09-29
Rama: experiment/combat-stat-contract-v0.1
Estado: **CERRADA COMO SCREEN / CANDIDATO LAB SELECCIONADO**

## Pregunta única

¿Cómo puede mejorar **Estratos Compactos (Tramo II)** la ruta de fortificación
sin convertir Piel + Corteza, DEF total 5 → 6 → 6, en una escalera permanente
hacia DEF7 o más?

Además, Estratos debe funcionar aunque el jugador NO haya elegido Corteza en
Tramo I.

## Variante descartada conceptualmente

No se continúa con +1 DEF permanente a 2+ Arraigos porque una unidad plana
permanente se aplicaría a cada impacto de cada enemigo y reabriría el problema
multiimpacto que motivó DEF_CAP2.

## Candidato LAB: ESTRATO_REACTIVO_2

Regla propuesta:

~~~text
Piel activa
+
Arraigo aumenta y alcanza 2 o 3
→ gana/refresca 1 ESTRATO COMPACTO

máximo almacenado = 1

siguiente impacto directo conectado
→ +2 DEF sólo para ese impacto
→ consume ESTRATO
~~~

Reglas:

- una evasión no consume Estrato;
- si el trigger fuerte hace saltar Arraigo 1→3, genera un solo Estrato;
- si el ascenso es gradual 1→2→3, puede proteger hasta dos impactos en toda
  la activación;
- no aumenta la DEF permanente;
- no aumenta máximo de Arraigo;
- no modifica Tenacidad;
- no añade duración;
- funciona con o sin Corteza Endurecida.

## Por qué esta estructura

El poder está limitado por transiciones de Arraigo, no por número de enemigos.

~~~text
más atacantes
≠ más Estratos infinitos
~~~

La rama sigue siendo fortificación, pero mediante ventanas discretas.

## Screen inicial

50.000 combates por celda, semilla 20260929.

### Perfil común

Enemigo: PREC90, daño 2d4+1.

| Configuración | Sin Estratos | Con Estratos | Delta win | Delta HP |
|---|---:|---:|---:|---:|
| Piel base | 95.60% | 96.10% | +0.50 pp | +2.14 pp |
| Piel + Corteza | 96.37% | 96.31% | ~0.00 pp | +0.08 pp |

Lectura:

- Estratos funciona por sí solo;
- sobre Corteza el enemigo común ya es tan débil frente a la fortificación que
  aparece retorno decreciente;
- no hay una escalada gratuita de poder por apilar ambas ramas.

### Perfil pesado de sensibilidad

Este perfil YA EXISTE como stress LAB; no representa todavía un enemigo
LianQi III canónico.

Enemigo: PREC90, daño 1d6+3.

| Configuración | Sin Estratos | Con Estratos | Delta win | Delta HP |
|---|---:|---:|---:|---:|
| Piel base | 92.99% | 93.92% | +0.93 pp | +3.10 pp |
| Piel + Corteza | 94.31% | 94.55% | +0.25 pp | +1.20 pp |

El patrón es relevante:

> Estratos gana utilidad cuando el impacto individual es más peligroso, sin
> necesitar aumentar la DEF permanente.

Eso es deseable para un nodo de Tramo II que eventualmente deberá convivir con
enemigos más fuertes de LianQi III.

## Relación con Corteza

No se declara todavía una bonificación numérica especial por tener Corteza.

La especialización ya existe de forma natural:

~~~text
Corteza
→ fortificación permanente moderada 5→6→6

Estratos
→ ventanas reactivas de +2 DEF

Corteza + Estratos
→ base fortificada + protección puntual
~~~

Forzar ahora un bono mayor al Estrato sólo para crear una sinergia explícita
sería prematuro y puede volver a sobreescalar.

## Limitación actual

Todavía NO existen perfiles enemigos numéricos autoritativos de LianQi III.

Por eso este test:

- selecciona arquitectura;
- demuestra que no hace falta DEF7 permanente;
- NO cierra todavía el balance final de Estratos para LianQi III.

## Resultado de Etapa 9A

**ESTRATO_REACTIVO_2 pasa a candidato principal LAB para Estratos Compactos.**

Todavía:

- NO PROVISIONAL;
- NO CANON;
- NO runtime.

## Próxima etapa

**ETAPA 9B — ESTRATO_REACTIVO_2 contra 2 enemigos.**

Pregunta única:

¿el límite por transición de Arraigo mantiene controlado el escalado cuando
aumenta la cantidad de impactos?

No abrir todavía Cuerpo de Roca.
