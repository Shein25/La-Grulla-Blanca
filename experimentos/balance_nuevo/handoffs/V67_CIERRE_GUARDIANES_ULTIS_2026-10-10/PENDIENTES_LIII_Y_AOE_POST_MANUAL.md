# LianQi III — monstruos pendientes y pruebas POST_AOE

**Fecha:** 2026-10-10. **Estado:** AUDITORÍA DE ALCANCE Y PLAN, sin nuevas cifras de monstruo, sin simulaciones AOE cerradas.
**Autoridad de registro consultada:** `experimentos/balance_nuevo/monster_arc1_registry.json` en commit `45c3a9c240ea74208a0d8fd4d5be187bc817df35` (snapshot histórico T0). `native_stage` es etiqueta de perfil **NO prueba de acceso geográfico/legal al encuentro**.

## 1. Monstruos de etapa LianQi III fuera del cierre de cinco guardianes

| ID exacto | Nombre / clase | T0 histórico | Ataque principal y prioridad AOE | Decisión |
|---|---|---|---|---|
| `pez_lunar` | pez de luna sin ojos / NORMAL | `READY`; adaptación `T0–T4 CLOSED` | `Mordida de Corriente` daño directo; evasión elevada 29, DEF 2 | **Pendiente** validar impactos independientes y estrategia vs AOE; no cambiar T0 sin fallo acreditado |
| `anguila_estelar` | anguila de constelación rota / SKIRMISHER | `READY`; adaptación `T0–T4 CLOSED` | `Mordida del Meridiano Azul` daño directo + drenaje Qi 6; EVA 36 | **Pendiente** interacciones de AOE con drenaje de Qi y ventanas de energía; no buff a ciegas |
| `sombra_ahogada` | sombra ahogada del estanque / ELITE única | `READY`; `UNIQUE_T0_CLOSED_NO_T1_T4` | `Velo de Ahogo`: Veneno 1d2+2 ×3, cadencia 3 | **Pendiente** AOE contra objetivo único (×0,65) y persistencia Veneno; inmunidad a Hemorragia anatómica solo como hipótesis a ratificar |

### Exclusiones obligatorias
- `sapo_caldera`, `rey_escarabajo`, `guardian_coral` y `mantis_nube` son **guardianes de manual AOE legalmente en LIII**, independientemente de `native_stage` viejo; el quinto `custodio_eco_petreo` es guardián conceptual con T0/spawn canónico pendientes. **No contarlos como 3 monstruos adicionales sin cerrar**.
- `centinela_pluma`, `devorador_niebla` y `halcon_tormenta` figuran en el snapshot con `native_stage=LianQi_IV`, y `centinela_pluma` NO es el Custodio de Tierra. No desplazarlos artificialmente a LIII.
- Otros monstruos de LII/I solo se ensayarán si el Atlas y las reglas de acceso existentes demuestran que hay enfrentamientos POST_AOE relevantes; no crear nuevos spawns o mezclas como si existieran en runtime.
- El registro histórico no prueba que el T0 necesite **modificación numérica**: lo pendiente es **auditoría de interacción AOE y dificultad**. Reabrir freezes T0–T4 exige evidencia causal y decisión humana.

## 2. Contrato AOE obligatorio

Fuentes:
- `docs/experimentos/CONTRATO_COMBATE_ESTADISTICAS_DOT_V0_1.md` + `docs/experimentos/CONTRATO_MOTOR_EVENTOS_EFECTOS_V0_1.md`.
- `experimentos/balance_nuevo/handoffs/V66_GUARDIANES_AOE_2026-10-10/HANDOFF_V66_COMPLETO_2026-10-10.md`.

Separar dos etapas:
1. **PRE_AOE**: LianQi III antes del manual obtenido del guardián. Ningún personaje usa esa AOE. El duelo para obtener el manual no puede contar como POST_AOE.
2. **POST_AOE**: manual legalmente ganado una vez y técnica aprendida. Usar realmente sus costes, disponibilidad y adquisiciones; no regalar manual/maestría. La única Ulti de raíz principal se rige por decisión V67 separada.

Al ejecutar una AOE:
- Con **un solo enemigo hostil real** en el alcance: **×0,65 del daño directo AOE antes de DEF**, incluso si ese único enemigo es un jefe o élite.
- Con **dos o más enemigos hostiles reales**: factor **×1 por objetivo** y sin reparto, **un único gasto de Qi por ejecución**.
- **Cada objetivo** resuelve su propia Precisión/Evasión, DEF, Absorción, Control, estados y fuentes de DOT. No multiplicar alcance ni gasto por número de impactos. Conservar `ON_HP_DAMAGE` al determinar si abre Hemorragia.
- Sin blancos extras inventados, sin atracción entre habitaciones, sin afectación de aliados o neutrales no declarada por la técnica; el número de hostiles debe ser el legalmente presente.
- Hemorragia se activa con **acción voluntaria individual**, no al inicio de turno ni por perder turno bajo Control. Quemadura/Veneno conservan sus propios eventos. No crear ticks duplicados al haber varios objetivos.
- Cualquier Eco, Concordancia y efecto especial sigue la autoridad de eventos: no multiplicar por N un evento que contractualmente ocurre una sola vez.

## 3. Matriz mínima de comprobación real

| Eje | Casos obligatorios | Qué demuestra |
|---|---|---|
| Fase de progresión | PRE_AOE, POST_AOE con manual legal, intento sin manual | gate sin acceso gratuito |
| Cantidad de enemigos | 1, 2 y 3+ SOLO si hay composición existente verificada; fixtures sintéticos marcados como tales | x0,65 vs x1; un pago de Qi |
| Raíz | Fuego, Metal, Agua, Tierra, Viento | cinco AOE propias y Concordancias legales |
| Perfil | `pez_lunar`, `anguila_estelar`, `sombra_ahogada`; LII accesibles si procede | DEF/EVA, drenaje Qi, Veneno |
| Motor/IA | T0 y tiers legalmente desbloqueados de repetibles; élite única solo T0 | no aplicar adaptación T1–T4 a la sombra |
| Equipo/experiencia | equipamiento realmente alcanzable, 3 builds LIII y políticas autorizadas | no inflar monstruos por equipo hipotético |
| Recursos/aflicciones | impacto conectado/fallido, absorción, muerte parcial, estados de acción | independencia por blanco |
| Resultado | victoria, derrota, HP/Qi final, TTK, daño directo y DOT por objetivo, elección y prioridad IA | balance y trazabilidad |

### Pruebas adversariales de aceptación
A. AOE contra un solo `pez_lunar`: aplicar ×0,65 **antes** de DEF, con evasión por tirada.
B. AOE contra dos hostiles **solo en fixture identificado o ubicación verificada**: ambos reciben ×1, Qui una sola vez y tiradas separadas.
C. `anguila_estelar` reduce el Qi del personaje según su habilidad; NO se le atribuye AOE al monstruo si el catálogo solo declara DIRECT+QI_DRAIN.
D. `sombra_ahogada` aplica Veneno según su contrato y no adquiere T1–T4; bajo Control no duplicar ni omitir ticks incorrectamente.
E. Un enemigo muere por AOE y otro sobrevive: persistencia/target-list/AI estables; no segunda activación ni XP/drop duplicado.
F. Sin manual, comando AOE rechazado **sin consumir Qi ni acción** salvo que el contrato de intento fallido indique otra cosa.
G. AOE + Ulti principal con máximo una Ulti por pelea (la AOE es técnica normal, no debe gastar el cupo de Ulti).

## 4. Orden de ejecución recomendado — SIN inventar resultados
1. Auditar código exacto de cinco AOE, spawn/ROOM presentes y llegada legal a `pez_lunar`, `anguila_estelar`, `sombra_ahogada`.
2. Certificar eventos y pruebas unitarias 1/2/3 objetivos; comparar el resolver unitarget con AOE.
3. Recién entonces simular POST_AOE por monstruo/raíz/build/equipo/política con seeds pareadas y desgloses de daño/IA.
4. Proponer ajustes **solo** cuando un fallo/imbalance esté demostrado; conservar T0–T4 congelados y élite T0 si funcionan.
5. Preparar integración Astra A08 sin tocar `main` o HTML durante investigación.

**Estado final de este documento:** TRES perfiles LIII identificados; **cero ajustes numéricos nuevos a esos tres**, **no se ha ejecutado todavía el benchmark POST_AOE**. No confundir plan con prueba completada.
