# LianQi II — Inicio del laboratorio por etapa real, V01

Fecha: 2026-10-07
Rama autorizada: `experiment/monster-adaptive-six-revalidation-v0.1`
Estado: **PLAN / PREFLIGHT; NO BALANCE FREEZE; NO RUNTIME INTEGRATION**

## 1. Autoridades

- `HUMAN_DECISION_TECHNIQUE_ACQUISITION_BY_LIANQI_STAGE_2026-10-07.md`
- `LI_EQUIPMENT_FREEZE_2026-10-07.md`
- `LI_CONCORDANCE_NO_TRAP_TACTICAL_GATE_V01_PLAN_2026-10-07.md` y su REVIEW PASS fuera de Git, todavía pendiente de registro de freeze numérico.
- Catálogos `techniques_arc1_catalog.json`, `equipment_arc1_catalog.json`, `monster_arc1_registry.json`
- Motor de laboratorio `etapa19b_combat_engine.py`.
- No confundir el freeze T2 de especies LI con cierre nativo de especies LII.

## 2. Alcance LianQi II

- 5 ofensivas base LI:
  `palma_ardiente`, `destello_plata`, `latigazo_marea`, `golpe_montana`, `lanza_nubes`.
- 5 defensivas que se introducen en LII:
  `cuerpo_horno`, `armadura_plata`, `espejo_luna`, `piel_cobre`, `paso_nube`.
- Tramo I desbloqueado.
- 2 puntos de técnica disponibles en total.
- 0 Tramo II/III; 0 AOE en combate LII.
- La adquisición de técnicas elementales ajenas sigue permitida bajo su contrato de progresión; no imponer obligación de injerto ni inventar penalizaciones. El muestreo monorraíz inicial **no es** cierre del espacio multirraíz.

## 3. Monstruos nativos listos

- `sapo_ceniza`: NORMAL, LianQi_II, stats READY
- `escarabajo_hierro`: TANK, LianQi_II, stats READY

No incorporar al balance inicial:
- `eco_caido`: ELITE, PENDING_INTEGRAL_REBALANCE
- `sapo_caldera`, `rey_escarabajo`: BOSS, PENDING_INTEGRAL_REBALANCE

T1–T2 son la banda adaptativa estructural esperada en LII. T2 no es equivalente automática a LII. T3/T4 se validarán progresivamente con LIII/LIV y regresión global final; no inflar monstruos todavía.

## 4. Equipo

Sin cambiar el freeze LI. Perfiles LII explícitos:
- `LII_MANDATORY_ENTRY` (catalog simulation profile, no asumir que todo jugador llega con ese inventario).
- `LII_EXPECTED_STAGE`
- `LII_HIGH_ROLL_STRESS`

Más adelante agregar carry-over real de LI (equipamiento conservado). Los perfiles son hipótesis de simulación, no garantías de adquisición. Auditar M04/M05/M06 y contribución antes de canonizar probabilidad de obtención.

## 5. Plan de pruebas

### Fase A — Contract + Compiler Preflight (ahora)

- Validar IDs canónicos de 10 técnicas, 5 defensivas, 5 ofensivas, 0 AOE utilizables.
- Compilar Tramo I: 3 familias por técnica.
- Generar por raíz 16 configuraciones monorraíz preliminares:
  - BASE 0 puntos: 1
  - T1 en ofensiva solamente: 3
  - T1 en defensiva solamente: 3
  - T1 en ofensiva y defensiva: 9
- Total del subespacio monorraíz: 80 configuraciones (5 raíces×16).
- **Los 2 puntos no se asignan dos veces al mismo Tramo I de la misma técnica.** Un punto elige una de tres especializaciones de ese tramo.
- No supone que 80 = todas las builds legales, porque hay aprendizaje multielemental.
- Pruebas del motor de base sólo T0 con políticas UNITARGET_FIRST y DEFENSE_OPEN, R24; verificar Qi, roles, compilación, daño, defensas, 0 usos AOE, no NaN y zero timeouts sospechosos.
- Salida `LII_STAGE_REAL_PREFLIGHT_V01_REVIEW.zip`.
- No dar PASS sistémico LII de este smoke test.

### Fase B — Defensa causal en combate + T1/T2 nativos

- Comparación contra las dos especies READY, escala gradual R64→R256 si ambiguo.
- Adaptación T2 con memoria de 2 acciones efectivas consecutivas de categoría, anticipación 40% HP o golpe 15%; T1 natural se preserva y `due` canónico no se sustituye.
- Contrastar apertura DEFENSE_OPEN con defensas temporizadas/contextuales y rotación ofensiva; no codificar gasto automático de defensiva como política óptima.
- Validar si cada defensiva se siente útil sin obligar al jugador a activarla siempre.
- Medir P(win), HP final, Qi, duración, defensa absorbida, salvaguardas de IA, control y efectos de disponibilidad real.

### Fase C — Tramo I y builds multielementales

- Evaluar 0/1/2 puntos en configuraciones legales, conforme contrato de aprendizaje/adquisición.
- Cruzar especializaciones de defensiva y ofensiva, raíces ajenas aprendidas y penalizaciones **sólo si están definidas**; no inventar restricciones de injerto.
- Usar un screening predictivo para priorizar combos, no como sustituto de las pruebas reales.

### Fase D — Equipo LII como primera clase

- Catalogar adquisición M04–M06 y la progresión de equipo LI→LII.
- Cruzar ENTRY/EXPECTED/HIGH_ROLL con builds y roles, detectar piezas muertas/dominancia y cliffs.
- No tocar el equipo LI congelado.

### Fase E — Concordancias LII + cierre

- Extender hooks a las cinco defensivas y a Tramo I donde existan realmente.
- Mantener matriz conceptual 20/20, un Eco por resolución, sin fallback genérico.
- No extrapolar sin test las 16 magnitudes LI a nuevos hooks.
- Gate NO_TRAP específico LII, microescalaciones y regresión final.
- Preparar handoff final para Astra **al terminar** las etapas, sin integración durante este laboratorio.

## 6. QA y seguridad

- No main; no merge; no push salvo autorización expresa.
- Sólo rama experimental y documentos/lab; no modificar runtime HTML.
- AI decide, motor resuelve, no APIs/LLMs runtime, no relojes nuevos.
- Checkpoints reanudables, WORKERS=2 para Colab, progreso persistente `ipywidgets.IntProgress+HBox`, RUN azul, CP amarillo, DONE verde, ERR rojo.
- Manifest y SHA-256 de input, runner y outputs; QA de notebooks antes de entregar.
- No introducir valores canónicos nuevos sin evidencia.
