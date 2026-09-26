# Baseline representativo — Monster Canonical Behavior Lab v0.1

## Alcance

Primera batería que conecta criaturas reales de `MOBS ver74` con el kernel auditado Monster Combat AI v0.1.

No ejecuta combate. Sólo selecciona intent.

## Cinco representantes

Asignaciones experimentales, NO canónicas:

```text
rata_qi          → INSTINTIVO / COLONIA
serpiente_qi     → REACTIVO_1 / SOLITARIO
lobo_espiritual  → CAZADOR_2 / MANADA
devorador_niebla → TACTICO_3 / SOLITARIO
mantis_nube      → MASTER_4 / SOLITARIO
```

## Qué se prueba

- los 19 MOBS pueden pasar por `CADENCE_COMPAT`;
- la cadencia `round % tecnica.cada === 0` se preserva exactamente;
- el aviso corresponde a la ronda previa;
- básico y técnica se traducen a IDs separados;
- veneno/quemadura/drenaje se etiquetan sin ejecutar efectos;
- las técnicas de daño puro permanecen ofensivas;
- sólo los cinco representantes pueden entrar en `DECISION_EXPERIMENTAL`;
- las ventanas de memoria 0/1/2/3/4 están conectadas;
- el adaptador no inventa pesos de memoria/social/señales;
- no se muta canon ni se ejecuta daño.

## Límite deliberado

El adaptador actual crea:

```text
memoryWeights = {}
socialWeights = {}
signalWeights = {}
```

Por tanto, aunque el perfil cognitivo limite cuánto recuerda cada criatura, esa memoria todavía no cambia el score de una habilidad canónica.

Esto es importante: **el baseline valida cableado y compatibilidad, no personalidad táctica final**.

La siguiente capa deberá ser una política experimental separada para pesos tácticos, nunca agregada al snapshot canónico.

## Estado

`REPRESENTATIVE_MONSTER_BASELINE: 18_PASS_0_FAIL_CONFIRMED`


## Ejecución confirmada

```text
Representative baseline: 18 PASS / 0 FAIL
Canon transversal:       13 PASS / 0 FAIL
Acumulado actual:         31 PASS / 0 FAIL
```

Se verificó sobre los archivos exactos de la rama:

- 19/19 MOBS producen un único intent compatible con la cadencia oficial;
- 16/16 técnicas aparecen exactamente en su ronda `cada`;
- 3 criaturas sin técnica permanecen en ataque básico;
- efectos canónicos se etiquetan sin ejecutarse;
- perfiles representativos limitan memoria a 0/1/2/3/4;
- criaturas sin asignación explícita no entran silenciosamente en `DECISION_EXPERIMENTAL`;
- el resultado del kernel permanece congelado y el snapshot canónico no se muta.
