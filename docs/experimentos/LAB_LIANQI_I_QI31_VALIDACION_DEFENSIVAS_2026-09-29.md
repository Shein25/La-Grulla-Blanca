# LAB — Validación de Qi31 con defensivas recalibradas

Fecha: 2026-09-29  
Rama: `experiment/combat-stat-contract-v0.1`  
Estado: **LAB / CANDIDATO ESTRUCTURAL / NO PROVISIONAL**

## Objetivo

Comprobar si el candidato de economía mixta `Qi máximo = 31` sigue siendo
sano después de recalibrar las defensivas débiles.

Candidatos LAB usados:

- Fuego: Cuerpo-Horno 25% HP / 2 turnos;
- Metal: Armadura de Plata actual;
- Agua: Espejo 24% HP / Reflujo25% / 3 turnos;
- Tierra: Piel de Cobre actual;
- Viento: Paso +35 EVA / 4 turnos.

## Estructura discreta

Costes efectivos base:

- ofensivas iniciales: 6 Qi;
- defensivas Fuego/Metal/Tierra/Viento: 7 Qi;
- defensiva Agua: 6 Qi efectivos por raíz principal.

### Qi30

- ofensiva pura: 5×6 = 30;
- Agua: defensa6 + 4×6 = 30;
- resto: defensa7 + 3×6 = 25; sobran5.

Resultado: Agua puede ejecutar una ofensiva adicional respecto de las otras
raíces defensivas por un acantilado aritmético.

### Qi31

- ofensiva pura: 5×6 = 30; sobra1;
- Agua: defensa6 + 4×6 = 30; sobra1;
- resto: defensa7 + 4×6 = 31; sobra0.

Resultado:

> las cinco raíces disponen del mismo presupuesto de cinco técnicas totales si
> una de ellas es la defensiva.

### Qi32–35

No añaden una nueva acción técnica respecto de Qi31; sólo aumentan residuo.

### Qi36

- ofensiva pura: 6×6;
- Agua: defensa6 + 5×6;
- defensivas7: todavía no pueden hacer defensa +5 ofensivas.

Aparece un nuevo desfase.

### Qi37

- defensiva7 + 5×6 = 37.

Pero esto eleva todo el presupuesto de LianQi I a seis técnicas ofensivas y es
un salto de economía mucho mayor que el necesario para resolver el problema
actual.

## Monte Carlo de sensibilidad

Con las defensivas recalibradas, el salto relevante se observa al pasar de
Qi30 a Qi31 en Fuego/Metal/Tierra/Viento.

A partir de Qi31 y hasta Qi35 los resultados cambian sólo por ruido de muestreo
porque el número de técnicas utilizables no cambia.

Esto confirma que Qi31 es una **frontera estructural**, no una optimización
accidental de una sola técnica.

## Resultado

```text
QI31
→ mejor candidato LAB actual para LianQi I
→ mínimo que iguala economía defensiva entre las cinco raíces
→ no promover todavía a PROVISIONAL
```

Antes de promoción debe cruzarse con:

- HP/DEF/EVA base del jugador;
- HP/Precisión/daño del enemigo de referencia;
- stress multi-enemigo de Piel/Placas/Paso;
- resto de técnicas base disponibles en LianQi I.

