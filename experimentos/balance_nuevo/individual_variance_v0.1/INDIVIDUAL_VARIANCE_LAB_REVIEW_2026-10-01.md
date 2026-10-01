# INDIVIDUAL_VARIANCE_LAB LianQi I — revisión Heavy

Fecha: 2026-10-01

## Integridad

Archivo:

`RESULTADOS_INDIVIDUAL_VARIANCE_LAB_LIANQI_I_V01.zip`

SHA-256:

`5e077b9513aedc36502a214b37c7f8e8a3f5ce2ed7577e5bc8811c35039f8aae`

Contrato:

- 5 especies LianQi I;
- 10 contextos expandidos por especie;
- 5.000 peleas naturales/contexto;
- 1.000 peleas Mutante condicionadas/contexto;
- 250.000 peleas naturales;
- 50.000 peleas Mutante condicionadas;
- 300.000 peleas totales;
- 4 workers;
- no raw fights;
- no canonical write;
- no runtime activation;
- no T1-T4.

## Incidencia Mutante

Global:

- 1.889 Mutantes / 250.000 spawns naturales;
- incidencia: **0,7556%**;
- objetivo LAB: 0,75%;
- guardia: <1%;
- Wilson 95% aproximado: 0,7224%–0,7903%.

Por especie:

| especie | Mutantes / 50k | incidencia |
|---|---:|---:|
| Rata | 359 | 0,718% |
| Avispa | 391 | 0,782% |
| Serpiente | 356 | 0,712% |
| Mono | 378 | 0,756% |
| Lobo | 405 | 0,810% |

Todas permanecen <1%.

El muestreo condicionado acepta aproximadamente 0,736%–0,758% de intentos,
consistente con el brazo natural.

## Normal vs Mutante

### Rata

Normal natural:

- victoria jugador: 99,976%;
- HP final: 77,11%;
- daño monstruo: 7,25;
- rondas: 3,27.

Mutante condicionado:

- victoria jugador: 99,78%;
- HP final: 65,28%;
- daño monstruo: 10,99;
- rondas: 3,89.

La Rata Mutante es claramente superior a la normal de su especie, pero sigue
siendo una amenaza baja en términos absolutos, coherente con su posición de
amenaza sobrenatural inicial.

### Avispa

Normal natural:

- victoria jugador: 88,26%;
- HP final: 59,62%;
- daño monstruo: 12,79;
- DOT: 71,57% del daño.

Mutante condicionado:

- victoria jugador: 60,29%;
- HP final: 31,32%;
- daño monstruo: 21,75;
- DOT: 67,21%.

La cola Mutante produce un salto material de dificultad sin perder la identidad
de DOT/evasión.

### Serpiente

Normal natural:

- victoria jugador: 74,57%;
- HP final: 39,23%;
- daño monstruo: 19,25;
- DOT: 86,05%.

Mutante condicionado:

- victoria jugador: 33,98%;
- HP final: 13,81%;
- daño monstruo: 27,29;
- DOT: 88,02%.

La identidad de veneno sostenido se conserva tanto en normales como Mutantes.

### Mono

Normal natural:

- victoria jugador: 53,34%;
- HP final: 19,36%;
- daño monstruo: 25,51;
- Qi drenado: 11,20.

Mutante condicionado:

- victoria jugador: 8,41%;
- HP final: 1,94%;
- daño monstruo: 31,01;
- Qi drenado: 11,34.

El QI_DRAIN permanece fijo y visible; la diferencia Mutante proviene de la
convergencia de supervivencia, precisión y daño.

### Lobo

Normal natural:

- victoria jugador: 26,72%;
- HP final: 7,01%;
- daño monstruo: 29,41.

Mutante condicionado:

- victoria jugador: 1,19%;
- HP final: 0,23%;
- daño monstruo: 31,55.

El Lobo conserva el papel APEX_BRIDGE, pero la distribución uniforme convierte
a la población natural media en una amenaza mucho mayor que el T0 canónico.

## Validación del muestreo Mutante

Los Mutantes observados espontáneamente en el brazo natural coinciden bien con
los 10.000 Mutantes condicionados por especie.

Win jugador, observado natural vs condicionado:

- Rata: 99,721% vs 99,780%;
- Avispa: 61,381% vs 60,290%;
- Serpiente: 33,427% vs 33,980%;
- Mono: 8,730% vs 8,410%;
- Lobo: 1,481% vs 1,190%.

Esto valida el rejection sampling para estudiar la cola sin alterar la
estimación de incidencia.

## Loadout

La diferencia EXPECTED_STAGE vs MANDATORY_ENTRY sigue siendo pequeña comparada
con la diferencia entre especies/individuos.

Win normal natural:

- Rata: 99,97% vs 99,98%;
- Avispa: 88,32% vs 88,21%;
- Serpiente: 75,03% vs 74,12%;
- Mono: 54,25% vs 52,43%;
- Lobo: 27,63% vs 25,80%.

No aparece una dependencia fuerte del loadout.

## Raíces

La raíz Fuego tiende a rendir mejor frente a las cuatro especies ofensivamente
más fuertes. La variabilidad no elimina la sensibilidad de identidad ya vista
en T0.

Casos más extremos en Mutantes condicionados:

- Mono: Fuego 16,85% win vs Viento 4,20%;
- Lobo: Fuego 4,60% vs Viento 0,25%;
- Serpiente: Fuego 57,95% vs Tierra 24,30%.

Esto debe conservarse como dato de diseño; no es un fallo de reproducibilidad.

## Hallazgo principal de diseño

La distribución actual es `UNIFORM_0_1` independiente por eje.

Por construcción:

- T0 = piso;
- media de cada q ≈ 0,5;
- los escalones de ataque se reparten casi uniformemente.

Por eso la criatura natural promedio está aproximadamente en el centro de la
envolvente T0→techo, no cerca del T0.

Esto explica el fuerte aumento de amenaza respecto de los T0 individuales ya
cerrados:

- Avispa T0 ≈ 99,985% win jugador → normal variable 88,26%;
- Serpiente T0 100% → normal variable 74,57%;
- Mono grid43 99,474% → normal variable 53,34%;
- Lobo T0 90,226% → normal variable 26,72%.

Esto **no invalida** el mecanismo: es la consecuencia directa de haber elegido
"T0 como piso + tirada uniforme hasta el extremo medido".

## Estado

### Mecánicamente validado

- un único species_id por especie;
- variación defensiva y ofensiva;
- tiradas independientes;
- T0 nunca sustituido en el registro canónico;
- Mutante <1%;
- XP x1.5;
- botín x1.5;
- no T1-T4;
- no nuevos monstruos de catálogo;
- muestreo condicionado válido para análisis de Mutantes.

### Decisión todavía abierta

La única cuestión pendiente antes de runtime es la **forma de la distribución
natural**:

A. mantener UNIFORM_0_1, haciendo que el individuo medio esté a mitad de camino
entre T0 y techo;

B. sesgar la distribución hacia T0 sin eliminar la posibilidad de extremos,
manteniendo la cola Mutante <1%.

No debe activarse runtime hasta fijar esta decisión de distribución.

