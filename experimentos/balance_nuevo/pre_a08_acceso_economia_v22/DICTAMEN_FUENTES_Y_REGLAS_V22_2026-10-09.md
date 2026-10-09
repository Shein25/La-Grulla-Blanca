# PRE-A08 V22 — fuentes de equipo y reglas económicas (auditoría documental)
**Estado: propuesta / no canon / no freeze.** Continúa V21; no se repiten V17–V21.

## Evidencia verificada
- Catálogo `equipment_arc1_catalog.json` blob `3ac868a399118845b91da6ccd884633e7ac2b496`: 68 piezas, 21 LII, 8 asociadas a M04, 9 a M05, 4 a M06. Todas LII `OPTIONAL`.
- 14 LII tienen precio nominal en piedras, 7 no: `aguja_acero_frio`, `sobretunica_patrulla`, `brazales_pulso_firme`, `fajin_patrulla`, `anillo_sello_hierro`, `pulsera_tension_meridiana`, `calzas_guardia_externa`.
- V21 verificó que el HTML ver74 en esta rama tiene `QUESTS={}`, `CATALOGO=[]`, y comandos de comercio placeholders. Los NPC nominales no prueban inventario o venta. No extrapolar a otra versión.
- `alchemy_consumables_v0.1/ALCHEMY_CRAFTING_ECONOMY_POLICY_V0_1.json` blob `111b2839aafea3fe49905f343d39a3d680eede05`: propuesta de craft sin gasto de piedras ni Contribución; consume materiales, 2 acciones, fallo consume ingredientes, reventa sin equilibrar, antídotos sin oferta rutinaria confirmada.
- Decisión humana vigente: **Contribución NO gastable**. El `contribution_plan` del catálogo describe recompensas/estatus, NO una moneda para convertir.

## Matriz de resolución por fuente (NO gates aprobados)
| Grupo | Piezas | Condición documentada | Lo que falta verificar |
|---|---:|---|---|
| M04 | 8 | Etiquetas de catálogo M04, fuentes NPC y permisos | M04 ejecutable, recompensa real, inventario, acceso a Jiang Rui / Lu Cheng / Ning Cai |
| M05 | 9 | Etiquetas M05; Ning Cai y colectivos de mercado/Sauces | M05 ejecutable, comerciantes reales, stock, condición HUESPED_SAUCES, colmillo legítimo |
| M06 | 4 | Etiquetas M06; Lu Cheng, Chen Bo, Lan Meihua | M06 ejecutable, permisos efectivos, stock, acceso a los tres NPC |

## Propuestas de diseño, pendientes de aprobación
1. Separar *mérito/reputación/permiso* de *piedras espirituales*. Contribución no se descuenta jamás.
2. Mantener los 14 precios de piedras solo como parámetros de ensayo, no precios canónicos. Los siete restantes quedan `PRECIO_PENDIENTE`; no convertir su precio legacy de Contribución.
3. Sin nuevas misiones, NPC, tiendas, salas ni permisos. Las etiquetas del catálogo no se transforman automáticamente en puertas de acceso.
4. No ofrecer equipo de catálogo en tests como «obtenible» hasta que una fuente ejecutable lo entregue. Usar Prólogo/M03 como referencias de diseño, explícitamente no adquisición verificada.
5. Reventa: probar sensibilidad 25%, 30%, 40% solo después de definir precio de compra y suministro. El precio de reventa nunca puede superar al de compra; inspeccionar también ciclos con materiales, crafting y recompensas.
6. Drops de monstruos y extracción de cadáveres son fuentes distintas. Un material de requisición narrativo no es automáticamente un ID de drop, y `colmillo_lobo_legitimo` no está acreditado en ver74.
7. Antídotos, bálsamos y Qi: conservar como frentes de QA pendientes. No declarar cobertura de aflicciones ni capacidad de compra de consumibles sin fuente y motor reproducibles.

## Gate previo a nuevos millones de combates
A. Identificar fuente ejecutable por pieza en el runtime objetivo A08, o marcar no disponible.
B. Verificar ingresos de piedras M04–M06 y coste de reposición; evitar loops de compra/reventa y craft/reventa.
C. Fijar política de stock, ventas, intercambio y disponibilidad, con aprobación humana.
D. Construir loadouts de equipo *realmente accesible* por hito y ejecutar cruce V17+V19+V20 con persistencia de aflicciones/antídotos si el motor lo soporta.
E. Solo entonces proponer congelación a Astra. Sin cambios a `main`, HTML, `ROOMS.exits`, ni integración canónica.

## QA documental
- 21/21 LII clasificadas; 8+9+4=21; 14 con piedras, 7 sin ellas.
- Sin ejecución de nuevos combates en V22; no confundir la revisión documental con benchmark.
- No se modifica ningún archivo existente. Sin decisiones canónicas nuevas.
