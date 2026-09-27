# Backup maestro de continuidad — La Grulla Blanca
Fecha: 2026-09-27

## Propósito

Respaldo estructurado de continuidad del proyecto para poder retomar trabajo, auditorías e integración sin depender del historial del chat.

IMPORTANTE: este snapshot NO modifica main y NO hace merge.

## Estado de Git / integración

- Repositorio: Shein25/La-Grulla-Blanca
- Rama de respaldo: snapshot/handoff-2026-09-27-astra-a04
- Base remota del snapshot: main
- main permanece sin modificar.
- Los commits A01–A04 informados por Astra no están publicados actualmente en GitHub; por eso este snapshot respalda su estado documental, hashes y decisiones, pero no puede contener esos commits hasta que sean publicados.

### Commits de integración informados por Astra

- A01 — World / Perception Adapter
  - 248396792aa769e7b3e577aca4fff6ad50a7a326
  - CERRADO
- A02 — Knowledge / Permission Guard
  - 2f6363f9c07d229ff2a3a6cd5ada3bc538469d32
  - CERRADO
- A03 — Navigation
  - 8365c9e87fea49d9bf914befc5b921fa6b691563
  - CERRADO
- A04 — Action Adapter
  - 7a5ac9a46e66ce83b8959de4f70dfc6a8d7ab683
  - CERRADO
- A05 — Domain State
  - EN CURSO

## Reglas de trabajo

1. No trabajar directamente sobre main.
2. No hacer merge salvo instrucción explícita.
3. Mantener ramas y commits auditables.
4. No modificar ROOMS.exits.
5. No inventar rooms, exits, NPC, monstruos, gates, permisos, revelaciones, estados de misión o persistencia.
6. Separar canon documental, implementación productiva, propuestas históricas y experimentos.
7. Las decisiones humanas posteriores prevalecen.
8. AI decides, motor resolves.
9. No crear nuevas arquitecturas IA sin necesidad técnica reproducible.
10. No avanzar al siguiente bloque automáticamente sin revisión.

## Runtime autorizado

- grulla-blanca_ver76.html
- SHA-256: b41c12431f076790b2e2fb0e9e485fb35d3b8c7a834d7b1222e9105518eb270a
- cierre ver76 SHA-256: 45fc0307e94e1b5261120b6fc4ce638fadae9a5014c24b21529acaad47f84648
- paquete final Astra import SHA-256: e2da147a9100a81c8536e6cd620f8048d7574a53d704138fa2c2574449ec8c33

## Arc1 documental

Arc1 documental cerrado:
- Prologue + M01–M07
- M08–M11
- M12
- M13–M15
- M16
- M17
- M18
- Epílogo

Runtime ver76 implementa Prologue–M07. M08–M18/Epílogo requieren integración productiva.

## IA cerrada para handoff

### NPC
- 32/32 cubiertos.
- No existe asignación histórica canónica fija por NPC.
- Integración: seleccionar por NPC la arquitectura más simple ya probada que cubra su rol.
- Selección baseline Astra:
  - FSM: 13
  - Behavior Tree: 8
  - Utility + GOAP + Execution: 8
  - Utility diálogo: 2
  - Memory → Relations → Utility → GOAP → Execution: 1

### Monstruos
- 18/18 combatientes.
- muneco_practica excluido.
- CADENCE_COMPAT conserva autoridad.
- C_STAGGERED, T0–T4, thresholds, decay, maxTierReached, learning ceiling y Survival E1 congelados.

### Grulla
- controlador separado.
- fases I–III, memoria, counters, anti-spam y contratos cerrados.
- test:grulla-integration-ready debe ejecutarse antes y después de conexión productiva.

## Dormancy / Catch-up

Resuelto experimentalmente:
- sólo área activa del jugador simula continuamente;
- áreas dormidas: 0 Scheduler, Utility, GOAP, Pathfinder y Executor;
- activeAreaId como fuente de verdad;
- catch-up resuelve estado final sin reproducir millones de turnos;
- agendas y overrides soportados.

## Mapa de integración

A01 World / Perception ✅
A02 Knowledge / Permission ✅
A03 Navigation ✅
A04 Action Adapter ✅
A05 Domain State ← EN CURSO
A06 Save / Load
A07 NPC Runtime
A08 Monster Runtime
A09 Grulla
A10 Arc1 Cross-Integration
A11 Stress / Regression / Memory
A12 Auditoría final / candidata jugable

## A01

- commit: 248396792aa769e7b3e577aca4fff6ad50a7a326
- 28 PASS / 0 FAIL
- 32 NPC
- 320 pares NPC/revelación
- 3.200 snapshots
- 329 rooms preservadas
- snapshots inmutables
- sin mutación de ver76
- Chromium pendiente por spawn EPERM

## A02

- commit: 2f6363f9c07d229ff2a3a6cd5ada3bc538469d32
- 42 PASS / 0 FAIL
- regresión A01: 28 PASS / 0 FAIL
- SOSPECHA ≠ SABE ≠ CONFIRMADO
- permisos actor-bound y scope exacto
- narrativa irreversible protegida
- gaps:
  - A02_PERMISSION_PROJECTION_BRIDGE
  - A02_VERIFIED_EVIDENCE_FEED

## A03

- commit: 8365c9e87fea49d9bf914befc5b921fa6b691563
- 34 PASS / 0 FAIL
- regresión A01+A02: 70 PASS / 0 FAIL
- pathfinder original 43/43 PASS
- stress 3.000 queries / 0 fallos
- 329 rooms
- 787 exits fuente
- 786 internos
- 1 frontera externa Arc2
- 11 gates
- 0 cambios a ROOMS.exits
- gaps:
  - A03_SCOPED_GATE_CONTEXT
  - A02_PERMISSION_PROJECTION_BRIDGE
  - A02_VERIFIED_EVIDENCE_FEED

## A04

- commit: 7a5ac9a46e66ce83b8959de4f70dfc6a8d7ab683
- 44 PASS / 0 FAIL
- regresión A01–A03: 104 PASS / 0 FAIL
- 624 movimientos canónicos directos
- 340 SUCCEEDED
- 284 rechazados pre-dispatch
- revalidación fresca
- deduplicación
- UNKNOWN_OUTCOME seguro
- sin auto-retry
- narrativa irreversible bloqueada
- gaps:
  - A04_ATOMIC_ENGINE_PORT
  - A04_SIMPLE_DIALOGUE_ENTRYPOINT
  - A05_DOMAIN_NOT_CONNECTED

## Diseño de diálogo autónomo — requisito futuro

Aún no implementado. Debe entrar antes o dentro de A07.

### Reglas lingüísticas
- PROHIBIDO el voseo.
- Español neutro.
- Registro adaptado a edad, rango, relación, personalidad y situación.

### Identidad
Cada NPC debe sentirse como una vida distinta, no una plantilla con nombre distinto.

La voz debe surgir de:
PERSONALIDAD + HISTORIA PERSONAL + MEMORIA + RELACIONES + CONTEXTO.

Deben variar:
- ritmo
- longitud de frase
- formalidad
- humor
- ironía
- prudencia
- orgullo
- miedo
- calidez
- forma de mentir
- relación con autoridad
- temas evitados
- experiencias previas

### Variables que modulan diálogo
- afinidad
- reputación
- memoria
- conocimiento real
- rango/rol
- contexto
- estado situacional/emocional

Las variables internas NO se muestran como números. Se perciben por tono, confianza, dureza, evasión, ayuda, hostilidad y cercanía.

### Entradas separadas
- diálogo canónico / misión
- diálogo autónomo con opciones
- banter breve
- NPC ↔ NPC

cmd_hablar() no debe reutilizarse para charla autónoma porque entra en lógica de misiones.
Hace falta una entrada segura futura, conceptual tipo hablarAutonomo()/emitirDialogoNPC(), sin side effects narrativos irreversibles.

### Opciones estilo Fallout
El jugador ve frases naturales, no etiquetas funcionales.

Ejemplo:
1. "¿Qué tiene de especial ese jade?"
2. "No dejas de mirar a Luo."
3. "Olvídalo."
4. [Comprensión] "Estás ocultando algo."

### Naturalidad
- evitar lenguaje de asistente/IA;
- evitar exposición enciclopédica;
- permitir silencios, evasión, interrupciones, dudas, ironía, respuestas parciales;
- no todos deben ser carismáticos de la misma forma;
- algunos pueden ser secos, otros cálidos, elegantes, mordaces, tímidos, técnicos, etc.;
- prueba de voz ciega: líneas sin nombre deberían poder asociarse razonablemente a su NPC.

## Anti-spam narrativo

Ningún sistema autónomo escribe directamente en UI.

Flujo:
EVENTO INTERNO → relevancia → prioridad → cooldown → agrupación → salida visible.

Prioridad sugerida:
- P0 crítico
- P1 importante
- P2 ambiente
- P3 interno/no visible

Reglas:
- aproximadamente 2–3 intervenciones espontáneas antes de devolver control al jugador;
- agrupar microeventos;
- no mostrar cada pensamiento/gesto;
- silencio válido;
- separar terminal principal / escena social / murmullos / log detallado.

## Arc2 — dirección

Foco: mundo regional vivo.

Ideas:
- encuentros vivos NPC ↔ monstruo ↔ jugador;
- rumores y propagación de conocimiento;
- política entre facciones;
- relaciones dinámicas;
- economía regional;
- recursos;
- rutinas autónomas;
- consecuencias persistentes;
- Demonios Internos / tribulación mental.

Encuentros vivos:
- combate puede haber empezado antes de llegar;
- el jugador puede intervenir o ignorar;
- no se reinicia el encuentro;
- puede continuar al retirarse el jugador;
- consecuencias persistentes.

## Arc3 — reservado

- Reinos Secretos procedurales distintos por partida.
- Formaciones / matrices espirituales.
- Subastas complejas.
- Herencias y economía de alto nivel.

### Reinos Secretos
Generación por semilla:
- topología
- bioma
- reglas espirituales
- recursos
- peligros
- NPC/facciones expedicionarias
- herencias
- condiciones de salida

### Subastas
Deben funcionar como simulación social xianxia:
- NPC conversando y discutiendo;
- facciones;
- reputación;
- dar cara como presión social no automática;
- alianzas temporales;
- sabotaje económico;
- conocimiento desigual;
- rumores;
- palcos;
- seguridad de la casa;
- sanciones/expulsión;
- memoria entre subastas;
- interfaz con lote, postores, escena social, rumores, historial, acciones y estado de ronda.

## Próximo punto de control

Esperar revisión de A05 — Domain State.

Auditar:
1. commit y parent;
2. dominios y fuentes;
3. que no invente recursos/estados;
4. estados médicos, archivo, formaciones, logística y M16;
5. regresiones A01–A04;
6. no autorizar A06 hasta cerrar A05.
