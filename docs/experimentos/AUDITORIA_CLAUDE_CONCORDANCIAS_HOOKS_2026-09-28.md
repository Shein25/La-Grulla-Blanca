# Protocolo de auditoría — Concordancias 20/20, hooks y técnicas de Arco 1

Fecha: 2026-09-28  
Rama objetivo: `experiment/combat-stat-contract-v0.1`  
Modo obligatorio: **SOLO LECTURA**

## 0. Objetivo

Realizar una segunda auditoría arquitectónica después del cierre de:

- matriz global de 20 Concordancias dirigidas;
- registro universal de estadísticas y propiedades;
- contrato del motor de eventos/efectos;
- contrato numérico de combate;
- 12 técnicas de Arco 1 diseñadas hasta Tierra.

La auditoría debe responder una pregunta central:

> ¿Las 20 Concordancias y las 12 técnicas pueden convivir en un único motor genérico, escalable y determinista, sin hardcodear IDs de técnicas, sin introducir estadísticas inexistentes, sin usar aumentos planos de Concordancia y sin contradicciones entre hooks?

No implementar nada.

---

# 1. Restricciones

Claude debe trabajar en modo auditor.

Prohibido:

- modificar archivos;
- crear commits;
- crear ramas;
- hacer merge;
- editar runtime;
- "arreglar" contradicciones silenciosamente;
- inventar números de balance;
- convertir sugerencias en decisiones aprobadas.

Debe distinguir siempre:

```text
CONTRADICCIÓN
HUECO DE ESPECIFICACIÓN
RIESGO ARQUITECTÓNICO
RIESGO DE BALANCE
MEJORA OPCIONAL
DECISIÓN DEL DISEÑADOR
CORRECTO
```

Severidades:

```text
BLOQUEANTE
ALTO
MEDIO
BAJO
CORRECTO
```

No dar puntaje global.

---

# 2. Orden de autoridad

Usar esta precedencia cuando dos textos difieran:

1. `CONTRATO_CONCORDANCIAS_GLOBALES_V0_1.md`
2. `REGISTRO_UNIVERSAL_ESTADISTICAS_PROPIEDADES_COMBATE_V0_1.md`
3. `CONTRATO_MOTOR_EVENTOS_EFECTOS_V0_1.md`
4. `CONTRATO_COMBATE_ESTADISTICAS_DOT_V0_1.md`
5. `TECNICAS_ARCO1_DISENO_APROBADO_2026-09-28.md`
6. `RESOLUCION_AUDITORIA_COMBATE_2026-09-28.md`
7. `grulla-blanca_ver74.html` sólo como runtime histórico

Si el runtime histórico contradice los contratos nuevos, no marcarlo como defecto del contrato: marcarlo como **riesgo de migración**.

No usar valores/mecánicas viejas de `ver74` para completar silenciosamente un hueco nuevo.

---

# 3. Invariantes que deben comprobarse

## 3.1 Concordancias

Verificar que las 20 relaciones cumplan:

1. relación dirigida ORIGEN→DESTINO;
2. identidad global distinguible;
3. prioridad por contexto;
4. sólo usa hooks registrados;
5. sólo puede modificar `concordance_hooks` expuestos por la técnica;
6. un Eco produce una sola resolución primaria;
7. primer hook compatible gana;
8. sin hook compatible → no transformación y no consumo de Eco;
9. no existe fallback universal de daño;
10. no existe movilidad como sistema;
11. no existen resistencias elementales;
12. no existe ventaja elemental automática;
13. toda magnitud de Concordancia escala porcentualmente/relativamente sobre el hook receptor;
14. no se conceden aumentos absolutos tipo +N daño/+N DEF/+N Precisión/+N Control;
15. una transformación estructural discreta sí puede existir;
16. la Concordancia no debe multiplicar la estadística total del actor cuando corresponde escalar sólo la aportación del hook;
17. la Concordancia no aumenta target cap de AOE;
18. no debe introducir IDs de técnicas en el resolver.

## 3.2 Motor

Verificar compatibilidad con:

- Event Bus;
- Effect Engine;
- State Engine;
- `ActionContext`;
- `DamagePacket`;
- `ImpactResult`;
- `ControlAttempt`;
- `EffectDefinition`;
- frecuencias;
- roles direccionales;
- `reaction_depth`;
- zonas;
- estados persistentes;
- recursos internos;
- `CONTAINED_TRIGGER`.

## 3.3 Estadísticas

Comprobar que ninguna Concordancia o técnica requiera accidentalmente:

```text
MOBILITY
MOVEMENT_SPEED
MOBILITY_REDUCTION
SLOW
FIRE_RESISTANCE
METAL_RESISTANCE
WATER_RESISTANCE
EARTH_RESISTANCE
WIND_RESISTANCE
PHYSICAL_DEFENSE separada
MAGIC_DEFENSE separada
ELEMENTAL_DEFENSE separada
ATTACK_SPEED
CAST_SPEED
PASSIVE_QI_REGEN
QI_REGEN_PER_TURN
GENERIC_ELEMENTAL_ADVANTAGE
```

---

# 4. Auditoría exhaustiva de las 20 relaciones

Auditar una por una:

## Fuego como origen
- Fuego→Tierra · Cimiento Cocido
- Fuego→Metal · Forja Ardiente
- Fuego→Agua · Presurización
- Fuego→Viento · Corriente Ascendente

## Metal como origen
- Metal→Fuego · Chispa de Ignición
- Metal→Agua · Cauce Tallado
- Metal→Tierra · Anclaje de Hierro
- Metal→Viento · Filo en la Corriente

## Agua como origen
- Agua→Fuego · Vapor Súbito
- Agua→Metal · Temple de Agua
- Agua→Tierra · Erosión / Sedimentación
- Agua→Viento · Velo de Niebla

## Tierra como origen
- Tierra→Fuego · Corazón de Magma
- Tierra→Metal · Forja Asentada
- Tierra→Agua · Cauce Represado
- Tierra→Viento · Tormenta de Polvo

## Viento como origen
- Viento→Fuego · Avivamiento
- Viento→Metal · Filo Propulsado
- Viento→Agua · Corriente Ligera
- Viento→Tierra · Golpe del Vendaval

Para cada relación entregar:

| Campo | Auditoría |
|---|---|
| Identidad | ¿es distinta y coherente? |
| OFFENSIVE | hooks válidos y orden |
| DEFENSIVE | hooks válidos y orden |
| CONTROL | hooks válidos y orden |
| UTILITY | hooks válidos y orden |
| Escalado | ¿porcentual/relativo? |
| Fallback | ¿evita fallback arbitrario? |
| Hardcode | ¿requiere ID concreto? |
| Cobertura futura | ¿sirve para contenido no existente hoy? |
| Colisiones | ¿se solapa peligrosamente con otra relación? |
| Resultado | CORRECTO / hallazgo |

No exigir que todas las relaciones tengan receptor actual en Arco 1.

---

# 5. Auditoría de manifestaciones estructurales aprobadas

Revisar específicamente:

## 5.1 Tierra→Fuego · Núcleo de Magma

Debe comprobarse:

- sólo se usa vía `CONTAINED_TRIGGER`;
- no es DOT;
- no es Quemadura;
- no da daño por turno;
- no modifica retroactivamente el impacto creador;
- se consume al detonarse;
- detonación unitarget y AOE respetan el conjunto de blancos existente;
- la onda AOE no añade objetivos fuera de la ejecución;
- no existe doble escalado;
- magnitud futura será relativa/porcentual;
- el resolver no pregunta "¿es Núcleo de Magma?".

## 5.2 Tierra→Metal · Placa Fundacional

Debe comprobarse:

- una Placa protege el primer impacto sin consumirse;
- pasa a REFORZADA;
- el siguiente impacto usa potencia porcentualmente reforzada;
- después se consume;
- `once_per_activation`;
- no existe +N DEF fijo;
- escala con la DEF propia futura de la Placa;
- no crea una Placa ficticia;
- no puede reforzarse infinitamente.

## 5.3 Tierra→Agua · Embalse

Debe comprobarse:

- almacena restauración de Absorción que habría sido excedente;
- no es segunda barrera;
- no cura Vida;
- libera sobre el mismo pool cuando vuelve a existir espacio;
- capacidad/liberación son relativas;
- ciclo de vida ligado a la activación defensiva;
- no produce triggers ofensivos accidentales.

## 5.4 Tierra→Viento · Nube Residual

Debe comprobarse:

- usa ZONE/ZONE_DURATION;
- no introduce movilidad;
- no añade blancos al AOE original;
- sólo aplica efectos reales declarados;
- duración/magnitud escalan relativamente;
- no inventa daño si no existe hook compatible.

---

# 6. Auditoría de las 12 técnicas actuales

Auditar:

## Fuego
1. Palma Ardiente
2. Respiración del Cuerpo-Horno
3. Círculo de las Cien Ascuas

## Metal
4. Destello de Plata
5. Armadura de Plata
6. Lluvia de Filos

## Agua
7. Latigazo de Marea
8. Espejo de Luna
9. Marea de las Ocho Orillas

## Tierra
10. Golpe de Montaña
11. Piel de Cobre
12. Temblor de Montaña

Para cada técnica producir una ficha:

```text
TÉCNICA:
ROL:
TAGS:
MECHANICAL_HOOKS BASE:
MECHANICAL_HOOKS POR RAMA:
CONCORDANCE_HOOKS BASE:
CONCORDANCE_HOOKS DESBLOQUEADOS POR RAMA:
RECURSOS/ESTADOS:
TRIGGERS:
FRECUENCIAS:
```

Después evaluar sus cuatro posibles Ecos entrantes.

Ejemplo de formato:

| Eco entrante | Relación | Primer concordance_hook compatible | Resultado conceptual | ¿consume Eco? | ¿requiere rama? | Riesgo |
|---|---|---|---|---|---|---|

Regla crítica:

> No asumir que todo `mechanical_hook` está expuesto a Concordancias. Si el documento de técnica todavía no declara `concordance_hooks`, marcarlo como hueco a cerrar, no inventarlos como hecho.

---

# 7. Auditoría de ramas

Comprobar que las ramas:

- añaden/modifican hooks como datos;
- pueden desbloquear un `concordance_hook` sin cambiar el resolver;
- no contienen una Concordancia hardcodeada por nombre de rama;
- no requieren `if technique_id` central;
- no dependen de valores absolutos legacy de Concordancia;
- mantienen independencia entre Tramos;
- permiten sinergias acumulativas sin dependencias trampa;
- una ruta completa puede potenciar un hook ya existente, pero no debe alterar arbitrariamente la identidad elemental global.

Identificar cualquier texto legacy como:

```text
+1 DEF
+1 Arraigo
+N puntos de Concordancia
```

y verificar que esté claramente superado por la matriz global.

---

# 8. AOE y Concordancias

Comprobar:

- todos los hostiles válidos;
- sin target cap;
- sin split de daño;
- impacto separado por objetivo;
- 65% unitarget antes de DEF/redondeo;
- Concordancia actúa coherentemente sobre la ejecución completa salvo regla explícita;
- detonaciones/propagaciones secundarias no vuelven a seleccionar enemigos arbitrariamente;
- `once_per_action` y `once_per_target_per_action` no se confunden;
- orden determinista de objetivos;
- no doble conteo de Robo de Vida;
- no doble Eco por múltiples impactos.

---

# 9. Escalado futuro

Probar conceptualmente valores de órdenes de magnitud diferentes.

No calcular balance; verificar arquitectura.

Casos:

### S-1
Técnica Arco 1: daño base pequeño.

### S-2
Técnica futura: daño base 200+.

La misma Concordancia debe seguir siendo relevante sin cambiar código ni usar +N fijo.

### S-3
Defensa con DEF de Placa mucho mayor que Arco 1.

Placa Fundacional debe escalar proporcionalmente.

### S-4
Barrera futura con Absorción muy alta.

Embalse debe escalar respecto del propio efecto, no mediante una cantidad absoluta.

### S-5
Técnica con Precisión propia alta.

Una Concordancia debe escalar la contribución del hook, no la Precisión total del actor.

---

# 10. Casos adversariales obligatorios

## A · Hook múltiple

Una técnica expone:

```text
CRIT_CHANCE
PRECISION
PROPAGATION
```

La relación prioriza en ese orden.

Confirmar que sólo se aplica `CRIT_CHANCE`.

## B · Sin hook

Existe Eco válido por elemento pero la técnica no expone ningún hook compatible.

Resultado esperado:

```text
acción normal
Eco conservado
sin fallback
```

## C · Rama desbloquea canal

La técnica base no expone DOT.

Una rama añade:

```text
AFFLICTION_APPLICATION
DOT_POTENCY
PERSISTENCE
```

Una Concordancia que antes no podía actuar ahora debe poder hacerlo sólo por datos.

## D · Tierra→Fuego directa

Fuego directo sin DOT.

Debe poder usar `CONTAINED_TRIGGER` si la técnica lo expone y crear Núcleo de Magma sin hardcode central.

## E · Tierra→Fuego persistente

La misma técnica con rama DOT.

Debe priorizar PERSISTENCE/DOT antes que CONTAINED_TRIGGER.

No deben ocurrir simultáneamente ambos resultados por un solo Eco.

## F · Tierra→Metal futura

Defensa Metal con stacks distintos de Placas.

La relación debe poder usar FORTIFICATION/STACKABLE_STATE sin saber qué es Armadura de Plata.

## G · Agua defensiva sin Reflujo

Defensa Agua con Absorción pero sin restauración.

Tierra→Agua no debe inventar Embalse si no existe canal compatible.

## H · Viento AOE sin zona

AOE Viento sin ZONE/ZONE_DURATION.

Tierra→Viento no debe inventar Nube Residual si el contenido no la expone.

## I · Escalado alto

Repetir una relación con magnitudes 100× mayores.

No debe aparecer ningún valor plano fijo de Concordancia.

## J · Stat total vs hook

Un actor tiene Precisión total alta por múltiples fuentes; la técnica sólo aporta una fracción.

Una Concordancia de Precisión debe escalar la aportación de la técnica/hook, no la estadística total.

## K · AOE + Núcleo

Un objetivo de una AOE tiene Núcleo de Magma.

La detonación completa ocurre en el marcado; la propagación secundaria sólo alcanza al conjunto ya válido para esa ejecución y nunca descubre objetivos nuevos.

## L · Dos efectos estructurales

Una técnica expone varios hooks estructurales compatibles.

Confirmar que un Eco sigue generando una sola resolución primaria.

---

# 11. Validación del catálogo de hooks

Comparar TODOS los hooks mencionados en:

- matriz de Concordancias;
- técnicas;
- motor;

contra el registro universal.

Entregar tres listas:

```text
A. hooks registrados y usados correctamente
B. hooks usados pero no registrados
C. hooks registrados pero semánticamente duplicados/redundantes
```

Prestar especial atención a:

- `CONTAINED_TRIGGER`;
- `FORTIFICATION`;
- `INTENSITY`;
- `EXECUTION`;
- `REACTIVE_RESPONSE`;
- `AREA_EFFICIENCY`;
- `PROPAGATION`;
- `ZONE`;
- `ZONE_DURATION`;
- `DEBUFF_DURATION`;
- `STACKABLE_STATE`;
- `INTERNAL_RESOURCE`.

---

# 12. Validación de nombres y semántica

Buscar colisiones donde dos hooks parezcan significar lo mismo pero se resuelvan distinto.

Ejemplos a revisar:

- `PERSISTENCE` vs `DOT_DURATION` vs `ZONE_DURATION`;
- `FORTIFICATION` vs `DEF_GRANTED` vs `ABSORPTION`;
- `INTENSITY` vs `DOT_POTENCY` vs `DIRECT_DAMAGE`;
- `EXECUTION` como hook semántico vs ejecución normal de ActionContext;
- `REACTIVE_RESPONSE` como familia vs Reflect/Retaliation;
- `AREA_EFFICIENCY` vs `PROPAGATION`.

Si la distinción es válida, explicarla.
Si no está suficientemente definida, marcar hueco.

---

# 13. Preguntas finales obligatorias

Responder explícitamente:

1. ¿Las 20 relaciones poseen identidades suficientemente distintas?
2. ¿Hay alguna relación que inevitablemente caiga en un fallback genérico?
3. ¿Todos los hooks utilizados existen en el registro universal?
4. ¿Hay hooks demasiado vagos para implementarse sin hardcode?
5. ¿Las 12 técnicas pueden declarar sus `concordance_hooks` como datos?
6. ¿Alguna rama obliga a tocar el resolver?
7. ¿Núcleo de Magma es expresable sin ID hardcodeado?
8. ¿Placa Fundacional es expresable sin ID hardcodeado?
9. ¿Embalse es expresable sin ID hardcodeado?
10. ¿Nube Residual es expresable sin ID hardcodeado?
11. ¿El escalado porcentual está suficientemente cerrado para Arcos futuros?
12. ¿Alguna Concordancia multiplica por error una stat total en vez de la contribución receptora?
13. ¿Hay alguna interacción que pueda aplicar dos resoluciones con un solo Eco?
14. ¿AOE + Concordancias conserva todos los invariantes del contrato?
15. ¿Qué correcciones son obligatorias antes de diseñar las tres técnicas de Viento?
16. ¿Qué puntos pueden esperar al benchmark numérico?
17. ¿Qué puntos requieren una decisión explícita del diseñador?

---

# 14. Formato de entrega

## A. Resumen ejecutivo

Máximo 20 hallazgos principales.

## B. Contradicciones verificadas

Tabla:

| ID | Severidad | Archivos | Hallazgo | Evidencia | Corrección mínima |

## C. Huecos de contrato

Tabla separada.

## D. Matriz 20/20

Una fila por relación.

## E. Matriz 12 técnicas × 4 Ecos entrantes

No omitir ninguna técnica.

## F. Hooks

Listas A/B/C de §11.

## G. Casos adversariales A–L

PASS / FAIL / INDETERMINADO con explicación.

## H. Decisiones del diseñador

Sólo decisiones verdaderamente necesarias; no convertir balance en bloqueo arquitectónico.

## I. Respuestas 1–17

Una por una.

## J. Conclusión

Separar:

```text
BLOQUEANTES ANTES DE SEGUIR DISEÑANDO
CORRECCIONES ALTAS
PUEDE ESPERAR A BENCHMARK
CORRECTO / SIN CAMBIOS
```

No implementar las correcciones.
