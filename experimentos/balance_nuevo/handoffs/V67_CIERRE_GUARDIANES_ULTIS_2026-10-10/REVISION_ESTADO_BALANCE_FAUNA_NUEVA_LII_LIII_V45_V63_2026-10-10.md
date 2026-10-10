# Auditoría del estado de balance de fauna nueva LianQi II y III — 2026-10-10

**Autoridad:** informativa; NO es ratificación de parámetros ni modificación productiva.
**Índice de identidades canónico:** `experimentos/balance_nuevo/CATALOGO_CANONICO_MONSTRUOS_ARCO1_V3.json` — **31 identidades** (18 antiguas + 6 nuevas LII + 6 nuevas LIII + Custodio de Tierra).
**Fuente histórica de resultados LIII:** documentos reales V45, V46, V47, V48, V63 preservados/recuperados para la revisión. Fuentes originales V45 y V46 están guardadas dentro de este mismo handoff. NO elevar T0 experimental a READY.

## Conclusión principal

**SÍ existe balance experimental sustancial para las seis nuevas especies LIII; NO existe evidencia de cierre humano final de los números de T0, tiers adaptativos ni Mutantes.**
La aprobación humana V46 comprende sus **identidades y diseños**, NO las magnitudes numéricas de T0 V45 ni T1→T4 V46/V47.

La aprobación de los seis nuevos repetibles LII V35, por el contrario, sí fue **numérica**: seis valores específicos ratificados en `experimentos/balance_nuevo/handoffs/CIERRE_RATIFICADO_VIENTO_Y_NORMALES_2026-10-09/DECISION_HUMANA_CIERRE_LII_NORMAL_Y_VIENTO_2026-10-09.json`, todavía pendientes de integración/paridad productiva. No extrapolar esa ratificación a T3/T4 de LII ni a los seis nuevos LIII.

## Evidencia por fase (combates NUEVOS y sujetos realmente comparados)

| Campaña | Combates | Alcance | Estado |
|---|---:|---|---|
| V45 | 219.240 | 6 especies nuevas LIII; T0 1v1 sin AOE/Ultis | T0 numérico candidato; QA PASS |
| V46 | 15.360 | 8 especies LIII (2 antiguas + 6 nuevas); piso vs Mutante condicionado T0 | Mutantes/variación preliminar, sin freeze |
| V47 | 48.000 | 2 especies LII previas + 8 LIII, T0→T4 normales/Mutantes condicionados | implementación funcional de laboratorio, 0 freeze |
| V48 R64 | 2.054.400 | 2 LII anteriores + 8 LIII; equipo, Tramos, tiers, mutantes, consumibles | QA experimental PASS, NUMERIC NOT FROZEN |
| V63 | 129.024 | 8 LIII, 5 raíces, builds de 4 PT, T2/T3/T4, normal/mutante | CANDIDATE_PASS_LIII; no canon, no AOE real multiblanco |

**No sumar COLD/reproducciones a combates nuevos; no atribuir 2.054.400 solo a las seis nuevas; también hay Pez, Anguila y dos especies anteriores de LII en esa batería.**

## Resultados T0 V45: porcentaje de victoria del JUGADOR

Equipos máximos de LII, no equipo LIII entregado gratis. Por celda especie × equipo `n=2520` (5 raíces ×7 builds ×2 políticas ×36 semillas). Las dos columnas proceden del HOLDOUT2 final independiente de V45.

| ID | Nombre | LII máximo DEF | LII máximo EVA | Con M08 torso opcional, solo estrés de progresión |
|---|---|---:|---:|---:|
| `garza_bruma_roca` | Garza de Bruma de Roca | 84,52 % | 71,67 % | 94,40 % |
| `cangrejo_laja_humeda` | Cangrejo de Laja Húmeda | 77,94 % | 56,75 % | 94,52 % |
| `sanguijuela_remanso_turbio` | Sanguijuela de Remanso Turbio | 81,23 % | 65,87 % | 92,42 % |
| `salamandra_filtracion_tibia` | Salamandra de Filtración Tibia | 83,29 % | 67,46 % | 95,20 % |
| `rana_cascajo_barranco` | Rana de Cascajo del Barranco | 83,77 % | 67,98 % | 95,71 % |
| `carpa_lamina_reflejo` | Carpa de Lámina Reflejada | 86,67 % | 72,70 % | 97,06 % |

V45 prueba viabilidad T0, NO un umbral mínimo de dificultad universal. M08 es hipotético/opcional. Los seis `stats_status` y `technique.params_status` permanecen `PENDING_INTEGRAL_REBALANCE`. El `Control=0` de V45 es hipótesis, no dato ratificado.

## Riesgos posteriores relevantes

**V47 (T4, equipo máximo LII DEF):** Cangrejo normal T4 = 52,92 % de victoria del jugador vs Mutante T4 condicionado = 15,83 %. Sanguijuela normal T4 = 45,00 % vs Mutante T4 condicionado = 13,75 %. Estos brazos no representan incidencia natural.

**V48 R64 (T4 Mutante, mismo equipo LII máximo DEF):** Sanguijuela = 15,16 %; Salamandra = 21,56 %; Cangrejo = 25,23 %. Mutantes se **sobremuestrearon** intencionalmente (≈50 % de la cohorte de estrés) frente a una incidencia natural estudiada cerca de 0,75 %; no usar los promedios condicionados como probabilidad de ganar contra fauna cotidiana.

**V48 raíz y equipo:** ocho LIII T4 normales, build `OFF_II_DEF_II`, equipo máximo LII DEF: Fuego 97,75 %, Tierra 82,91 %, Agua 76,76 %, Viento 61,13 %, Metal 49,80 %. Diferencia importante por raíz, Concordancias OFF. La túnica M08 puede producir breakpoints de DEF plana; no inflar monstruos para neutralizar equipamiento opcional.

**V63:** nueva batería de 129.024 duelos LIII 1v1 con ocho especies y cambios candidatos de técnicas/raíces. Señala que Sanguijuela T4 Mutante puede ser muy difícil para Metal (~6,2 % victoria), y que Salamandra presiona todas las raíces. V63 declara `CANDIDATE_PASS_LIII`, **no** `RUNTIME_APPROVED` ni `CANON`. No convalidó por sí solo un T0 READY para las seis especies ni T1–T4.

## Estado exacto y próximos gates

| Aspecto | Nuevos LII V35 (6) | Nuevos LIII V45/V46 (6) |
|---|---|---|
| Identidades canónicas | SÍ | SÍ |
| Valores T0/ajustes numéricos aprobados expresamente | SÍ, seis campos V35 específicos | NO, V45 candidatos |
| T1–T4 de esos seis con freeze numérico completo | NO afirmar | NO; V46/V47 solo experimental |
| Combates físicos documentados | SÍ, V33–V35 | SÍ, V45–V48/V63 |
| AOE 2+ blancos frente a ellos | NO DEMOSTRADO | NO DEMOSTRADO |
| Fichas/spawns integrados en HTML | NO VERIFICADO | NO; V45 placement preview condicionado a gate NEW |

**Próximo orden**: (1) reconciliar identidad + T0 propuesta, confirmar huecos de Control/atributos; (2) revisión focal por raíz de Sanguijuela, Salamandra y Cangrejo y acceso/equipo reales, sin nerf global; (3) decisión humana explícita sobre T0 por especie; (4) congelar T1, T2, T3, T4 y Mutantes SECUENCIALMENTE tras paridad de eventos; (5) validar AOE 1/2/3 blancos en resolver autorizado POST_MANUAL. No repetir las 2.054.400 peleas V48 salvo bug o nueva hipótesis causal.

Fuentes de respaldo V45/V46 completas:
- `FUENTE_IMPORTADA_V45_NUEVA_FAUNA_LIII_2026-10-09.md`
- `FUENTE_IMPORTADA_V46_CADENA_ADAPTATIVA_LIII_2026-10-09.md`
Documentos posteriores identificados en la Biblioteca de esta conversación: `DICTAMEN_V47_IMPLEMENTACION_MECANICAS_2026-10-09.md`, `DICTAMEN_INTEGRAL_V48_R64_5_SHARDS_2026-10-09.md`, `DICTAMEN_V63_CIERRE_LIII_Y_APERTURA_BOSS_AOE.md`.

**Guardias:** no main, no merge, no runtime/HTML, no spawns/rooms, no sobrescribir ratificaciones V35/LI/guardianes, no declarar AUTO_READY.
