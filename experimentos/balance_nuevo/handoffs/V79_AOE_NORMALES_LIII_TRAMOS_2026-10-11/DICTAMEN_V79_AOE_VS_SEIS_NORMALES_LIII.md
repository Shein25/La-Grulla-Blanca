# V79 — AOE frente a normales LianQi III y evaluación de Tramos I/II
**Fecha:** 2026-10-11. **Estado:** `E1_1v1_PARITY_PASS / SYNTHETIC_1vN_FULL_COMBAT / NO_CONCORDANCE_NUMERIC_ON / NO_HTML_PARITY`.

## Respuesta al autor

**Aún no es correcto aumentar indiscriminadamente los Tramos I/II de las cinco AOE.** Los Tramos de daño sí incrementan el daño real por ejecución, pero una AOE repetida en duelo (multiplicador contractual ×0,65 ante único hostil y 8–11 Qi por uso) funciona mucho peor que una técnica unitarget. Dos o tres normales LIII *simultáneos* castigan severamente incluso a un personaje que NO usa AOE y aun cuando abre con defensa. Esas formaciones son **sintéticas, no spawns confirmados**. Antes de rediseñar cifras hay que comprobar composición legal de encuentros, magia extranjera adquirida y Concordancias ON con manifestaciones efectivas.

## Autoridad de enemigos / jugador

- Seis normales propios de LIII con identidades reales: `garza_bruma_roca` (75 HP), `cangrejo_laja_humeda` (90), `sanguijuela_remanso_turbio` (78, veneno), `salamandra_filtracion_tibia` (79, quemadura), `rana_cascajo_barranco` (84), `carpa_lamina_reflejo` (78, drenaje Qi). Se usan **baselines T0 numéricos V45 seleccionados en V67**, aún **no productivos**; Control=0 sigue hipótesis seleccionada. Ningún T0 ni spawn alterado.
- LianQi III: 4 PT exactamente; 10 repartos por raíz (0 AOE, 3 variantes T1, 6 variantes T2), 5 raíces, 2 equipos: **máximo LII defensa a la entrada** y **LIII esperado opcional**, este último NO regalado al ascender. Manual de AOE propia **asumido en el fixture** y fase POST_AOE; no representa obtención real.
- **Motor:** E1/V66 físico. 1 blanco AOE ×0,65, 2/3 blancos ×1 a cada uno, Qi una sola vez por acción, impactos independientes; T0 normales atacan en su turno, con veneno/quemadura/drenaje. Grupos 2/3 creados como blancos simultáneos del laboratorio, NO encuentros/ROOM. **No se incorporan capas V61C posteriores ni paridad de producción NEW/HTML.**

## Alcance ejecutado y QA

| Suite | Combates |
|---|---:|
| Tramos y políticas, 1/2/3 blancos, 48 semillas por celda | **259.200** |
| Defensa inicial, 1/2/3 blancos, 32 semillas por celda | **69.120** |
| AOE inicial 1/2/3 veces, 1/2/3 blancos, 16 semillas por celda | **69.120** |
| **TOTAL** | **397.440** |

**1260/1260 regresiones E1 1v1 EXACTAS**, cero diferencias de victoria, rondas, HP, Qi final y Qi gastado; **0 timeouts en las 397440**. Hash SHA256 y CRC ZIP PASS; fuente portátil extraída en carpeta limpia y `verify_v79.py` ejecutado **PASS**. Escenas de un enemigo son exactamente equivalentes a E1 original en los puntos verificados; **no** afirmar paridad 1vN HTML ni Concordancia ON.

## Tasas de victoria contra un solo normal — equipo entrada LII DEF

| Estrategia de combate, siempre 4 PT legales | WR del jugador | N |
|---|---:|---:|
| Solo técnica unitarget | **81,81%** | 1440 |
| Apertura defensiva, después unitarget | **88,85%** | 960 |
| Una AOE T1 opción 0 y después unitarget | **66,46%** | 480 |
| Dos AOE T1 opción 0 y después unitarget | **54,58%** | 480 |
| AOE T2 camino (0,1) todo el tiempo | **11,04%** | 1440 |
| AOE T2 DIRECT+DIRECT todo el tiempo | **8,47%** | 1440 |
| Abrir con defensa y luego AOE T2 DIRECT+DIRECT todo el tiempo | **17,71%** | 960 |

Estos porcentajes comparan **diferentes repartos de 4 PT y políticas**, no son un contraste de una única variable causal. `T1 opción 0` es DOT en Fuego, Ruptura en Metal, Debuff en Agua/Tierra e Interferencia en Viento: NO atribuirlo a la misma mecánica. Con AOE T2 DIRECT+DIRECT reiterada, **cerca del 100%** terminan usando el básico al agotarse Qi. Debe entenderse la AOE como área/apertura de estados, no como equivalente de golpe unitario continuo.

## AOE sobre varios normales del mismo nivel — solo *fixture sintético*

En los **86400** combates completos 2v1 (jugador contra dos normales de la misma especie) de la suite principal, el jugador venció **46 (0,053%)**; en **86400** de 3v1, **0** victorias. Ni política unitarget ni defensa inicial resuelven el peligro de 2/3 normales LIII actuando cada ronda. Esto **no demuestra** que el juego realmente ofrezca esos encuentros, ni que los Tramos sean su única causa.

AOE DIRECT+DIRECT Tramo II con 2 normales y equipo de entrada: daño directo **total promedio por ejecución** (cada blanco recibe su tirada independiente, no se divide el daño): **Fuego 19,3 HP; Metal 15,6; Agua 14,8; Tierra 14,9; Viento 14,9**. Con tres: **Fuego 29,2; Metal 23,8; Agua 22,1; Tierra 22,0; Viento 22,3**. Los enemigos tienen 75–90 HP por individuo y cada sobreviviente puede atacar por ronda.

## Diferencias entre Tramos; evitar buff uniforme

Usando la AOE repetida contra UN normal, equipo LII defensivo, `T1 opción 0` / `T2 DIRECT+DIRECT`:
- Fuego: **19,10% / 18,40%**; el híbrido T2 `DOT+DIRECT` alcanzó **36,11%**, favorecido por quemadura.
- Metal: **1,39% / 4,17%**.
- Agua: **0,00% / 2,08%**.
- Tierra: **3,47% / 6,94%**.
- Viento: **4,17% / 10,76%**.

Los Tramos directos mejoran el daño, pero Agua/Metal desempeñan funciones de debilitación/ruptura que no se capturan en un ranking de daño total puro. No convertirlos en clones de Fuego ni introducir escalas en Concordancias sin autoridad.

## Estado REAL de Concordancias: pendiente

V77/V78 comprobaron física de AOE, Eco, hooks, pago único y sensibilidad hipotética de +10/+20%, **no** aplicaron el resolver completo de 20 relaciones dirigidas. **V79 no ha usado Concordancia ON numérica**, ni técnicas AOE extranjeras: todos sus WR son **sin bonus Concordancia**. Las magnitudes de algunas relaciones aún no tienen autoridad ratificada, y no existe auditoría suficiente de manuales extranjeros/acceso. No inventar porcentajes ON, ni promocionar 1vN sintético a encuentros reales.

## Dictamen y siguiente gate

1. **No retocar numéricamente ningún Tramo todavía** por estos promedios agregados: primero validar **Composición del encuentro / cantidad real de hostiles** y **adquisición del manual**.
2. Siguiente prueba focal **Marea Agua** (debuff de precisión/duración; requiere validar impacto defensivo con turnos, no solo daño), **Lluvia Metal** (DEF_SHRED / penetración), **Círculo Fuego** (DOT híbrido 0,1), **Tijera Viento** (interferencia + área) y **Temblor Tierra** (evasion debuff + preparación). Mantener contratos propios, no bonos planos.
3. Instrumentar ON/OFF con manifestaciones numéricas/estructurales aprobadas y paridad 1vN real antes de inferir si Tramos son inútiles con Concordancia.
4. Ningún cambio a V76 B Metal, Sombra V72 110 HP, Viento V67, monstruos 31 identidades, T0 originales, ROOM/exits o HTML.

**ZIP portable adjunto en la conversación:** `GRULLA_V79_AOE_TRAMOS_SEIS_NORMALES_LIII_2026-10-11.zip` — **4.555.033 bytes**, SHA-256 **`1434d167fbc91d11c55fc2fcaf00cf0f0a5e3630221e32e9d23fe2a973caf88f`**, 45 entradas, 44 hash PASS, CRC PASS, `verify_v79.py` PASS desde extracción aislada. Incluye fuente E1/V66, ejecutores, los 397440 resultados CSV completos, informes y QA; **ZIP no subido a GitHub**.

**Guardas:** NO MAIN, NO MERGE, NO HTML, NO `ROOMS.exits`, NO NPCs/spawns/gates manuales inventados, NO upgrades de monstruos.
