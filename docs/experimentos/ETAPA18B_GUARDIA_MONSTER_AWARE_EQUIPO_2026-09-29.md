# ETAPA 18B — Guardia Monster-Aware para diseño de equipo

Fecha: 2026-09-29
Rama: experiment/combat-stat-contract-v0.1
Estado: **GUARDIA DE DISEÑO / SIN MONTE CARLO TODAVÍA**

## Objetivo

Impedir que el equipo de Arco 1 se diseñe mirando únicamente:
- enemigos LianQi I;
- benchmarks simplificados;
- fichas desnudas del jugador.

El catálogo debe anticipar la progresión real de monstruos y la integración futura de Monster AI / adaptación.

## 1. Bandas nativas de monstruos ya definidas experimentalmente

Distribución:
- LianQi I: 5 especies;
- LianQi II: 5;
- LianQi III: 4;
- LianQi IV: 4.

Ejemplos relevantes de ver74:

### LianQi I
- Rata: HP9, daño1d4.
- Lobo espiritual: HP18, daño1d6+1; técnica1d6+3.

### LianQi II
- Escarabajo de Hierro: HP21, DEF legacy15, técnica1d8+3.
- Sapo Caldera: HP34, daño2d6, técnica2d6+4 + quemadura.
- Rey Escarabajo: HP38, DEF legacy16, técnica2d8+2.

### LianQi III
- Anguila Estelar: HP30, daño1d8+2, técnica1d8+4 + drenaje7 Qi.
- Sombra Ahogada: HP42, daño2d6 + aflicción.
- Guardián Coral: HP52, daño2d6+1, técnica2d8+3 + drenaje8 Qi.

### LianQi IV
- Devorador de Niebla: HP38, daño2d6.
- Halcón de Tormenta: daño2d6, técnica2d6+4.
- Mantis de Nube: HP46, daño2d6+2, técnica2d8+3.
- Centinela de Plumas: HP48, daño2d6+2, técnica2d6+4.

Estos valores son evidencia de ESCALA/IDENTIDAD de ver74. Su antiguo campo DEF/ataque no se transpone directamente al nuevo contrato sin conversión, porque la semántica de DEF fue rediseñada.

## 2. Tendencia natural

Promedios de fichas legacy por banda:

| Etapa | HP medio | daño básico medio |
|---|---:|---:|
| I | 13.4 | 3.3 |
| II | 29.0 | 5.9 |
| III | 37.5 | 6.75 |
| IV | 40.75 | 8.0 |

La progresión no es una simple fórmula lineal: rol y especie importan.
Boss/Elite pueden superar ampliamente la media.

## 3. Monster Adaptive Survival

E1 puede añadir defensas propias de especie:
- EVADE_NEXT;
- DEFENSE_UP;
- ABSORB_RESERVE;
- MITIGATE_NEXT.

Ejemplos candidatos cerrados en laboratorio:
- Rata/Avispa +25 EVA temporal;
- Lobo +3 DEF temporal;
- Sapo Ceniza mitiga35%;
- Escarabajo absorbe4 por golpe / reserva8;
- Rey Escarabajo absorbe5 / reserva10;
- Guardián Coral absorbe5 / reserva10;
- Mantis/Centinela +5 DEF temporal.

La defensa consume acción y tiene cooldown, pero obliga al equipo ofensivo a considerar:
- Precisión;
- Penetración;
- daño suficiente;
- economía de Qi;
- timing.

## 4. C_STAGGERED

Modelo seleccionado de adaptación poblacional.

Por presión real puede progresar:

T1:
- HP x1.025;
- daño x1.025;
- E1 de supervivencia.

T2:
- HP x1.05;
- daño x1.05;
- HIT +1;
- memoria persistente;
- defensa anticipatoria elegible.

T3:
- HP x1.075;
- daño x1.075;
- HIT +1;
- EVA +5;
- counter específico de especie.

T4:
- HP x1.10;
- daño x1.10;
- HIT +1;
- EVA +5;
- crítico base5% ->10%;
- segunda adaptación compatible.

El jugador NO regala esos tiers al subir: la población debe aprenderlos mediante presión real.

## 5. Memoria y feedback

La integración experimental ya demostró la cadena:

Monster Combat AI
→ Intent Bridge
→ resultado real
→ Signal Adapter
→ Semantic Memory
→ siguiente decisión.

Ejemplo confirmado:
un Guardián Coral que observa repetidamente que su técnica falla contra Absorción puede dejar de priorizarla en modo experimental.

También existen modificadores de contexto:
- MANADA;
- OPORTUNISTA;
- HP bajo;
- memoria de defensa efectiva;
- cognición INSTINTIVO/REACTIVO/CAZADOR/TACTICO/MASTER.

Esto significa que el equipo no puede evaluarse sólo por DPS estacionario.

## 6. Consecuencias obligatorias para el equipo

### DEF
No limitar artificialmente la armadura por miedo a benchmarks LI.
La curva provisional de Vestidura +1/+2/+3/+4 DEF es válida como punto de partida y podrá subir/bajar sólo tras benchmark II–IV.

### HP
Debe existir como segunda capa defensiva porque:
- DOT ignora DEF;
- drenajes/aflicciones cambian el combate;
- golpes de boss son significativamente mayores.

### Precisión
No es un stat cosmético:
- monstruos pueden usar EVADE_NEXT;
- C_STAGGERED T3/T4 añade EVA;
- fauna avanzada ya tiene identidades móviles.

### Penetración
Debe tener oferta suficiente:
- Escarabajos/guardianes poseen identidad defensiva;
- Survival puede añadir DEF/Absorción;
- no debe existir una única pieza obligatoria.

### Qi
Debe considerarse contra:
- Anguila Estelar;
- Guardián Coral;
- Macaco;
- combates más largos por supervivencia adaptativa.

### Tenacidad / Control
Su valor crecerá cuando kits enemigos y bosses incorporen más Control real.
No retirar estas opciones porque un benchmark puro de daño no las use.

### Evasión
Será valiosa contra daño directo creciente, pero debe medirse contra HIT/Precisión de fauna alta y C_STAGGERED.

### daño de técnicas
Los bonos modestos de equipo son correctos como contrapeso a HP/defensas mayores, pero deben medirse junto con:
- scalar de cultivo;
- ramas;
- crítico;
- Penetración;
- defensa adaptativa.

## 7. Regla de simulación futura

Cada etapa deberá probarse en al menos:

1. T0 NATURAL;
2. T1 SUPERVIVENCIA;
3. población veterana elegible según ceiling;
4. NORMAL;
5. SKIRMISHER/TANK;
6. ELITE/APEX;
7. BOSS.

Y cuatro perfiles de equipo:
- NAKED;
- MANDATORY_ENTRY;
- EXPECTED_STAGE;
- HIGH_ROLL_STRESS.

No se promoverá a CANON ningún presupuesto de equipo II–IV antes de este cruce.

## 8. Frontera ver75/ver76

Los módulos cerrados todavía estaban en laboratorio/integración experimental:
- Monster Combat AI;
- Tactical Overlay;
- Intent Bridge;
- Semantic Memory;
- Signal Adapter;
- Feedback Loop;
- Structured Hooks.

Por tanto:
- no fingir que ya ejecutan productivamente todos los efectos;
- sí diseñar equipo anticipando que serán integrados;
- no codificar counters específicos de un monstruo dentro de un objeto.

## 9. Estado

El catálogo ETAPA18/18A sigue siendo PROVISIONAL.

Desde ahora:
> ningún nuevo equipo puede diseñarse o cerrarse sin revisar su función frente a la progresión nativa de monstruos y a las capas adaptativas seleccionadas.

La auditoría de adquisición y el Monte Carlo masivo siguen diferidos por decisión humana.
