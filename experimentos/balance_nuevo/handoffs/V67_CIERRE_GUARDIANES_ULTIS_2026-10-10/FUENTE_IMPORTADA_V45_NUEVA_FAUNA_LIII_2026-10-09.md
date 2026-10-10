# La Grulla Blanca — V45 · Seis monstruos normales nuevos para LianQi III

**Fecha:** 9 de octubre de 2026. **Corte:** laboratorio T0 V45, CRN y holdout independiente. **No es runtime ni autorización de T0 READY.**

## 1. Decisión que originó el trabajo

El autor solicitó ampliar la escasa fauna normal del tramo LianQi III con criaturas originales, usando resultados de las simulaciones previas. El punto de partida de poder del jugador es **LIII (42 HP / 49 Qi / 4 PT/Tramo II) con el mejor equipamiento LII**; no con equipo LIII concedido automáticamente. Para nuevas criaturas se definieron **6 perfiles no únicos**, con daño y habilidades soportadas por el simulador real de ETAPA19B; no se inventaron habilidades de Control aún no vinculadas.

La auditoría del atlas de ver76 candidata encontró **329 salas en total, 22 en `aguas_barrancos`**, y sólo **dos perfiles normales previos LIII**: `pez_lunar` y `anguila_estelar` (además del élite `sombra_ahogada` y jefe `guardian_coral`). Estos dos normales previos se mantienen intactos. La propuesta agrega 6, dando un catálogo futuro de **8 especies normales de LIII** (incluidos roles de escaramuzador/tanque) en esta región. Ninguna nueva criatura invade una sala de jefe/élite o un spawn fijo existente.

## 2. Fichas de las seis especies — propuesta numérica final del laboratorio

Los seis perfiles entregados en `PATCH_PREVIEW_MONSTERS_V45.json` conservan `stats_status=PENDING_INTEGRAL_REBALANCE` y `technique.params_status=PENDING_INTEGRAL_REBALANCE`, aun teniendo valores numéricos propuestos; no se pueden promover automáticamente a `READY`. Control 0 es **hipótesis del LAB**, no ratificación humana del atributo. Qi máximo `null` respeta `resource_model=NONE`.

| Especie (ID) | HP | PREC | EVA | DEF | TEN | Básico | Técnica cada N turnos |
|---|---:|---:|---:|---:|---:|---|---|
| **Garza de Bruma de Roca** (`garza_bruma_roca`) | 75 | 109 | 31 | 0 | 14 | `1d2+6` | Pico de Niebla Cortante: `1d3+8` / 3 |
| **Cangrejo de Laja Húmeda** (`cangrejo_laja_humeda`) | 90 | 98 | 9 | 3 | 28 | `1d2+6` | Tenaza de Pizarra: `1d3+8` / 4 |
| **Sanguijuela de Remanso Turbio** (`sanguijuela_remanso_turbio`) | 78 | 103 | 16 | 1 | 16 | `1d2+6` | Mordida de Limo Frío: `1d2+7` / 3; veneno 1d2+2 × 2 ticks |
| **Salamandra de Filtración Tibia** (`salamandra_filtracion_tibia`) | 79 | 103 | 16 | 2 | 22 | `1d2+6` | Salpicadura Irritante: `1d2+7` / 4; quemadura 1d2+1 × 2 ticks |
| **Rana de Cascajo del Barranco** (`rana_cascajo_barranco`) | 84 | 100 | 17 | 2 | 23 | `1d2+6` | Salto de Cascajo: `1d3+8` / 3 |
| **Carpa de Lámina Reflejada** (`carpa_lamina_reflejo`) | 78 | 104 | 26 | 1 | 13 | `1d2+6` | Succión de Corriente: `1d3+7` / 3; drenaje 3 Qi al conectar |

Los críticos son 5 % / ×1,5 para cada nuevo perfil; no hay escalado adaptativo ni Mutantes en esta propuesta. El Cangrejo dispone de DEF 3 y alta TEN, no escudo invisible. Sanguijuela y Salamandra usan DOT real que atraviesa DEF y respeta absorción. La Carpa consume Qi; el Pez y la Anguila antiguos no se alteran.

## 3. Ubicaciones en el mundo existente

**Solo nuevas colocaciones fijas sugeridas**, una identidad por sala, sin alterar `ROOMS.exits` ni crear habitación, gate, misión, NPC o hábitat nuevo. La seguridad en LI–LII exige **filtro de cultivo del owner NEW** antes de materialización, targeting, atracción y recompensa; ocultar una sala no es protección suficiente. Ninguna colocación de las siguientes está ejecutándose en el juego.

| Especie | Sala 1 | Sala 2 |
|---|---|---|
| Garza de Bruma de Roca | `aguas_cauce_alto` | `aguas_paso_piedras` |
| Cangrejo de Laja Húmeda | `aguas_garganta_norte` | `aguas_pasarela_roca` |
| Sanguijuela de Remanso Turbio | `aguas_poza_profunda` | `aguas_cascada_velada` |
| Salamandra de Filtración Tibia | `aguas_filtraciones_cantera` | `aguas_paso_alto` |
| Rana de Cascajo del Barranco | `aguas_garganta_sur` | `aguas_desvio_sauces` |
| Carpa de Lámina Reflejada | `aguas_manantial_entrada` | `aguas_rama_clara` |

Las 12 salas escogidas tenían cero mobs fijos, cero NPCs y cero objetos fijos en el snapshot auditado. Se preservan exactamente las ubicaciones de `pez_lunar`, `anguila_estelar`, `sombra_ahogada` y `guardian_coral`, así como los territorios errantes ya existentes. No se crean 12 criaturas activas antes del gate: el archivo es un **plan de colocación condicionado**.

## 4. Batería y reproducibilidad

Congelé y validé por SHA-256 las fuentes de combate, equipo y técnicas de V44 sin cambiarlas. La semilla se mantiene pareada para ambos brazos del monstruo y los tres arquetipos de equipamiento de una misma raíz/build/política/réplica. Dos políticas: `UNITARGET_FIRST` y `DEFENSE_OPEN`. Siete configuraciones focales por raíz: BASE, OFF_I, OFF_II, DEF_II, SPLIT_I, BOTH_II y MIXED, 4 PT como máximo. **Sin AOE**, sin Ultimates frente a normales, sin T1–T4. Las tres cargas: LII alto defensivo, LII alto evasivo, y posterior torso M08 **opcional** para medir la progresión.

| Cohorte | Nuevas peleas | COLD (no nuevas) |
|---|---:|---:|
| SCREEN | 10.080 | 0 |
| FOCAL | 12.600 | 0 |
| HOLDOUT | 90.720 | 0 |
| MICRO | 15.120 | 0 |
| HOLDOUT2 | 90.720 | 0 |
| COLD | 0 | 22.680 |
| COLD2 | 0 | 22.680 |
| **TOTAL** | **219.240** | **45.360** |

**QA: PASS.** Cero timeouts; integridad de fuentes; 90.720 peleas en el holdout final y 22.680 repeticiones COLD2 que coinciden fila por fila (0 diferencias). El holdout anterior y su COLD también coinciden. Cohortes SCREEN/FOCAL/MICRO sirvieron para cribar, y los **resultados comparables del final solo se citan del `HOLDOUT2` independiente**. No sumamos COLD al total de nuevas peleas.

## 5. Holdout final: qué monstruos funcionan

Las cifras son **victorias del jugador**, no del monstruo; cada celda de especie/equipo n=2.520 (5 raíces × 7 builds × 2 políticas × 36 semillas). Las rondas incluyen victorias y derrotas, no solo las peleas ganadas.

| Especie | Mejor LII DEF | Mejor LII EVA | M08 torso opcional | Rondas med. DEF |
|---|---:|---:|---:|---:|
| Garza de Bruma de Roca | 84.52 % | 71.67 % | 94.4 % | 9 |
| Cangrejo de Laja Húmeda | 77.94 % | 56.75 % | 94.52 % | 12 |
| Sanguijuela de Remanso Turbio | 81.23 % | 65.87 % | 92.42 % | 9 |
| Salamandra de Filtración Tibia | 83.29 % | 67.46 % | 95.2 % | 9 |
| Rana de Cascajo del Barranco | 83.77 % | 67.98 % | 95.71 % | 10 |
| Carpa de Lámina Reflejada | 86.67 % | 72.7 % | 97.06 % | 10 |

- **No son clones:** Garza tiende a esquivar; Cangrejo es la prueba de penetración y aguante; Sanguijuela aplica veneno real; Salamandra pone quemadura; Rana da daño directo sostenido; Carpa presiona con drenaje de Qi.
- **No se rebajó ninguna vestidura:** la ganancia por M08 es muy notable. Es una mejora de progresión, no un error numérico que deba borrarse.
- **Diferencias entre raíces:** Fuego se impone más fácilmente en todos los perfiles; Agua y Viento son más vulnerables ante algunos. No usar el promedio como demostración de equidad perfecta. Cangrejo con mejor LII defensivo arroja ~68,45 % de Agua y ~60,71 % de Viento contra ~98,02 % de Fuego. Requiere validación por raíz y equipo antes de canon.
- **Los seis son normales, no élites:** no hay fases, memoria permanente, inmunidad especial ni guardián AOE encubierto. La complejidad proviene de estadística normal, un especial periódico y/o DOT/drenaje que ya maneja el lab.

## 6. Límites técnicos y bloqueos explícitos

1. `stats_status=PENDING_INTEGRAL_REBALANCE` sigue vigente para los seis. Ninguna persona aprobó todavía sus números individualmente. `PATCH_PREVIEW...` NO debe importarse como perfiles productivos READY.
2. El validador original del registry impone **18 perfiles exactos** (`profile_count` + `load_registry`); hay que ampliar las autoridades y pruebas de 18 a 24 mediante una tarea de integración explícita, sin falsear cierres antiguos. El archivo `REGISTRY_24_PREVIEW_V45.json` es **solo revisión**.
3. **El gate LIII aún no está integrado**: ver76 materializa mobs fijos sin comprobar etapa NEW. Añadir criaturas directamente a `ROOMS.mobs` sin gate produciría encuentros LI/LII no autorizados. Mantener fail-closed hasta conectar CultivationDomain y revalidar spawn, targeting, atracción, combate, cadáver y reward.
4. Los combates evaluados son **1 contra 1**. No se ejecutaron oleadas de dos o tres monstruos ni AOE post-manual. No atribuirle al programa pruebas de mezcla de roster que todavía no soporta.
5. El mejor set LII no es automáticamente concedido a todos los jugadores; es el **baseline de balance solicitado**. El torso de M08 es opcional, no dotación inicial.
6. El coste de Lanza de Viento en LIII y la paridad real de Tramo II/Concordancias/Control/A08 siguen pendientes; no modificar la ratificación V36/V38 LII.
7. No se crearon drops productivos, tasas de caída, precios, materiales de extracción activos ni nuevas misiones. Los recursos de `FICHAS_ECOLOGIA_V45.json` son ideas pendientes de auditoría de profesión/cadáver/obtención para evitar botín gratis e inconsistencias.
8. Las simulaciones nuevas se anclan al laboratorio V44 y a la estructura de cinco raíces y equipo, no convierten comparaciones V43/V35 históricas en repeticiones nuevas.

## 7. Próximo orden de trabajo

**Ahora:** una aprobación humana de las seis identidades y de su rol de población, seguido de balance T0 específico de los outliers por raíz / equipos opcionales y pruebas de densidad real (1v2, 1v3, oleadas y respawn) cuando se conecte el runner adecuado. **Después:** terminar Pez Lunar y Anguila, trabajar Sombra Ahogada, validar equipo M08–M12 y Tramo II, posteriormente las cinco AOE tras manual. Solo al final guardianes únicos AOE.

## 8. Proveniencia

- GitHub: `Shein25/La-Grulla-Blanca`, rama de laboratorio `experiment/lii-tramo1-multirraiz-v08-2026-10-08`, HEAD de referencia `3d581e92d49f76bbce06fd7bfbda3ecf2ee680ca`.
- V44 base (`GRULLA_LIII_V44_PRIMER_BALANCE_T0_2026-10-09.zip`): SHA-256 `ffdf1bc8c4f2a4a294d0e8118a987af90ebfac9a32894e8cbd641a046f310303`.
- HTML candidata ver76 inspeccionada para mapa (no runtime productivo): SHA-256 `ca9147dde7932a10b5e9ff67283ea3b47c007042a3b293b85b04dc342c6c92ee`. Solo se empaquetó un snapshot de rooms, no el archivo entero.
- No se modificó GitHub ni `main`, no se ejecutaron merges, push, ni cambios a HTML, ROOMS, A07 o misiones.

**ESTADO FINAL V45: DESIGN_NEW_SIX_SPECIES_DONE; 12 ROOM_PLACEMENT_PREVIEW_PASS; T0_NUMERIC_CANDIDATES_VALIDATED_IN_LAB; HUMAN_NUMERIC_FREEZE_PENDING; STAGE_GATING_INTEGRATION_BLOCKED.**