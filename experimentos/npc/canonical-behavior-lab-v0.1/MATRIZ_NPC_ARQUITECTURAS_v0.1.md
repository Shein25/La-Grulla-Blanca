# Matriz NPC — baselines de arquitectura v0.1

## Estado

Los 32 NPC canónicos de `NPC_DEF` ver74 poseen al menos un baseline de comportamiento reproducible.

Esto **no asigna todavía arquitectura definitiva**. La columna "baseline probado" describe qué motor/capa se utilizó para observar el comportamiento actual.

| NPC | Categoría | Baseline probado | Resultado principal |
|---|---|---|---|
| Ji Xueying | autoridad | FSM mínima/eventos | ANCLADA; Consejo/M17 sin movimiento |
| Qiao Ren | autoridad | Autonomous Loop (Utility+GOAP+Execution) | deber/coord. funcionan; autorización M17 ausente |
| Wei Jian | autoridad | Behavior Tree | crisis preempta entrenamiento; combate/gates fuera |
| Song Rui | autoridad | Utility+GOAP+diálogo | R3 funciona; conocimiento extendido/archivo incompletos |
| Lan Meihua | autoridad | Utility+GOAP | deber médico simbólico; falta triage/tratamiento |
| Duan Shibo | autoridad | Utility+GOAP | deber Recursos simbólico; falta logística material |
| He Zhen | autoridad | Utility+GOAP+diálogo | deber Formaciones simbólico; falta red de formaciones |
| Shen Baojun | intermedio | FSM mínima/eventos | M03 entrenamiento; no inventa M16 |
| Madre Wen | intermedio | FSM mínima/eventos | continuidad; no inventa frente M16 |
| Tao Ming | intermedio | FSM | ROUTINE ↔ EMERGENCY en M16 |
| Jiang Rui | intermedio | FSM + BT + Utility | superficie de decisión contextual medible |
| Su Lian | intermedio | Behavior Tree | M16 Jardines preempta tutorial |
| Chen Bo | intermedio | Behavior Tree | pacientes preemptan examen |
| Yao Fen | intermedio | Behavior Tree | Medicina preempta lección de Alquimia |
| Gao Shun | funcional | FSM + Behavior Tree | guardia/patrulla y preempción comparadas |
| Feng Zhi | funcional | FSM mínima/eventos | rutina Disciplina; M16 no inventado |
| Ma Qiren | funcional | Behavior Tree | distribución M16 preempta stock |
| Pei Luo | funcional | FSM + Behavior Tree | rutina equivalente; crisis muestra diferencia estructural |
| Lu Cheng | funcional | FSM anclada | reparación M16 sin movimiento |
| Ning Cai | funcional | FSM anclada | producción emergencia sin movimiento |
| Wen Tao | funcional | Behavior Tree | nodo crítico preempta reparación rutinaria |
| Yu Shun | funcional | FSM mínima/eventos | M09 copias; M16 no inventado |
| Ma Gu | funcional | FSM | apoya RECURSOS sin inventar séptimo frente |
| Ren Bo | funcional | Behavior Tree | RUTAS preempta patrulla |
| Xu An | funcional | Behavior Tree | SAUCES preempta rutina comunitaria |
| Mei Shufen | funcional | FSM con guardia narrativa | Sauces DAÑADO no implica muerte automática |
| Lin Yue | compañero | Memory→Relations→Utility→GOAP | memoria social cambia decisión y plan |
| Han Qiao | compañero | Utility+GOAP | ayuda ordinaria vs deber logístico M16 |
| Zhao Wen | compañero | diálogo Utility | DESCONOCIDO nunca se revela |
| Mei Lian | compañero | Utility+GOAP | SAUCES/MEDICINA colapsan: falta identidad de frente |
| Guo Chen | compañero | Utility+GOAP + guardia | Segunda Rama no puede entrar por duty genérico |
| Luo Yan | compañero | diálogo Utility | R5 y LIBERAR/CUSTODIAR no representados |

## Gaps transversales antes de producción

1. `KNOWLEDGE_SCHEMA_R1_TO_R10`: Utility v0.1.1 sólo modela R1-R3.
2. Navegación física real por rooms, rutas y gates.
3. Executor de combate/seguridad para intents marciales.
4. `RESOURCE_ALLOCATION_AND_LOGISTICS`: inventario, cantidades, reservas, carros y destinos.
5. `ARCHIVE_PROTECTION_AND_CATALOG_STATE`: documentos, daño, traslado y catalogación.
6. `MEDICAL_TRIAGE_AND_TREATMENT_STATE`: pacientes, gravedad, aflicciones y tratamiento.
7. `FORMATION_NETWORK_STATE_AND_REPAIR`: nodos, barreras, energía e integridad.
8. Asignación de frentes M16 y responsables disponibles.
9. Permisos institucionales como `ARCHIVO_RESTRINGIDO_PERMISSION` y autorización de `NUCLEO_PROFUNDO`.
10. Guardias de decisiones irreversibles para impedir que `FULFILL_DUTY` absorba decisiones narrativas.
11. Acciones sociales Utility todavía no mapeadas a GOAP, por ejemplo `hablar_jugador`.
12. Estado de mundo de dominio para que los intents simbólicos produzcan consecuencias reales.

## Conteo de pruebas confirmadas

Baselines de comportamiento:

```text
Autoridades    88/88
Intermedios    74/74
Funcionales    89/89
Compañeros     85/85
TOTAL         336/336 PASS
```

Suite canónica transversal adicional:

```text
15/15 PASS sobre NPC_DEF completo
32/32 NPC cubiertos
```

## Interpretación

Un PASS significa que el baseline cumple el contrato experimental y respeta el canon usado.

No significa que el NPC esté listo para producción. Los gaps anteriores indican qué adaptadores/capas de dominio faltan antes de integrar comportamiento autónomo real.

## Próximo bloque

Monstruos: reutilizar el mismo método de laboratorio, pero partiendo del Monster Combat AI ya auditado y separando decisión de combate, navegación/aggro, aparición, persecución y consecuencias del mundo.
