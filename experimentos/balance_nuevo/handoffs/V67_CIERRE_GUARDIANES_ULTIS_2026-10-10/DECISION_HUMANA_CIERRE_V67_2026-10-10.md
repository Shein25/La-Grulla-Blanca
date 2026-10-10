# DECISIÓN HUMANA V67 — cierre de balance de guardianes y Ultis Metal/Viento

> **ENMIENDA URGENTE — 2026-10-10:** El índice V2 reúne **25 identidades verificadas, PERO NO es el total canónico definitivo**. Por confirmación humana, existen además **nuevos monstruos repetibles creados para LianQi III** que NO fueron incorporados aún porque faltan por recuperar sus IDs/nombres desde la fuente de creación. El total correcto queda **PENDIENTE**. Tanto «18 monstruos en total» como «25 monstruos en total» son afirmaciones inválidas. Las nuevas especies de LianQi II Y III forman parte del canon por decisión humana; la falta de identificación en el índice es una tarea de recuperación, no una exclusión.

> **AUTORIDAD CANÓNICA DE MONSTRUOS (2026-10-10):** el inventario histórico de **18** se encuentra **DEPRECADO COMO TOTAL**. Usar siempre `experimentos/balance_nuevo/CATALOGO_CANONICO_MONSTRUOS_ARCO1_V2.json` y `experimentos/balance_nuevo/CATALOGO_MONSTRUOS_AUTORIDAD_ACTUAL.md` (25 identidades verificadas = 18 históricas + seis repetibles LII V35 + Custodio LIII). Las menciones a «registro de 18 perfiles» solo identifican la fuente numérica histórica, nunca el catálogo total válido. No reabrir T0 por esta incorporación.

**Fecha:** 2026-10-10. **Repo:** Shein25/La-Grulla-Blanca.
**Rama experimental única:** `experiment/v67-cierre-guardianes-ultis-aoe-2026-10-10`, creada desde V66 HEAD `9264381e60843d4e77604f27a75f93e00c24a4cf`.
**Autoridad:** el autor declara terminado el frente de **rebalanceo de los cinco guardianes AOE** para seguir con monstruos ordinarios de LianQi III, y **APRUEBA expresamente** las variantes moderadas `METAL_CANDIDATE_SOFT_M02` y `VIENTO_CANDIDATE_SOFT_W01` para el diseño de balance.
**Estado de implementación:** NUMÉRICO_APROBADO / PENDIENTE_DE_INTEGRAR_Y_VALIDAR_EN_RUNTIME. No confundir decisión humana con código HTML modificado.

## 1. Ultis APROBADAS por decisión humana

Fuente estructurada obligatoria: [`BALANCE_ULTIS_METAL_VIENTO_APROBADO_V67.json`](BALANCE_ULTIS_METAL_VIENTO_APROBADO_V67.json). Los originales V03.1 no se sobreescriben ni eliminan; los nuevos números prevalecen **al integrar estas DOS Ultis**.

### Metal — `METAL_SENTENCIA_FILO_CELESTIAL` / Sentencia del Filo Celestial
Variante `METAL_CANDIDATE_SOFT_M02`.
- Un golpe inicial con escala de **50% de su rango original 12–40**, +30 Precisión original.
- Penetración **adicional** de esta Ulti **90 → 45 puntos porcentuales**, aplicada también al remate; NO sustituye la penetración normal del personaje.
- Hemorragia **3×potencia4×3 acciones → 1 carga de potencia 1 por 2 acciones voluntarias**; exige daño real a Vida; absorción y anatomía pueden impedirla.
- Mantiene **Punto de Ruptura** con su condición de dos activaciones reales de Hemorragia, ataque Metal conectado, ausencia de nueva tirada de evasión, daño sin crítico y **remate al 50%** de la fórmula original `14–20 + 4 * cargas restantes`.
- **Coste 16 Qi** y **una Ulti máxima por combate**. No editar las técnicas normales Metal.

### Viento — `WIND_VENDAVAL_MIL_HERIDAS` / Vendaval de las Mil Heridas
Variante `VIENTO_CANDIDATE_SOFT_W01`.
- **Conserva dos cortes en una sola acción** (originales `18–26` y `22–32`), con sus reglas de Precisión/crítico; cada paquete directo a **45% del original**.
- **Una Hemorragia de potencia 2 por corte que dañe Vida**, máximo **2 cargas** de esta Ulti, por **2 acciones voluntarias** cada una (máximo teórico 8 DOT base si conectan ambos).
- Si solo uno de los dos cortes abre herida, mantener **+2 adicional únicamente en la primera activación de esa herida**, conforme al candidato W01; no convertirlo en daño permanente.
- Coste **16 Qi**. No alterar técnicas normales Viento ni el máximo universal de 4 cargas.

### Reglas comunes de acceso
LianQi III permite solamente Ulti de la **raíz principal**, con maestría completa `APRENDIDA_AL_MAXIMO` comprobada, sin deducirla de los PT activos. LianQi IV puede habilitar la del injerto, pero el máximo global sigue siendo **una Ulti por combate**. No regalar Ultis para validar resultados.

## 2. Resultados de soporte (adaptador físico E1 V67; NO runtime HTML final)
Batería V67-D: 720 combates por cruce raíz/guardián (3 builds, 2 equipos, 3 políticas, 40 semillas), más controles y sensibilidad. Fuentes selladas:
- Backup V66 SHA-256 `e8402ca195ba9f2d4fe97ae4a71351d25f691c7601a81c49693cdf77198d3a39`.
- Backup Ultis V03.1 SHA-256 `8c18d8f3aaecfe887e76fd7d410ca803bb7c499f0584b00c318bf75122337f0e`.
- Laboratorio completo `GRULLA_V67_BALANCE_ULTIS_METAL_VIENTO_2026-10-10.zip`, SHA-256 `d4214f3bdf668699d4d89e463a57709e8ea5eb3f50ad19fcca96c16ed6695465`, **ZIP externo, no incluido en Git**.

| Combate por manual de la propia raíz | Solo técnicas V66 | Ulti original V67-C | Ulti ajustada APROBADA |
|---|---:|---:|---:|
| Metal vs Rey Escarabajo | 63,47% | 100,00% | **78,89%** |
| Viento vs Mantis | 56,81% | 100,00% | **77,08%** |

Los ajustes dieron **0 eliminaciones hasta ronda 3 en esos cruces**; esta métrica es **ronda de laboratorio, no validación de <=3 acciones efectivas de jugador**. En el adaptador, Metal mantiene posibilidad/activación de remate. No tratar el 100% previo como paridad productiva demostrada.

## 3. Guardianes AOE: cierre de este frente de BALANCE, sin falsificar estado productivo
Cinco identidades: `sapo_caldera`, `rey_escarabajo`, `guardian_coral`, `mantis_nube`, `custodio_eco_petreo`.
- Decisión humana: **dejar de reequilibrar globalmente HP/DEF** de estos cinco, mantener el estado probado y avanzar al siguiente frente. Las técnicas y Ultis pueden explicar resultados sin inflar estadísticas.
- Cuatro T0 históricos ratificados del commit `45c3a9c240ea74208a0d8fd4d5be187bc817df35` **no se editan ni se sustituyen por overlays V65**. Cierre de balance **no equivale** a haber hecho merge/patch de esos T0.
- `custodio_eco_petreo` tiene identidad aprobada, pero el T0 numérico canónico, manual y spawn de runtime **siguen sin ratificarse/integrarse**. Nunca sustituir por `centinela_pluma`.
- Inmunidad al sangrado de `guardian_coral` y `custodio_eco_petreo`: **fixture candidato de las comparaciones**, aún no ratificado como flag de registro/runtime. Las tasas de Metal/Viento cambian materialmente si se desactiva; preservar BOTH brazos al validar.
- Guardianes únicos; se accede legalmente en **LianQi III** aunque algún `native_stage` histórico sea LII/LIV; sin respawn, sin T1–T4 persistentes, manual una vez, sin nueva habitación ni gate inventado.

## 4. Trabajo todavía abierto: paridad/integración
La decisión aprueba **números** y cierra la iteración de balance, no certifica que E1, V03.1 y HTML coincidan evento por evento. Astra deberá: integrar parámetros en un adaptador autoritativo; comprobar penetración, críticos, remate, Qi, Hemorragia, Absorción, recursos, ventanas y prioridades; respetar el gate de maestría; ejecutar regresión; pasar de laboratorio a HTML con autorización separada. Ninguna escritura de runtime en esta rama.

**Guardas permanentes:** NO MAIN, NO MERGE, NO HTML, NO `ROOMS.exits`, NO modificar T0 ratificados, spawns, economía, NPC, diálogos A07 ni reglas de adquisición sin decisión expresa.

**Siguiente frente:** [`PENDIENTES_LIII_Y_AOE_POST_MANUAL.md`](PENDIENTES_LIII_Y_AOE_POST_MANUAL.md).
