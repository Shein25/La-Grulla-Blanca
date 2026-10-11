# Cierre humano V77: balance Metal / Sombra y cambio de frente a AOE + Concordancias

**Fecha:** 2026-10-10. **Autoridad:** mensaje humano «Bien entonces guarda el cambio de balance, cerramos el jefe este, pasamos a testear como se comporta el aoe usando concordancia, ya sea con otra aoe de otra rama, usando otra técnica o usando dos veces la aoe de la misma rama».

## Balance de diseño cerrado, sin patch runtime

**Metal / Sentencia del Filo Celestial:** se reafirma como cifra **V76 B seleccionada** (registrada previamente): 65% del daño original de apertura, 65% del remate, penetración adicional +10pp, una hemorragia potencia2 ×2 activaciones, +30 precisión, coste16 Qi, una Ulti máxima por combate. El jugador decide cuándo activar, **ronda 4 no es obligación**. Ficha vigente: `experimentos/balance_nuevo/handoffs/V76_SENTENCIA_METAL_PUNTO_INTERMEDIO_2026-10-10/SENTENCIA_METAL_BALANCE_SELECCIONADO_V76.json`. V67 Metal queda como historia, V67 Viento intacta, demás 24 Ultis inalteradas.

**Sombra Ahogada del Estanque (`sombra_ahogada`):** el autor cierra el rebalance T0 **numérico de diseño** del **élite único LianQi III**, no de un guardián AOE. Ficha V72: HP110, DEF1, Velo CD4 con veneno `1d2+2` durante 2 pulsos, Espejo de Remanso 8 absorbente tras primer golpe real >=16 HP. Otros stats V72 sin cambios. **No volver a reequilibrarla sobre las pruebas de Ultis/Concordancia antes de identificar la causa**. El catálogo V3 marca `V77_HUMAN_CLOSED_NUMERIC_DESIGN_LIII_HP110__NOT_RUNTIME_READY`. El histórico T0 HP51 queda archivado, no se sobreescribe.

**Cierre de balance ≠ cierre runtime:** pendientes integración HTML, eventos de DOT/escudo, manual/post-manual real, 1vN, Concordancias numéricas, equivalencia de Ultis y SAVE/LOAD. No declarar `READY` productivo. No tocar cinco guardianes numéricos ni `main`, merge, HTML, `ROOMS.exits`, NPC, economía o spawns. Inventario canónico 31 identidades.

## Nueva orden de pruebas — tres secuencias

1. AOE de raíz A → AOE de raíz B: comprobar Eco dirigido, hook receptor, pago Qi una vez por acción, 1/2/3 blancos.
2. AOE → otra técnica: en especial unitarget de otra raíz y control negativo misma raíz; después añadir defensiva/control cuando el puente esté validado.
3. AOE → misma AOE por segunda vez: prueba de sustitución de Eco, NO Concordancia autoelemental, dos pagos reales de Qi, estados de DOT/reaplicación por fuente sin duplicar ticks.

**Base normativa:** `docs/experimentos/CONTRATO_CONCORDANCIAS_GLOBALES_V0_1.md`; `docs/experimentos/MAPEO_HOOKS_TECNICAS_ARCO1_2026-09-29.md`; `docs/experimentos/RESOLUCION_AUDITORIA_CONCORDANCIAS_HOOKS_2026-09-29.md`; PRE/POST_AOE en `experimentos/balance_nuevo/handoffs/V67_CIERRE_GUARDIANES_ULTIS_2026-10-10/PENDIENTES_LIII_Y_AOE_POST_MANUAL.md`.

El primer laboratorio V77 evalúa **selección de hooks y física AOE**; no fabrica escalas de Concordancia ni simula victoria multiblanco completa. Datos en el dictamen V77 hermano y ZIP reproducible del chat.
