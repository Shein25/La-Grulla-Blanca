# Resolución post-auditoría — Concordancias, hooks y técnicas

Fecha: 2026-09-29  
Rama: experiment/combat-stat-contract-v0.1  
Estado: **RESOLUCIONES ARQUITECTÓNICAS APLICADAS / SIN RUNTIME**

## 0. Contexto

Se contrastaron tres auditorías externas independientes sobre el mismo HEAD de auditoría: Kimi, DeepSeek y Claude.

La resolución se basó en coincidencias verificadas contra la rama y en revisión directa de los contratos.

No se modificó runtime.

---

# 1. Correcciones documentales aplicadas

- retirado MOBILITY_REDUCTION del catálogo del Motor;
- retiradas familias de Control ligadas a movilidad: ROOT y MOVEMENT_DENIAL;
- sincronizados CONTAINED_TRIGGER, ZONE, ZONE_DURATION y DEBUFF_DURATION;
- reemplazado el ejemplo legacy con STRUCTURAL_MAGNITUDE / IMPACT;
- reparadas todas las listas de prioridad corrompidas de la matriz;
- secciones antiguas de Concordancias del contrato numérico marcadas LEGACY;
- mapeos antiguos de Piel de Cobre y Temblor marcados LEGACY / NO CANÓNICOS;
- retirado lenguaje de movilidad de la identidad mecánica de Viento.

---

# 2. Decisiones arquitectónicas cerradas

## D-01 · Eco no consumido vs Eco sustituido

~~~text
sin hook compatible
→ no consume Eco por Concordancia
~~~

pero:

~~~text
si la técnica pura completa una ejecución válida
→ genera su Eco
→ el Eco nuevo sustituye el anterior
~~~

NO CONSUMIDO y NO SUSTITUIDO son conceptos diferentes.

## D-02 · DIRECT_DAMAGE

DIRECT_DAMAGE puede existir en mechanical_hooks[] sin estar en concordance_hooks[].

Sólo las técnicas que lo exponen explícitamente permiten que una Concordancia resuelva sobre daño directo.

## D-03 · Duraciones porcentuales

~~~text
duration × (1 + concordance_scale)
→ ROUND_HALF_UP
→ snapshot
~~~

No existe un mínimo artificial de +1 turno.

## D-04 · EXECUTION

EXECUTION queda retirado temporalmente de todas las prioridades de Concordancia.

Permanece registrado como familia mecánica hasta que exista una semántica operacional única.

## D-05 · Movilidad

No existen como sistema de combate:

~~~text
MOBILITY
MOVEMENT_SPEED
MOBILITY_REDUCTION
SLOW
ROOT
MOVEMENT_DENIAL
~~~

## D-06 · Roles

role_primary sólo admite:

~~~text
OFFENSIVE
DEFENSIVE
CONTROL
UTILITY
~~~

Latigazo de Marea queda role_primary = CONTROL.

HYBRID describe composición elemental, no rol funcional.

## D-07 · QI_COST_PERCENT de Concordancia

~~~text
DECLARE_ACTION
→ CONCORDANCE_PREVIEW
→ coste normal
→ capa local de Concordancia
→ piso
→ redondeo
→ validación/pago
→ COMMIT_CONCORDANCE
~~~

No modifica permanentemente el pool global del actor.

---

# 3. Clases operacionales de hook

Se adoptan:

~~~text
SCALAR
PARAMETRIC
STRUCTURAL
~~~

SCALAR escala una contribución propia del receptor:

~~~text
receiver_value × (1 + concordance_scale)
~~~

Nunca escala la stat total del actor.

PARAMETRIC debe declarar scale_target.

STRUCTURAL debe declarar transformation_rule.

Un hook STRUCTURAL sin transformación registrada para esa relación/contexto no se considera compatible y el resolver continúa con la siguiente prioridad.

---

# 4. Hooks antes ambiguos

Se definieron operacionalmente PERSISTENCE, INTENSITY, FORTIFICATION, REACTIVE_RESPONSE, STACKABLE_STATE, INTERNAL_RESOURCE, AFFLICTION_APPLICATION, PROPAGATION, AREA_EFFICIENCY y DAMAGE_PORTION.

AREA_EFFICIENCY:

- sólo AOE;
- modifica magnitud ofensiva local;
- se aplica antes de AOE_SINGLE_TARGET_SCALAR;
- no aumenta blancos;
- no modifica debuffs, Control, duración ni stacks;
- no es PROPAGATION.

---

# 5. Manifestaciones estructurales

Se creó un schema universal ConcordanceManifestation con campos para relación, hook receptor, clase, contexto, dueño, alcance, duración, trigger, condiciones, frecuencia, escala, transformación, consumo, operaciones, flags, cleanup y snapshot.

## Núcleo de Magma

- Tierra→Fuego + CONTAINED_TRIGGER;
- se crea sólo sobre impacto conectado;
- AOE puede crear uno por objetivo conectado con una sola resolución primaria;
- mismo source debe detonarlo;
- paquete secundario no critica, usa DEF/Absorción, no Penetración ni Robo de Vida;
- no recibe el 0.65 AOE por defecto;
- magnitud almacenada queda snapshot y no vuelve a escalar con el detonador.

## Placa Fundacional

- Tierra→Metal + FORTIFICATION;
- primer impacto directo válido: protege, no consume, pasa a REFORZADA;
- segundo: DEF propia × escala relativa;
- la transformación termina;
- si otra regla evita el consumo, la Placa sobrevive como NORMAL, nunca como REFORZADA infinita.

## Embalse

- Tierra→Agua + ABSORPTION_RESTORE;
- usa overflow_restore de AbsorptionRestoreResult;
- almacena excedente;
- libera tras una pérdida de Absorción para paquetes futuros;
- no retroabsorbe el paquete actual;
- no es segunda barrera;
- no sobrevive a ruptura/reconstrucción de la instancia original.

## Nube Residual

- Tierra→Viento + ZONE/ZONE_DURATION;
- owner ROOM;
- no requiere posiciones internas;
- por defecto usa el target_set congelado de la acción creadora;
- no incorpora nuevos enemigos;
- no crea daño sin canal declarado.

---

# 6. AOE

Una Concordancia se resuelve una vez por ActionContext.

Después puede producir efectos per_target, sin volver a resolver el Eco.

~~~text
PROPAGATION
AREA_EFFICIENCY
ZONE
paquetes secundarios
~~~

no descubren blancos fuera del target_set congelado salvo futura excepción global explícita.

---

# 7. Mapeo de las 12 técnicas

Fuente canónica:

docs/experimentos/MAPEO_HOOKS_TECNICAS_ARCO1_2026-09-29.md

Quedaron declarados:

- 12/12 role_primary;
- 12/12 mechanical_hooks[];
- 12/12 concordance_hooks[];
- hooks condicionales por rama;
- receptor de Núcleo en Palma/Círculo;
- receptor de Placa Fundacional en Armadura;
- receptor de Embalse en Espejo;
- Piel deja de exponer STACKABLE_STATE para evitar el legacy +1 Arraigo.

La mini-reauditoría 12 × 4 produce 48 resultados deterministas.

---

# 8. Pendiente no arquitectónico

Puede esperar a benchmark:

- valores finales de concordance_scale;
- valor final de 0.65 AOE;
- porcentajes de Núcleo/Placa/Embalse/Nube;
- límites de Robo de Vida;
- piso final de coste de Qi;
- números de balance de las 12 técnicas.

---

# 9. Próximo paso

Antes de runtime:

1. verificación mecánica de consistencia de documentos;
2. diseñar las 3 técnicas de Viento usando este contrato desde el inicio;
3. reauditar cobertura 20/20 con 15 técnicas;
4. benchmark numérico;
5. sólo después autorizar implementación.
