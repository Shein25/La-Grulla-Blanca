# Review V04 — LII T0 Micro Gate target ~70%

Fecha: 2026-10-07
Estado: MECHANICALLY_PASS / ESCARABAJO_NEAR_CLOSED / SAPO_REQUIRES_ONE_AXIS_MICROSEARCH

## Integridad

- 176.640 combates.
- manifest 8/8 válido.
- 0 timeouts.
- issue reportado:
  - MUTANT_REJECTION_HIGH:LOBO_FROZEN_NORMAL
- el issue corresponde únicamente al control Lobo:
  - 4 rechazos / 132 intentos = 3,03%;
  - no invalida Sapo/Escarabajo;
  - es sampling noise alrededor de la barrera de auditoría 3%.

## Target humano

HIGH_ROLL_STRESS LII:
- banda: 67–73% player-win;
- centro: ~70%.

No es target universal del juego.

## Escarabajo

HRS:
- E0 floor fijo: 69,9805%
- E1 Carga 1d2+9 con q>=.975: 69,7461%
- E2 Carga 1d2+9 con q>=.95: 69,3945%
- E3 Carga 1d2+9 con q>=.90: 68,9063%

Todos pasan la banda.

Lectura:
- el floor está prácticamente en 70%;
- no añadir stat variance ordinaria;
- si se desea variación de habilidad, E1 o E2 son seguros;
- E1 es el más cercano al centro;
- E2 hace la variación algo más visible y sigue dentro de banda.

## Sapo

HRS:
- S0 floor fijo: 73,3398%
- S4 micro stats only: 66,1523%
- S1 micro + skill q>=.95: 65,9766%
- S2 micro + skill q>=.90: 65,7422%
- S3 micro + skill q>=.85: 65,5664%

Conclusión:
- floor apenas supera la banda por +0,34 pp;
- mover simultáneamente HP/PRE/EVA/DEF/TEN sobrecorrige en ~7,2 pp;
- la variación de Nube 1d2+4→1d2+5 tiene efecto pequeño frente al bloque completo de stats;
- no volver a usar el micro-envelope de cinco stats combinado.

## Próximo paso

V05 focal sólo Sapo:
- conservar floor;
- probar variación aislada por eje;
- probar pares mínimos de ejes;
- combinar finalistas con variación leve de Nube;
- screen principal sólo HRS;
- confirmar finalistas en CARRY_OVER / EXPECTED / HRS.

Objetivo:
encontrar la mínima variación ordinaria que deje al Sapo ~70% HRS sin perder espacio para T1.
