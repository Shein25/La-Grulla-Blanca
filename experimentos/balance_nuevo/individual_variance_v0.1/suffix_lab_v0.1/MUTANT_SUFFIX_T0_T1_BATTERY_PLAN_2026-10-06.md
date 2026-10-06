# Mutant Suffix T0/T1 Battery v0.1

Fecha: 2026-10-06
Estado: LAB_ONLY_NOT_RATIFIED

## Contexto recuperado

Los handoffs conservan sufijos Mutantes propuestos como Acorazado/Fugaz/etc. y ordenan no ratificarlos hasta disponer de pruebas.

Direcciones históricas recuperadas:
- Acorazado: predominio HP/DEF; propuesta de absorción al caer bajo 50% HP.
- Fugaz: predominio EVA; propuesta de EVA durante la siguiente acción del jugador después de recibir un crítico.
- Acechante: predominio PREC; no quedó habilidad histórica definida.
- Indómito: predominio TEN; propuesta de resistencia adicional frente al primer control.
- Voraz: predominio ofensivo; propuesta de potenciar el siguiente básico tras bajar al jugador de cierto HP.
- Multi-eje: nombres Excepcional/Ascendido pendientes; acumulación/exclusividad nunca ratificada.

Los sufijos se derivan de los mismos q_axis; no usan RNG adicional.

## Guardia

Nada de este laboratorio es CANON. No modificar T0 ni T1 congelados, no tocar main, no merge. La dificultad extrema de un Mutante no es un fallo por sí sola.

## Fase A — clasificación

500.000 spawns por especie. Se comparan 9 clasificadores:
- min group score: 0.75 / 0.80 / 0.85
- multi margin: 0 / 0.05 / 0.10

Objetivo: medir incidencia de Acorazado/Fugaz/Acechante/Indómito/Voraz, MULTI y MUTANT_UNMARKED sin alterar la incidencia Mutante global.

## Fase B — habilidades T0/T1

Para cada sufijo disponible naturalmente en cada especie:
- se muestrean Mutantes cuyo grupo dominante coincide con el sufijo;
- se reutiliza el mismo individuo y la misma seed para NONE y 3 intensidades;
- 4 perfiles de jugador;
- 5 raíces;
- 2 policies;
- T0 y T1 congelado;
- R64.

Parámetros LAB:
- Acorazado: absorción 10/15/20% HPmax, primer cruce <=50% HP.
- Fugaz: +15/+25/+35 EVA para la siguiente acción del jugador tras recibir crítico.
- Acechante: NUEVA HIPÓTESIS LAB porque no existía habilidad histórica: después de fallar un ataque, siguiente ataque +10/+20/+30 PREC.
- Indómito: +15/+25/+35 TEN sólo durante el primer intento de Control.
- Voraz: bundles 30%HP/x1.25, 40%HP/x1.50, 50%HP/x1.75 para el siguiente BASIC después de cruzar el umbral.

## Fase C — multi-sufijo / upper stress

Sobre el upper envelope:
- todos los pares de sufijos disponibles por especie;
- ALL_SUPPORTED;
- intensidad media;
- EXPECTED_STAGE y HIGH_ROLL_STRESS;
- 5 raíces;
- 2 policies;
- T0/T1;
- R64.

Objetivo: decidir posteriormente exclusividad vs acumulación y el tratamiento de Excepcional/Ascendido.

## Criterio

No existe piso de win-rate del jugador.
Bloquean: NaN/Inf, timeout/soft-lock, ruptura de identidad, floors/envelopes inválidos, T1 alterado o comportamiento imposible.
El runner no ratifica automáticamente ningún sufijo ni habilidad.
