# Rata T4 — Mordisco Frenético — Phase B precision / critical review

Fecha: 2026-10-01

## Geometría congelada para esta fase

```text
opening:
INSTANCE_BASIC ×1.0

follow-up:
1 × (2d4 canónico ×0.50)

cooldown:
5
```

Fueron comparadas cuatro combinaciones:

- precisión independiente / crítico independiente;
- follow-up exige hit de apertura / crítico independiente;
- precisión independiente / crítico sólo en apertura;
- follow-up exige hit de apertura / crítico sólo en apertura.

Cinco policies: VETERAN, UNITARGET_FIRST, AOE_FIRST, DEFENSE_OPEN y ROTATION.

## Precision

### INDEPENDENT_PER_HIT

Cada packet es un mordisco físico real y tira su propia precisión.

Ventajas observadas:

- expresa mejor la identidad de ráfaga;
- no depende de una única tirada binaria;
- no introduce bonos ocultos;
- sigue respondiendo a EVA del jugador;
- DEF/absorción continúan por hit.

### FOLLOWUP_REQUIRES_OPENING_HIT

Reduce los packets efectivos por uso aproximadamente de ~2,0 a ~1,77–1,90
según policy.

El daño cae moderadamente, pero no aparece una mejora compensatoria de
estabilidad, loops o interacción con T1–T3.

Añade una regla especial sin resolver un problema observado.

**No preferido.**

## Critical

Permitir crítico independiente en el follow-up mantiene el crit observado por
hit cerca del 5% natural.

Restringir crítico a la apertura reduce el crit agregado aproximadamente a la
mitad, pero:

- el p90 de daño de Mordisco permanece esencialmente igual;
- no cambia cualitativamente win rate;
- no elimina ningún spike problemático observado;
- requiere una excepción específica para T4.

No existe evidencia para prohibir críticos al follow-up.

## Policy observations

VETERAN / UNITARGET:

- incremento moderado y estable respecto de T3;
- sin desplazamiento importante de Reflejo o T3.

DEFENSE_OPEN:

- los packets de Mordisco son fuertemente amortiguados por DEF;
- confirma que no existe bypass.

AOE_FIRST:

- T4 incrementa amenaza sobre una policy ya débil en 1v1;
- no se observan loops ni anomalías de precisión/crítico.

ROTATION:

- T3 casi desaparece como corresponde;
- T4 sigue manifestándose porque es una habilidad T4 instintiva y no depende
  del patrón T2.

Esto es intencional: romper el patrón contrarresta T2/T3, pero no elimina una
habilidad física aprendida por una población que ya alcanzó T4.

## Selección provisional Phase B

```text
precision_rule = INDEPENDENT_PER_HIT
critical_rule  = INDEPENDENT_PER_HIT
```

Sin:

- precision bonus;
- precision penalty;
- crit bonus;
- shared crit;
- follow-up gate.

## Siguiente fase

Phase C mantiene todo lo anterior congelado y calibra sólo cooldown.

Candidatos iniciales: CD3 / CD5 / CD7.

T4 sigue experimental.
