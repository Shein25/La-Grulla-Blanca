# HANDOFF V66 — guardianes AOE por raíz — 2026-10-10

**Estado:** HANDOFF_DOCUMENTAL / LAB V66 terminado **sin Ulti** / no es ratificación de cinco kits ni integración de runtime.
**Repositorio:** Shein25/La-Grulla-Blanca
**Rama exclusiva de respaldo:** \`handoff/v66-guardianes-aoe-2026-10-10\`
**Base:** \`experiment/lii-tramo1-multirraiz-v08-2026-10-08\`. NO tocar main, NO merge, NO editar HTML, ROOMS.exits, gates, A07, comercio ni spawn.
**Último experimento:** V66, «Guardianes AOE, desglose por las cinco raíces»; **63.000 combates nuevos**: 36.000 principales (18.000 controles + 18.000 V65 candidatos) y 27.000 sensibilidad. 0 errores/timeouts reportados, 0 candidatos vencidos en <=3 acciones en la muestra principal.
**Artefacto portable íntegro:** \`GRULLA_V66_GUARDIANES_AOE_DESGLOSE_5_RAICES_2026-10-10.zip\` (708 KB aprox.), SHA-256 \`e8402ca195ba9f2d4fe97ae4a71351d25f691c7601a81c49693cdf77198d3a39\`. **Este ZIP no está incrustado en Git**; el respaldo en Git preserva este handoff, resultados esenciales, fuentes y punto de reanudación. Conservar/subir el ZIP junto al próximo chat para reproducir los 63.000 combates; no afirmar lo contrario.

## AUTORIDADES (orden obligatorio)
1. Decisión humana del 2026-10-07: \`experimentos/balance_nuevo/adaptive_six_revalidation_v0.1/DECISION_HUMANA_GUARDIANES_AOE_IDENTIDADES_UBICACIONES_2026-10-07.md\`, commit \`0f59db18357abadc168cd117d14aa0010e8453e2\`.
2. **Cuatro T0 únicos ratificados**, commit \`45c3a9c240ea74208a0d8fd4d5be187bc817df35\`, \`experimentos/balance_nuevo/monster_arc1_registry.json\`, blob \`0261dd2b254ee0db0d28256b37e54fd7756790c7\`. Snapshot anterior con \`PENDING_INTEGRAL_REBALANCE\` no deroga este T0.
3. V61-C = **candidato** de balance de técnicas; V62 = guarda estricta del +10% exclusiva de la propia técnica Metal/Viento con PT; V63 = gate experimental LIII; V65 = candidatos de kits de guardianes; V66 = comparación separada por raíz. Nada implica ratificación de fichas V65.
4. **Ultis:** revisar \`DECISION_ULTIMATE_REPERTOIRE_2026-10-05.md\` y autoridad V03.1 real. En LIII únicamente Ulti PRINCIPAL si la rama tiene maestría \`APRENDIDA_AL_MAXIMO\`; no exige PT activos de la tercera familia; **máximo una Ulti usada por combate**. Ulti del injerto: LIV, NO en este gate. V65/V66 NO tienen puente físico validado de Ultis: \`WITH_ULTI=BLOCKED\`, no valor 0 ni daño inventado.

## IDENTIDADES Y REGLAS DE CINCO GUARDIANES
- Fuego: \`sapo_caldera\`, Sapo Caldera de Tres Gargantas; sala \`camara_caldera\`; entrega manual para Círculo de las Cien Ascuas.
- Metal: \`rey_escarabajo\`, Rey Escarabajo de la Veta Negra; sala \`nido_escarabajos\`; manual para Lluvia de Filos.
- Agua: \`guardian_coral\`, Guardián de Coral Memorioso; sala \`aguas_rama_oscura\` (NO \`aguas_camara_hidrica\`); manual para Marea de las Ocho Orillas (runtime histórico \`marea_circular\`, revisar mapeo antes de implementar).
- Viento: \`mantis_nube\`, Mantis de Nube Cortante; ubicación histórica \`alturas_senda_mantis\`, propuesta \`bosque_corredor_viento\` aún NO implementada; manual para Tijera del Vendaval Partido.
- Tierra: \`custodio_eco_petreo\`, **El Custodio del Eco Pétreo** (nombre/ID RATIFICADOS); propuesta sala \`bosque_rocas_blancas\`, **SIN spawn, SIN manual/runtime, SIN T0 numérico ratificado**; manual conceptual Temblor de Montaña. **No sustituirlo por Centinela de plumas petrificadas.**
- Los cinco se perciben legalmente **desde LianQi III**, aunque la sala de alguno corresponda a zona LII. No equiparar \`native_stage\` antiguo con acceso legal.
- Guardianes únicos: una derrota por partida, sin respawn, entrega única e idempotente del manual, sin atracción entre salas; huida reinicia encuentro. No hay tres fases obligatorias: **kits continuos y telegráficos**. Cuatro T0 históricos conservados en brazo BASE; V65 son overlays TUNED experimentales.
- Gate de adquisición: personaje **LIII PRE_AOE**, 4 PT legales, equipo realmente accesible, sin la técnica AOE que el guardián entrega, con brazo NO_ULTI y brazo MAIN_ROOT_ULTI_READY (pendiente). Tramos máximos LIII: II. La Ulti no debe regalarse ni usarse si no se cumple maestría.
- Norma de AOE POST manual: cuando hay un solo enemigo hostil, **x0.65 antes de DEF**, sea jefe o monstruo común; con >=2 hostiles, x1 por objetivo, sin reparto ni límite fijo, impacto por objetivo, Qi pagado una sola vez y un Eco según el contrato, sin spawns inventados. Esta regla no transforma un duelo PRE_AOE en multiblanco.

## RESULTADO V66 — MATRIZ 5×5, victoria del jugador, SIN Ulti
720 combates por pareja guardián/raíz (dos equipos, 3 builds, 3 políticas, semillas nuevas). No es paridad definitiva con Concordancias ni Ultis.

| Guardián | Fuego | Metal | Agua | Tierra | Viento |
|---|---:|---:|---:|---:|---:|
| Sapo Caldera | 50,3% | 42,6% | 30,0% | 29,0% | 52,6% |
| Rey Escarabajo | 83,2% | 63,5% | 52,8% | 52,5% | 65,4% |
| Guardián de Coral | 46,7% | 39,9% | 19,7% | 24,0% | 41,8% |
| Mantis de Nube | 59,2% | 48,2% | 37,2% | 33,6% | 56,8% |
| Custodio del Eco Pétreo | 55,6% | 41,8% | 24,9% | 31,1% | 45,7% |

| Guardián | Victoria global | Mediana de turnos al vencer | Victoria de SU raíz |
|---|---:|---:|---:|
| Sapo | 40,9% | 10 | Fuego 50,3% |
| Rey | 63,5% | 11 | Metal 63,5% |
| Coral | 34,4% | 12 (Agua 14) | Agua 19,7% |
| Mantis | 47,0% | 10 (Viento 9) | Viento 56,8% |
| Custodio | 39,8% | 11 (Tierra 13) | Tierra 31,1% |

**Hallazgos no negociables:** Coral demasiado duro para Agua (y Tierra); Custodio duro para Tierra y builds no ofensivas; Rey algo fácil para Fuego (83,2%), pero subir +1 DEF castiga demasiado a Metal/Agua; Sapo/Mantis funcionan como candidatos, NO ratificados. En 18.000 enfrentamientos candidatos: sin derrotas de guardián en <=3 acciones. El brazo Ultis podría modificar ese resultado.

### Sensibilidad V66 (cohortes propias, NO mezclar porcentajes con la matriz principal)
- Coral: drenaje 4→2 Qi mejora poco a su propia raíz; no alcanza para arreglar daño/precisión/control/tempo. Investigar **ventanas de vulnerabilidad condicionadas a acciones reales de Agua**, sin daño gratuito ni inmunidades.
- Custodio: DEF 4→3 beneficia mucho a Tierra pero vuelve trivializable por Fuego. Rediseñar contra-juego de Resonancia para Control, defensas y preparación; no nerfear universalmente la DEF.
- Rey: +1 DEF o +8 HP pueden hundir las raíces débiles. Conservar caparazón temporal y ventanas legibles; no subir defensa permanente.

## REPRODUCIBILIDAD Y ARCHIVOS DEL ZIP
- \`V66_RESULTADOS_INDIVIDUALES.csv\` (36.000 combates), \`V66_SENSIBILIDAD_INDIVIDUAL.csv\` (27.000), matrices \`V66_MATRIZ_5X5_CONTROL_Y_CANDIDATO.csv\`, \`V66_DELTA_PAREADO_POR_RAIZ.csv\`, agregados por raíz/jefe/build/equipo/política.
- \`V66_RESUMEN_Y_GUARDAS.json\`, \`V65_FICHAS_T0_Y_CUSTODIO_NO_CANON.json\`; \`v65_aoe_guardian_lab.py\`, \`ejecutar_v66_por_raiz.py\`, \`sensibilidad_v66_tres_jefes.py\`, \`generar_informe_y_zip_v66.py\`.
- \`sources/\` trae motor experimental V47–V62, equipos y registro de monstruos; \`MANIFEST_SHA256.json\`, \`INFORME_V66_DESGLOSE_POR_RAIZ.md\`. El ZIP original pasó CRC en sesión 2026-10-10; SHA-256 fijado arriba.
- Los resultados de combates provienen del runner de laboratorio, no runtime HTML. No se reabren campañas cerradas V50–V63 sin bug causal comprobado.

## SIGUIENTE TRABAJO EXACTO: V67
1. Antes de calibrar números nuevos, auditar contrato y **runner físico de Ultis V03.1**, localizar fuentes autorizadas, sus 25 definiciones, verificación de maestría y consumo de una Ulti. NO inventar daños, Qi ni cooldown.
2. Implementar puente aislado de comparación pareada \`NO_ULTI\` vs \`MAIN_ROOT_ULTI_READY\` con semillas iguales por guardián/raíz/build/equipo/política; usar turnos, Qi, telegráficos, DEF, DOT, Absorción y Eco reales. LIII PRE_AOE; del injerto no corresponde.
3. Medir win-rate, TTK de victorias, muerte del jefe <=3 acciones, daño de Ulti, acción/turno de ejecución, porcentaje que no llega a usarla, Qi/HP al finalizar, por raíz, con especial seguimiento de Agua→Coral, Tierra→Custodio y Fuego→Rey.
4. Optimizar Coral/Custodio con ventanas que permitan contrajuego dentro del sistema, sin nerfs universales ni recomenzar desde cero; verificar también Rey/Sapo/Mantis.
5. Para cierre: ratificación humana expresa antes de modificar cuatro T0 históricos, cinco kits, premios, gates, salas o runtime. Mantener \`main\` intacto, NO merge ni push de código productivo.

**CONTINUAR DESDE V66**, no desde V64 ni recatalogar a Centinela como guardián.