# Auditoría externa — motor de combate, estadísticas, Concordancias y técnicas

Fecha: 2026-09-28
Rama a auditar: experiment/combat-stat-contract-v0.1
Modo: LECTURA / NO IMPLEMENTAR / NO HACER COMMITS / NO MODIFICAR ARCHIVOS

# PROMPT PARA CLAUDE

Actúa como arquitecto senior de sistemas de combate y auditor de diseño técnico.

Estás auditando un MUD xianxia llamado La Grulla Blanca. No implementes nada todavía.

## RESTRICCIONES ABSOLUTAS

1. Trabaja únicamente en modo lectura.
2. NO modifiques archivos.
3. NO hagas commits.
4. NO cambies de rama.
5. NO hagas merge.
6. NO toques main.
7. NO propongas una reescritura completa sólo por preferencia personal.
8. Distingue estrictamente entre contradicción, hueco de especificación, riesgo arquitectónico, riesgo de balance y mejora opcional.
9. No trates valores provisionales de balance como errores arquitectónicos salvo que generen una imposibilidad lógica.
10. No inventes requisitos que no estén en los contratos.
11. Si dos documentos parecen contradecirse, cita ambos y explica exactamente el conflicto.
12. No des por implementado lo que sólo está documentado.
13. Prioriza correctitud y extensibilidad, no estética de código.

## RAMA

Audita: experiment/combat-stat-contract-v0.1

## ARCHIVOS PRINCIPALES

Lee completos, como mínimo:

1. docs/experimentos/CONTRATO_COMBATE_ESTADISTICAS_DOT_V0_1.md
2. docs/experimentos/CONTRATO_MOTOR_EVENTOS_EFECTOS_V0_1.md
3. docs/experimentos/TECNICAS_ARCO1_DISENO_APROBADO_2026-09-28.md
4. docs/experimentos/CHECKPOINT_TECNICAS_ARCO1_2026-09-28.md
5. docs/GUARDIA_RAMA_3C5_IMPLEMENTACION.md si existe en esta rama.
6. grulla-blanca_ver74.html para entender el runtime histórico/actual que eventualmente deberá migrarse.

Busca además cualquier documento relacionado con estadísticas, técnicas, DOT, daño, Concordancias, combate y NPC/monstruos cuando afecten el contrato.

## CONTEXTO

El objetivo del nuevo motor NO es que todas las mecánicas estén activas en Arco 1.

El objetivo es que el núcleo quede preparado para soportar sin una refactorización estructural posterior:

- daño directo;
- multigolpe;
- AOE;
- crítico;
- DEF;
- Penetración;
- Absorción;
- Control/Tenacidad;
- DOT y aflicciones;
- buffs/debuffs;
- curación;
- regeneración;
- Robo de Vida;
- Vida al impactar;
- Vida al matar;
- Qi;
- robo/drenaje de Qi;
- Reflect;
- Retaliation;
- Daño Aplazado;
- recursos internos;
- marcas/cargas;
- efectos reactivos;
- estados de comienzo/final de turno;
- Concordancias;
- ramas;
- equipo/pasivas;
- contenido futuro.

Reflect, Retaliation y Daño Aplazado deben quedar preparados, NO activados automáticamente en Arco 1.

# AUDITORÍA 1 — ESTADÍSTICAS

Audita:

- Vida / Vida máxima
- Qi / Qi máximo
- Ataque/modificadores ofensivos
- Precisión
- Evasión
- DEF
- Penetración porcentual
- Penetración plana
- Probabilidad crítica
- Daño crítico
- Control
- Tenacidad
- Absorción
- curación
- Robo de Vida
- coste de Qi

Para cada una informa:

1. fuente de verdad;
2. fórmula;
3. orden;
4. pisos/techos;
5. redondeo;
6. qué la modifica;
7. qué NO la modifica;
8. doble aplicación posible;
9. ambigüedades;
10. extensibilidad.

Busca doble scaling, penetración duplicada, doble tirada Precisión/Evasión, Control aplicado a debuffs ordinarios, Absorción tratada como DEF, raíces/injertos duplicados y redondeos intermedios.

# AUDITORÍA 2 — PIPELINE DE DAÑO

Reconstruye y verifica:

~~~text
acción
→ coste
→ precisión
→ porciones
→ planos
→ porcentajes
→ crítico
→ modificadores recibidos
→ DEF/penetración
→ redondeo
→ Absorción
→ Vida
→ freeze
→ efectos posteriores
~~~

Prueba:

1. impacto normal;
2. fallo;
3. crítico;
4. DEF a cero;
5. Absorción total;
6. Absorción parcial;
7. letal;
8. AOE;
9. multigolpe futuro;
10. híbrido.

Señala cualquier mutación retroactiva de un ImpactResult congelado.

# AUDITORÍA 3 — EVENT BUS / EFFECT ENGINE

Audita CONTRATO_MOTOR_EVENTOS_EFECTOS_V0_1.md.

Pregunta:

¿Con estas primitivas se puede añadir contenido futuro sin hardcodear IDs de técnicas en el resolver?

Comprueba:

- ActionContext
- ImpactResult
- DamagePacket
- HealPacket
- ResourcePacket
- ControlAttempt
- EffectDefinition
- Trigger
- Condition
- Operation
- frequency scopes
- priorities
- provenance
- root_action_id
- parent_event_id
- reaction_depth
- ventanas de mutación
- State Engine

No sugieras una primitiva nueva sólo para una técnica. Debe ser mecánica general reutilizable.

# AUDITORÍA 4 — RECURSIÓN

Intenta romper:

~~~text
Reflect → Reflect
Reflect → Retaliation
Retaliation → Reflect
Retaliation → Retaliation
DOT → Reflect
Reflect → Robo de Vida
Retaliation → Robo de Vida
daño secundario → ON_HIT → reacción
~~~

Comprueba flags, provenance y reaction_depth.

# AUDITORÍA 5 — RECUPERACIÓN

Diferencia:

~~~text
Curación directa
Regeneración
Robo de Vida
Vida al impactar
Vida al matar
~~~

Verifica modificadores, sobrecuración, crítico, AOE, multigolpe, límite por acción, Absorción, overkill, Daño Aplazado y exclusión de DOT/Reflect/Retaliation.

# AUDITORÍA 6 — DOT / AFLICCIONES / ESTADOS

Debe soportar:

- Quemadura;
- Hemorragia;
- Veneno futuro;
- intensidad acumulable;
- instancias independientes;
- refresh;
- DOT futuro con crítico explícito;
- DOT futuro que ignore Absorción explícitamente.

Audita stacking, duración, tick, fuente y kill attribution.

# AUDITORÍA 7 — CONTROL

Comprueba:

- fórmula Control/Tenacidad;
- clamp;
- ControlAttempt;
- SKIP_ACTION/Arrastre;
- lockouts;
- familias futuras;
- diferencia Control vs debuff estadístico;
- duración;
- frecuencia.

No inventes inmunidades universales de jefes.

# AUDITORÍA 8 — AOE

Contrato nuevo:

~~~text
AOE
→ todos los NPC hostiles de la sala
→ arrastra al combate
→ impacto independiente por objetivo
→ daño no se divide
→ 2+ objetivos = 100%
→ 1 objetivo = 65% provisional
~~~

Busca límites históricos 3/4/6 en documentos nuevos y revisa once_per_action, once_per_target, Robo de Vida, crítico, Precisión, Concordancias, estados y aggro.

Distingue runtime histórico de contrato nuevo.

# AUDITORÍA 9 — CONCORDANCIAS

Principio esperado:

Las Concordancias pertenecen a relaciones elementales globales; las técnicas sólo exponen hooks/capacidades.

Debe funcionar:

~~~text
ORIGEN → DESTINO
→ identidad elemental
→ prioridades por contexto
→ búsqueda de hook compatible
→ transformación válida
~~~

Y:

~~~text
sin hook compatible
→ NO consumir Eco
~~~

Evalúa una misma relación en técnica ofensiva, defensiva, Control, utilidad y técnica futura.

Busca Concordancias demasiado ligadas a un nombre de técnica o rama.

NO cierres números todavía.

Propón qué familias globales de hooks necesita cada una de las 20 relaciones dirigidas.

# AUDITORÍA 10 — 12 TÉCNICAS

Fuego:
- Palma Ardiente
- Respiración del Cuerpo-Horno
- Círculo de las Cien Ascuas

Metal:
- Destello de Plata
- Armadura de Plata
- Lluvia de Filos

Agua:
- Latigazo de Marea
- Espejo de Luna
- Marea de las Ocho Orillas

Tierra:
- Golpe de Montaña
- Piel de Cobre
- Temblor de Montaña

Para cada una:

~~~text
ROL
TAGS
HOOKS BASE
HOOKS AÑADIDOS POR RAMAS
TRIGGERS
ESTADOS
RECURSOS
FRECUENCIAS
CONCORDANCIAS POSIBLES
¿REQUIERE HARDCODE?
RIESGOS
~~~

No rebalancees salvo exploit arquitectónico evidente.

# AUDITORÍA 11 — RAMAS

Comprueba que las ramas puedan expresarse como datos:

- añadir hook;
- trigger;
- operación;
- coste;
- duración;
- stacking;
- máximo;
- sinergia.

Busca condiciones de ramas que obliguen a hardcode dentro del núcleo. Las sinergias pueden existir, pero en definición/configuración de contenido.

# AUDITORÍA 12 — PRUEBAS ADVERSARIALES

Intenta expresar SIN modificar núcleo:

A)
Durante 3 turnos +5 Tenacidad. Al recibir daño directo aplica Veneno al atacante. Si ya estaba envenenado recupera 2 Qi. Máximo una vez por turno.

B)
20% Reflect + 3 Retaliation.

C)
30% del daño comprometido a Vida se aplaza en dos pagos.

D)
Al crítico roba hasta 3 Qi. Máximo una vez por objetivo por acción.

E)
Una barrera se regenera al inicio del turno mientras no haya sido destruida.

F)
Al romper una barrera obtiene Evasión durante un turno.

G)
Al tercer stack de una marca, consume stacks e intenta Control.

H)
Nueva técnica Fuego crea una zona persistente. Tierra→Fuego debe potenciar persistencia sin conocer el ID.

Para cada caso:

- expresable;
- expresable con ambigüedad;
- no expresable;
- primitive/hook faltante.

# FORMATO DE RESPUESTA

## 1. Resumen ejecutivo

Máximo 15 puntos. Clasifica cada hallazgo:

BLOQUEANTE / ALTO / MEDIO / BAJO / CORRECTO

No uses puntaje numérico global.

## 2. Contradicciones verificadas

| Severidad | Archivo A | Archivo B/código | Contradicción | Evidencia | Corrección mínima |

## 3. Huecos del contrato

| Severidad | Sistema | Hueco | Consecuencia | Propuesta |

## 4. Riesgos de hardcode

| Sistema/técnica | Riesgo | Cómo expresarlo como dato |

## 5. Auditoría de estadísticas

Una subsección por estadística.

## 6. Pipeline

Reconstrucción paso a paso.

## 7. Eventos/efectos

Suficiencia y primitivas faltantes.

## 8. Concordancias

Familias globales de hooks/prioridades, sin números.

## 9. Técnicas

Una ficha por técnica.

## 10. Casos adversariales

A-H.

## 11. Suite de pruebas

Separar:

- unit tests;
- integration tests;
- property/invariant tests;
- benchmark/balance tests.

## 12. Decisiones del diseñador

Lista de cuestiones que NO debe decidir el auditor.

# CRITERIO DE BLOQUEANTE

Marca BLOQUEANTE sólo si:

- dos contratos son imposibles de cumplir simultáneamente;
- existe recursión/infinito;
- un evento puede contarse dos veces sin regla;
- el diseño obliga estructuralmente a hardcode;
- un orden indeterminado cambia materialmente el resultado.

Un valor provisional de daño no es bloqueante.

Cuando dependa de intención de diseño, marca:

DECISIÓN DEL DISEÑADOR

y no la resuelvas unilateralmente.

# PREGUNTAS FINALES

Responde explícitamente:

1. ¿Las estadísticas tienen una sola fuente de verdad?
2. ¿El pipeline es determinista?
3. ¿El motor soporta estados y reacciones futuras?
4. ¿Reflect/Retaliation están seguros contra recursión?
5. ¿Robo de Vida evita doble conteo?
6. ¿Concordancias soportan técnicas futuras sin hardcode?
7. ¿Las ramas pueden ser datos y no lógica especial?
8. ¿Las 12 técnicas se expresan con el motor universal?
9. ¿Qué falta cerrar ANTES de implementar?
10. ¿Qué puede esperar al benchmark?
