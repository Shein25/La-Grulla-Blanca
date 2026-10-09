# PROMPT PARA NUEVO CHAT — LA GRULLA BLANCA / RETOMAR ÉLITE ECO V39

Retomá el proyecto **La Grulla Blanca** exactamente después de V39 (corte 2026-10-09). No vuelvas a diseñar desde cero ni pidas archivos/decisiones que ya están en Git. **Tu tarea actual es el ELITE Eco del Caído**, no el balance de Viento ni de los seis monstruos normales, que ya se cerró por decisión humana.

Repositorio: https://github.com/Shein25/La-Grulla-Blanca
Rama autorizada para documentación/laboratorios: experiment/lii-tramo1-multirraiz-v08-2026-10-08
Rama respaldo de snapshot: backup/pre-a08-eco-v39-2026-10-09 (verificá que exista).
**NO tocar main, NO merge, NO HTML/runtime productivo, NO ROOMS.exits, NO A07, NO NPCs, NO precios/comercio.** La integración productiva corresponde luego a Astra, con paridad y consentimiento.

**Primero leé estos archivos en Git en este orden:**
1. experimentos/balance_nuevo/handoffs/CIERRE_PRE_A08_ECO_V39_2026-10-09/HANDOFF_CONTINUAR_ELITE_ECO_V39_2026-10-09.md
2. experimentos/balance_nuevo/handoffs/CIERRE_RATIFICADO_VIENTO_Y_NORMALES_2026-10-09/RATIFICACION_LANZA_QI5_V38_2026-10-09.json
3. experimentos/balance_nuevo/handoffs/CIERRE_RATIFICADO_VIENTO_Y_NORMALES_2026-10-09/DECISION_HUMANA_CIERRE_LII_NORMAL_Y_VIENTO_2026-10-09.json
4. experimentos/balance_nuevo/pre_a08_cierre_normales_v35/FINAL_NUMERIC_TARGETS_SIX_NORMALS_V35.json
5. experimentos/balance_nuevo/pre_a08_elite_v39/DICTAMEN_ECO_ETAPA_Y_E8_V39_2026-10-09.md
6. experimentos/balance_nuevo/pre_a08_elite_v39/QA_V39_GIT_SUMMARY.json
7. experimentos/balance_nuevo/pre_a08_elite_v39/GATE_DECISION_NEXT_ELITE_V39.json
8. La documentación de adquisición real de habilidades y el handoff histórico handoff/lii-monsters-close-2026-10-08.
9. Backup ZIP local completo y el MANIFEST para código/runners y CSV brutos; verificar SHA256 antes de ejecutar.

**DECISIONES HUMANAS FIRMES:**
- Lanza que Parte Nubes: **en LianQi II 5 Qi**, con Eficiencia T1 **4 Qi**; en LianQi I conserva **6 Qi**. V36: Lanza T1 DIRECT 30%, T1 PRECISION 2d4+4, Paso de Nube T1 EVASION 45. **Sin sangrado**.
- Seis monstruos normales cerrados V35, no reabrir. Jabalí Embestida 1d3+8, Búho Picado 1d2+8, Zorro EVA21, Cangrejo Pinza 1d2+8, Murciélago Pulso 1d2+6, Araña HP75.
- Sobretúnica patrulla **DEF+2/HP+2**: mejor vestidura pesada de la etapa y NO nerfear. El equipo avanzado debe recompensar al jugador.
- Veneno -10% recuperación de Qi fuera de combate elegido; estado de implementación separado, pendiente. No inventar estados ni alterar economía.
- LI sin defensivas ni Tramo I; LII con defensivas y Tramo I, sin AOE; guardianes de manual AOE corresponden a LIII.

**ÚLTIMO HALLAZGO, V39 ECO E8, ELITE NO APROBADO:**
- Candidato E8 recuperado de autoridad histórica: HP84, precisión96, evasión18, defensa1, tenacidad18, básico 1d2+4. **Control sigue sin recuperar**, diagnosticado control=0 solo en el LAB. Eco sigue PENDING_INTEGRAL_REBALANCE, técnica especial null y T1/T2 BLOQUEADOS. No declararlo READY.
- V39: **18.240 combates nuevos T0** (9.120 discovery, 9.120 holdout), 2.160 COLD exactos, 0 timeouts. LianQi I con kit prólogo y solo ofensiva contra Eco gana **9,69%**. LianQi II con prólogo solo ofensiva **69,43%**; post M03 con defensiva hipotética **81,41%**; LII con Sobretúnica M04 opcional y defensiva hipotética **98,80%**.
- En HTML ver74: Eco vive en cruce_vetas, sala oculta; existe ruta desde patio_raices sin gates cerrados (20 movimientos), salida final terraza_cantera --sur--> cruce_vetas. Ocultar el botón de la salida **NO impide** ingresar el comando: bloqueoPaso no exige LII en esa arista. Verificar ver76 antes de declarar bug productivo; no modificar ROOMS.exits.
- Dilema todavía SIN decisión humana: ¿se permite voluntariamente enfrentarse temprano a Eco como secreto de alto peligro o se condiciona iniciar su combate a reconocimiento/progreso ya existente, sin prohibir exploración?
- No subir arbitrariamente daño/vida de Eco para ganarle a DEF2: evaluar su identidad de élite espiritual, una técnica real con contra-juego y acceso correcto. El 98,80% no autoriza nerfear Sobretúnica.

**SIGUIENTE TRABAJO**: auditar primero la cronología real del encuentro, equipo y habilidades obtenibles; comprobar gate en versión productiva sin cambiarlo. Luego diseñar 2–3 opciones de presión especial del élite como HIPÓTESIS LAB, separando riesgo LI y desafío LII; no generar 100.000 peleas innecesarias ni repetir V02/V37/V38/V39. Respetar V38 aprobado como baseline. Someter cambios narrativos/de acceso y estadísticas a aprobación humana antes de implementar. Hacer QA COLD reproducible, manifiesto SHA y dictamen nuevo (V40) solo si hay materia prima verificada.

Si el usuario pide continuar, avanzá con verificación y propuesta contextual inmediatamente. No reabrir cierres ni pedir repetición de información. Al final de cualquier V40, actualizar handoff, nuevo backup y documentación en la rama experimental. 
