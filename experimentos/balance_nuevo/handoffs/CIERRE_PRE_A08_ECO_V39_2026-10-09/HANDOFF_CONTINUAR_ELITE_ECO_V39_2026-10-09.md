# HANDOFF DE CONVERSACIÓN — La Grulla Blanca / PRE-A08 / Eco del Caído V39
**Corte:** 2026-10-09. **Autoridad:** decisiones humanas por encima de recomendaciones experimentales. **Estado:** trabajos numéricos cerrados de Viento y seis monstruos normales; frente activo Eco del Caído, élite T0 no ratificado. **NO MAIN / NO MERGE / NO HTML / NO ECONOMÍA.**

## 1. Repositorio, guardias y punto de partida
- Repo: https://github.com/Shein25/La-Grulla-Blanca
- Rama documental y experimental autorizada: **experiment/lii-tramo1-multirraiz-v08-2026-10-08**. Backup de snapshot separado: **backup/pre-a08-eco-v39-2026-10-09** (verificar que se haya creado antes de citarlo).
- Primera lectura obligatoria: este handoff; el prompt hermano; acta ratificada de Lanza; cierre seis normales; reporte y QA V39; registro de Eco y adquisición real de técnicas. Si un dato no está verificado, mantenerlo como pendiente.
- No editar main, no merge/push adicional salvo documentación/backup solicitado, no tocar HTML, ROOMS.exits, gates, A07, NPC, historia, precios, tiendas, comercio o registros de monstruos productivos.
- Ejecutar experimentos solo contra fuentes del motor de laboratorio y copias en memoria. Nunca declarar READY a Eco ni T1/T2 sin pasar los gates.

## 2. Decisiones humanas RATIFICADAS — NO REABRIR
**Viento (V36 + enmienda V38):** en LianQi II Lanza que Parte Nubes (lanza_nubes) cuesta 5 Qi, y con el nodo T1 de Eficiencia seleccionado, 4 Qi; en LianQi I permanece 6 Qi. Lanza T1 DIRECT aplica +30 % de V17 (ojo: V35 tenía un fallo en el adaptador LAB, no un bug productivo acreditado); Lanza T1 PRECISION compila daño 2d4+4; Paso de Nube Ligera T1 EVA concede 45 de evasión con coste/duración intactos. NO sangrado, NO aumento de daño global. Guardar estos cambios para integración posterior, todavía NO escritos en HTML.
**Seis normales LianQi II cerrados (V33–V35):** Jabalí Embestida 1d3+8; Búho Picado 1d2+8; Zorro Evasión 21; Cangrejo Pinza 1d2+8; Murciélago Pulso 1d2+6; Araña HP 75. No aplicar antiguos nerfs V19 ni variantes agresivas V34. Conservar los perfiles adaptativos y demás habilidades.
**Equipo y expectativas:** Sobretúnica de patrulla es la vestidura defensiva superior de LianQi II, DEF+2/HP+2; NO nerfearla a DEF1. Las recompensas deben sentirse superiores y respetar su momento real de obtención. M04/M05 son controles de disponibilidad OPCIONAL en V39, no adquisición demostrada.
**Otras reglas:** efecto seleccionado para veneno: -10 % de recuperación de Qi FUERA del combate, implementación/productivo pendiente (V30). Alivio HP Templada Estable 3d4+9 ratificado previamente. No reabrir economía/precios/comercio.

Archivos de autoridad:
- experimentos/balance_nuevo/handoffs/CIERRE_RATIFICADO_VIENTO_Y_NORMALES_2026-10-09/RATIFICACION_LANZA_QI5_V38_2026-10-09.json
- experimentos/balance_nuevo/handoffs/CIERRE_RATIFICADO_VIENTO_Y_NORMALES_2026-10-09/DECISION_HUMANA_CIERRE_LII_NORMAL_Y_VIENTO_2026-10-09.json
- experimentos/balance_nuevo/handoffs/PRINCIPIO_RATIFICADO_EXPECTATIVA_PROGRESION_EQUIPO_2026-10-09.md
- experimentos/balance_nuevo/pre_a08_cierre_normales_v35/FINAL_NUMERIC_TARGETS_SIX_NORMALS_V35.json

## 3. Punto exacto del frente ÉLITE: Eco del Caído (eco_caido)
**NUNCA afirmar que E8 está aprobado.** Es el candidato T0 mejor sustentado de E5/E7/E8/E9 históricos; el registro moderno sigue PENDING_INTEGRAL_REBALANCE y BLOCKED_UNTIL_T0_READY; technique=null; sin T1–T4.
Datos E8 reales recuperados del handoff histórico (branch handoff/lii-monsters-close-2026-10-08; blob a0ecb21dafe126d05d897349ee1889198b8c088b): HP84, PREC96, EVA18, DEF1, TEN18, daño básico 1d2+4. Control NO recuperado: V39 usó 0 explícitamente hipotético; 20 pares adicionales Control0 vs Control60 dieron métricas idénticas en el T0 SIN técnica especial, no autorizan el valor real.

**V39, nueva batería:** 18.240 combates (9.120 DISCOVERY + 9.120 HOLDOUT), 2.160 filas ×19 columnas COLD exactas; 0 timeouts. LI con equipo prólogo y solo ofensiva: Eco E8 9,69 % WR jugador, Escarabajo READY 9,48 %, Sapo READY 42,71 %. LII contra E8: equipo prólogo y ofensiva 69,43 %; post-M03 y ofensiva 70,52 %; post-M03 y defensiva hipotética 81,41 %; M04 Sobretúnica opcional ofensiva 96,67 %; M04 con defensiva hipotética 98,80 %; M05 Sauces opcional y ofensiva 77,14 %; con defensiva 84,01 %. No mezclar como si todos fueran equipos garantizados. Viento LII en V39 ya usa Lanza 5 Qi (69,79 % ofensiva con prólogo).
**Riesgo de diseño confirmado en ver74 (NO ver76):** ruta determinista desde patio_raices hasta cruce_vetas con 20 movimientos por ROOM.exits, sin atravesar gates; sala oculta=true aloja eco_caido; paso final terraza_cantera --sur--> cruce_vetas. La interfaz oculta la salida pero cmd_ir/bloqueoPaso no exige LianQi II. Conocimiento manual de comandos puede permitir una pelea casi imposible en LI (9,69%). No modificar ROOMS.exits ni introducir puertas arbitrarias. Hallazgo de acceso NO equivale a permiso humano para bloquear.
**Observación:** la narración de derrota y la bandera de vena resentida mencionan campo de entrenamiento/veta_negra, aunque Eco se sitúa en cruce_vetas; evaluar coherencia sin alterar narrativa.

Fuente:
- experimentos/balance_nuevo/pre_a08_elite_v39/DICTAMEN_ECO_ETAPA_Y_E8_V39_2026-10-09.md
- experimentos/balance_nuevo/pre_a08_elite_v39/QA_V39_GIT_SUMMARY.json
- experimentos/balance_nuevo/pre_a08_elite_v39/GATE_DECISION_NEXT_ELITE_V39.json
- Archivo portable: GRULLA_PRE_A08_V39_ECO_ETAPA_Y_GATES_T0_2026-10-09.zip, SHA256 eb9c8fd127df1120decf5584dfbd1d26d78ad47c47fbe91f40495d428d244bbd, 26 entradas, CRC/manifiesto PASS.

## 4. Próxima acción PRECISA y ordenada
1. Verificar HEAD/backup y leer los contratos anteriores. Confirmar contra ver76, si está disponible, la ruta oculta y ausencia/presencia de gate real; separar constatación ver74 de producción.
2. Determinar por lectura de misiones/cronología **cuándo** se espera luchar contra Eco y qué ofensivas, defensivas, equipo y consumibles puede poseer legítimamente. No inventar estados, gates ni misiones.
3. Someter al usuario una **decisión de diseño de acceso** bien fundamentada: encuentro secreto temprano con alto riesgo (y advertencias) **O** combate activado tras reconocimiento/progresión existente manteniendo el mapa explorable. No asumir automáticamente una opción.
4. Diseñar en laboratorio (no producción) 2–3 hipótesis de habilidad **propia del élite espiritual** capaces de presionar al jugador LII equipado, en lugar de inflar HP/ataque sin sentido ni debilitar Sobretúnica. Vincular a identidad, telegrafiado y counterplay; ninguna mecánica nueva sin aprobación.
5. Con hipótesis humanamente autorizadas, ejecutar baterías pareadas T0 con cinco raíces, LI exposición temprana si corresponde y LII equipos realmente legales; medir victorias, HP residual, Qi, turnos y distribución por build, incertidumbre y reproducibilidad. No repetir V02 34.560, V37 5.120, V38 ni V39 18.240 sin razón.
6. Reconciliar el Control E8 y la diferencia entre runner histórico T0 y motor nuevo. Después de la ratificación humana de T0, recién abrir T1/T2 con paridad evento-a-evento a la IA monstruos congelada. Integración Astra posterior y separada.

## 5. Matriz de autoridad y exclusiones
- LI no puede usar técnicas defensivas ni puntos Tramo I; en LII sí defensivas + Tramo I, +2 PT; sin AOE hasta LIII. Los tiers del monstruo T0–T4 NO son niveles LianQi.
- La fuente antigua de LI/LII listaba Sapo, Escarabajo y Eco como enemigos propios del gate LII; V35 cerró aparte seis perfiles normales estudiados bajo otro frente. **No deducir cronología real de solo native_stage**; si las dos autoridades de etapa parecen inconsistentes, verificar sin reabrir estadísticas aprobadas.
- Sapo Caldera y Rey Escarabajo: guardianes únicos LianQi III (manuales AOE), no pertenecen a este frente.
- Concordancias estructurales/condicionales V24–V26, aflicciones puente V27–V30, y paridad A08 siguen pendientes en sus propios frentes. Ningún freeze global PRE-A08.
- No suponer que el 98,80 % con Sobretúnica implique un bug o autorice nerf. No convertir Eco en esponja HP: si se necesita identidad élite, debe depender de habilidades, lectura de intenciones y preparación del jugador.

## 6. Backup / verificación
Este handoff tiene prompt compañero y manifiesto local de archivos ZIP (V20 histórico y V21–V39). El ZIP offline del cierre contiene CSV brutos y runners que Git NO contenía previamente. Los documentos y la rama de snapshot Git respaldan la autoridad y el estado del repositorio; el ZIP descargable respalda los binarios completos. Ver BACKUP_MANIFEST_2026-10-09.json en el paquete.
