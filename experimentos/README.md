# Laboratorio de experimentos

Esta carpeta contiene prototipos y bancos de pruebas **aislados de producción**.

Los experimentos se agrupan primero por dominio funcional para evitar mezclar IA de NPCs con IA de monstruos.

## Estructura actual

```text
experimentos/
├── npc/
│   ├── utility-ai/
│   ├── goap/
│   ├── memoria/
│   ├── scheduler/
│   ├── execution/
│   └── integraciones/
├── monstruos/
│   └── monster-ai/
├── backups/
└── README.md
```

## NPC

`experimentos/npc/` contiene los experimentos destinados al comportamiento de NPCs fuera del sistema específico de combate de monstruos:

- Utility AI;
- GOAP;
- memoria, relaciones y decisión;
- lifecycle / scheduler;
- executor y replanning;
- Autonomous NPC Loop e integraciones relacionadas.

Cada motor conserva su propia subcarpeta y versión. Agruparlos bajo `npc/` **no implica que todos los NPC deban usar todos los motores**.

## Monstruos

`experimentos/monstruos/` contiene los experimentos específicos de monstruos.

Actualmente incluye:

- `monster-ai/monster-combat-ai-v0.1`.

Las futuras familias específicas de monstruos, como Adaptive Ecology cuando exista como snapshot Git real, deberán incorporarse aquí en su propia subcarpeta. No crear carpetas vacías por adelantado.

## Backups

`experimentos/backups/` permanece en la raíz porque documenta la continuidad del laboratorio completo y no pertenece exclusivamente a NPCs ni a monstruos.

## Migración de rutas

La reorganización sólo cambia ubicación. Los snapshots internos no se modifican.

| Ruta anterior | Ruta nueva |
| --- | --- |
| `experimentos/utility-ai/` | `experimentos/npc/utility-ai/` |
| `experimentos/goap/` | `experimentos/npc/goap/` |
| `experimentos/memoria/` | `experimentos/npc/memoria/` |
| `experimentos/scheduler/` | `experimentos/npc/scheduler/` |
| `experimentos/execution/` | `experimentos/npc/execution/` |
| `experimentos/integraciones/` | `experimentos/npc/integraciones/` |
| `experimentos/monster-ai/` | `experimentos/monstruos/monster-ai/` |

Los documentos históricos en `backups/` pueden mencionar las rutas anteriores; deben interpretarse según esta tabla y no reescribirse retroactivamente.

## Auditorías externas

Los informes de prueba deben identificar al agente auditor tanto en el nombre del archivo como en la cabecera.

La cabecera debe incluir como mínimo:

- agente auditor;
- modelo/versión si se conoce;
- fecha;
- rama auditada;
- HEAD exacto;
- tipo de revisión.

## Aislamiento

Nada de `experimentos/` se considera producción por existir aquí.

Para integrar un resultado experimental al juego se requiere:

1. versión congelada;
2. tests;
3. auditoría independiente;
4. contrato de integración;
5. revisión antes de merge.

## Continuidad entre chats

Backup maestro del estado experimental:

`experimentos/backups/HANDOFF_MAESTRO_EXPERIMENTOS_2026-09-24.md`

Prompt corto para abrir un chat nuevo dedicado al laboratorio:

`experimentos/backups/PROMPT_NUEVO_CHAT_EXPERIMENTOS_2026-09-24.md`
