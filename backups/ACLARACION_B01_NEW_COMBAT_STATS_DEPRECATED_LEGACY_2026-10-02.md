# ACLARACIÓN DE AUTORIDAD — B01 / NEW_COMBAT_STATS_V0_1

Fecha: 2026-10-02
Estado: HUMAN_RATIFIED_AUTHORITY_CLARIFICATION
Alcance: documentación / preflight. NO runtime.

## Regla principal

La autoridad vigente de estadísticas de combate es:

`NEW_COMBAT_STATS_V0_1`

El sistema de estadísticas/equipo legacy que todavía existe físicamente en ver76 está:

`DEPRECATED`

y NO puede utilizarse como:

- autoridad;
- fallback;
- bridge de compatibilidad;
- fuente de defaults;
- destino del equipo nuevo;
- tabla para rellenar campos faltantes del contrato nuevo.

## Consumidores legacy explícitamente deprecados

Incluye, entre otros:

- `ataque`;
- `defensa` legacy;
- `daño`;
- `qi_med` usado como semántica vieja;
- slots legacy;
- agregadores legacy de equipo;
- `p.equipado` con shape viejo string-per-slot;
- cualquier traducción equipo nuevo -> stats legacy.

Su presencia en ver76 es evidencia histórica del runtime previo, no una autoridad de diseño vigente.

## Dirección correcta

```text
equipo nuevo
→ NEW_COMBAT_STATS_V0_1
→ binding productivo nuevo de jugador/equipo
→ consumidores productivos nuevos
```

Nunca:

```text
equipo nuevo
→ traducción a ataque/defensa/daño/qi_med
→ agregador legacy
```

## Interpretación correcta de B01

Blocker:

`B01_NEW_COMBAT_EQUIPMENT_CONSUMERS_NOT_CONNECTED`

significa:

> Falta conectar productivamente el nuevo sistema de estadísticas del jugador/equipo.

NO significa:

> Hay que adaptar el catálogo nuevo al agregador legacy.

## Prohibiciones

Para cerrar B01:

1. NO traducir `hp_max`, `evasion`, `precision`, `tenacity`, `control`, etc. a stats legacy.
2. NO crear aliases.
3. NO mantener modelo viejo y nuevo en paralelo.
4. NO reutilizar números legacy de ver76 como relleno automático.
5. NO copiar automáticamente `etapa19b_combat_engine.py` al runtime. Es LAB/provisional y referencia semántica, no implementación productiva autorizada.
6. Si falta un consumidor productivo, declararlo GAP real.
7. El destino es reemplazar/retirar consumidores legacy cuando corresponda, no conservarlos.
8. Saves legacy no condicionan el diseño: clean-slate, sin migración ni compatibilidad.

## Autoridad complementaria ya vigente

La documentación de combate vigente ya declara `NEW_COMBAT_STATS_V0_1` como autoridad y separa explícitamente:

```text
arquitectura/identidad cerrada
≠ balance numérico ready
≠ integración productiva A08
```

Por tanto, cerrar B01 NO autoriza iniciar A08 completo, integrar monstruos o promover runners LAB.

## Próximo trabajo autorizado conceptualmente

Nombre:

`NEW_PLAYER_STATS_EQUIPMENT_PRODUCTIVE_BINDING_PREFLIGHT`

Objetivo:

Auditar exclusivamente cómo establecer el consumidor productivo de:

```text
jugador
+
equipo
+
NEW_COMBAT_STATS_V0_1
```

sin:

- iniciar A08;
- integrar monstruos;
- integrar T1–T4;
- reabrir A07;
- implementar Comercio;
- introducir compatibilidad legacy.

El preflight debe identificar, para cada stat del contrato:

- autoridad de base del jugador;
- fuentes de equipo;
- unidad;
- orden de agregación;
- consumidor runtime;
- readiness productiva;
- GAP si falta autoridad.

Si una estadística base sólo tiene valor en LAB/provisional, marcar GAP. No promoverla ni inferirla automáticamente.
