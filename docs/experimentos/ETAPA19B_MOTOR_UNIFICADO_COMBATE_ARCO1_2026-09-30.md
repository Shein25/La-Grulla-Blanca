# ETAPA19B — Motor unificado de combate Arco 1

**Fecha:** 2026-09-30  
**Rama:** \`experiment/combat-stat-contract-v0.1\`  
**Estado:** LAB / PROVISIONAL. No runtime. No HTML. No merge.

## 1. Objetivo

ETAPA19B cubre el hueco entre los laboratorios aislados de técnicas y la matriz masiva de ETAPA19:

1. serializar las 15 técnicas de Arco 1 en un catálogo machine-readable;
2. compilar cualquier ruta legal de ramas sin interpretar prosa durante la simulación;
3. resolver combate 1v1 con el contrato nuevo de estadísticas;
4. incorporar raíces, progresión LianQi, equipo y monstruos traducidos;
5. ejecutar T0 NATURAL y T1 SURVIVAL bajo CADENCE_COMPAT;
6. producir métricas reproducibles para el screen masivo de LianQi I.

No se modifican todavía equipo, monstruos ni valores de balance como consecuencia de estos resultados.

## 2. Artefactos

- \`experimentos/balance_nuevo/techniques_arc1_catalog.json\`
- \`experimentos/balance_nuevo/etapa19b_combat_engine.py\`
- \`experimentos/balance_nuevo/etapa19b_selfcheck.py\`

Fuentes ya existentes reutilizadas:

- \`monster_arc1_new_contract_lab.json\`
- \`equipment_arc1_catalog.json\`
- \`etapa19_skill_buildspace.py\`
- \`TECNICAS_ARCO1_DISENO_APROBADO_2026-09-28.md\`
- contratos de combate/eventos y laboratorios de adaptación de monstruos.

## 3. Catálogo de técnicas

El catálogo contiene las 15 técnicas:

### Fuego
- Palma Ardiente
- Respiración del Cuerpo-Horno
- Círculo de las Cien Ascuas

### Metal
- Destello de Plata
- Armadura de Plata
- Lluvia de Filos

### Agua
- Latigazo de Marea
- Espejo de Luna
- Marea de las Ocho Orillas

### Tierra
- Golpe de Montaña
- Piel de Cobre
- Temblor de Montaña

### Viento
- Lanza que Parte Nubes
- Paso de Nube Ligera
- Tijera del Vendaval Partido

Cada técnica conserva:
- raíz;
- rol;
- targeting;
- coste;
- daño base provisional;
- tres Tramos;
- tres familias de rama por Tramo;
- parámetros necesarios para compilar sin re-interpretar la prosa;
- hooks defensivos/ofensivos/control/DOT/debuff.

El catálogo está etiquetado \`PROVISIONAL_LAB_INPUT_NOT_RUNTIME_CANON\`.

## 4. Compilador de ramas

\`compile_technique()\` transforma una técnica + secuencia de elecciones en una acción normalizada.

\`compile_build()\` compila las tres técnicas de una raíz.

El self-check recorre exhaustivamente todas las builds legales de LianQi IV:

- 11.512 por raíz;
- 5 raíces;
- **57.560 builds compiladas**.

Como los espacios LI–LIII son subconjuntos de la misma gramática, esta prueba cubre todas las longitudes de ruta disponibles.

Conteos esperados por raíz:
- LI: 1
- LII: 37
- LIII: 739
- LIV: 11.512

## 5. Contrato resuelto por el motor

### Impacto

\`P(hit)=clamp(Precision + modifiers - Evasion, 5, 100)\`

### Crítico

Base 5%, multiplicador 1.50 salvo modificadores explícitos.

### DEF

Orden:
1. DEF real;
2. shred;
3. penetración porcentual;
4. penetración plana;
5. DEF efectiva >= 0.

La DEF es reducción plana y puede llevar daño a 0.

### Redondeo

\`ROUND_HALF_UP\` una vez después de DEF y antes de Absorción/HP.

### DOT

- ignora DEF;
- sí atraviesa el pipeline de Absorción;
- no usa el scalar de cultivo de daño directo.

### AOE en 1v1

Se conserva el scalar provisional 0.65 cuando sólo existe un objetivo.

## 6. Sistemas representados

El motor ya puede interpretar en un mismo combate:

- daño directo;
- Golpe básico;
- Qi y fallback por agotamiento;
- crítico;
- Precisión/Evasión;
- DEF y penetración;
- DOT;
- Absorción;
- Control/Tenacidad;
- debuffs temporales;
- Palma / Quemadura;
- Cuerpo-Horno / Calor;
- Círculo;
- Destello;
- Armadura / Placas;
- Lluvia / Ruptura;
- Latigazo / Arrastre y anti-lock;
- Espejo / Reflujo;
- Marea;
- Golpe / Peso;
- Piel / Arraigo;
- Temblor / Resonancia;
- Lanza;
- Paso / respuesta tras evasión;
- Tijera;
- efecto de Absorción por umbral del Espejo de Pulso Velado.

## 7. Monstruos y CADENCE_COMPAT

El motor consume \`monster_arc1_new_contract_lab.json\`.

La técnica canónica del monstruo sigue siendo obligatoria cuando su cadencia toca. T1 no reemplaza esa cadencia.

Para T1:
- HP y daño usan el multiplicador C_STAGGERED T1;
- la población obtiene su E1 Survival;
- la defensa Survival consume la acción;
- cooldown LAB heredado: 2 rondas;
- EVADE_NEXT / DEFENSE_UP se consumen con la siguiente acción del jugador;
- MITIGATE_NEXT se consume con el siguiente impacto conectado;
- ABSORB_RESERVE conserva reserva y límite por golpe.

## 8. Dos bridges LAB explícitos

El laboratorio histórico de monstruos dejó semánticamente las señales:
- \`SELF_LOW_HP\`;
- \`TOOK_HEAVY_HIT\`;

pero no congeló sus umbrales numéricos.

Por eso ETAPA19B NO los disfraza de CANON. Se exponen en:

\`LabSignalBridge(low_hp_ratio=0.30, heavy_hit_ratio=0.20)\`

con provenance:

\`LAB_SIGNAL_BRIDGE_SENSITIVITY_REQUIRED\`

Antes de cerrar balance T1 deben correrse sensibilidades sobre esos umbrales.

Además, \`DEFENSE_UP\` se traduce temporalmente a DEF plana del contrato nuevo usando el \`defense_bonus\` ya almacenado en el perfil LAB. Esta traducción sigue siendo LAB hasta congelar explícitamente el bridge semántico.

## 9. Políticas del jugador para screening

El motor incorpora políticas simples y trazables:

- \`UNITARGET_FIRST\`
- \`DEFENSE_OPEN\`
- \`AOE_FIRST\`
- \`ROTATION\`

No representan todavía una IA óptima del jugador. Su función es separar potencia mecánica de decisiones y detectar sensibilidad a estilo de uso.

La matriz seria no debe declarar una build rota o débil a partir de una sola política.

## 10. Métricas

Se registran, entre otras:

- win rate;
- rondas/TTK;
- HP final;
- Qi final;
- Qi gastado;
- daño/Qi;
- daño directo;
- daño DOT;
- daño recibido;
- daño evitado por DEF;
- daño absorbido;
- hit rate;
- crit rate;
- intentos/éxitos de Control;
- evasiones;
- procs defensivos;
- procs adaptativos;
- uso de técnicas;
- uso de básico;
- derrotas asociadas a agotamiento de Qi.

## 11. Validación ejecutada

Validaciones estructurales:
- catálogo: 15/15 técnicas;
- árboles: 3 Tramos × 3 ramas;
- compilación de las 27 rutas completas por técnica;
- espacio LIV: 57.560 builds legales compiladas;
- catálogo real de monstruos en la rama: 18 perfiles;
- monstruos LI nativos: 5;
- catálogo real de equipo: 68 piezas.

Smoke local del motor:
- 5 raíces;
- 5 monstruos LI;
- T0 y T1;
- 3 políticas;
- 50 iteraciones por celda;
- **150 celdas / 7.500 combates**;
- semilla base 20260930;
- determinismo comprobado repitiendo una llamada con la misma semilla.

El entorno local usado para el smoke contenía deliberadamente sólo los 5 perfiles LI, por lo que el self-check completo marca \`MONSTER_COUNT:5!=18\` en ese fixture. Esa discrepancia no existe en el archivo real de la rama, que contiene los 18 perfiles. El self-check del repositorio mantiene la aserción 18/18 para Colab.

## 12. WATCH / todavía no cerrar

Aunque el compilador acepta todas las ramas, NO usar aún los resultados LII–LIV como balance final.

Pendientes para validar al llegar a esas etapas:

1. duración especial de Temblor cuando ya existía reducción de EVA;
2. recuperación/extensión de Piel por fallos de Control enemigo;
3. recuperación de Placas de Armadura por fallos de Control;
4. refund grupal de Marea;
5. AOE real contra 2+ enemigos;
6. orden fino de expiración de algunos buffs de Tramo alto;
7. sensibilidad de \`LabSignalBridge\`;
8. bridge final de \`DEFENSE_UP\` al contrato nuevo.

Estos puntos no afectan la validez del primer screen de **LianQi I**, porque LI no tiene puntos de rama.

## 13. Siguiente bloque

**ETAPA19C — LianQi I exhaustivo lógico.**

Orden:

1. enumerar las 6.144 combinaciones de equipo LI;
2. agregar las 5 raíces;
3. calcular firmas mecánicas;
4. colapsar equivalentes;
5. screen analítico/barato contra los 5 monstruos LI en T0/T1;
6. incluir varias políticas de jugador;
7. garantizar cobertura de todos los objetos;
8. seleccionar fronteras/anomalías/extremos;
9. recién entonces ejecutar Monte Carlo fuerte;
10. producir \`build_catalog\`, \`matchups\`, agregados, impacto de items/raíces y outliers.

No cambiar números antes de ese análisis.
