# V78 — Primera batería física AOE y Concordancias
**Fecha:** 2026-10-11. **Rama:** `experiment/v67-cierre-guardianes-ultis-aoe-2026-10-10`.
**Estado:** `PHYSICAL_MECHANICS_PASS__FULL_CONCORDANCE_AND_1VN_WINRATES_NOT_YET_VALIDATED`.

## Precedencia obligatoria de balances ya cerrados
- **Sentencia del Filo Celestial de Metal:** balance **V76 B**, seleccionado por el autor: apertura ×0,65; Punto de Ruptura ×0,65; penetración adicional +10pp; una carga de Hemorragia potencia 2 durante dos activaciones; coste 16 Qi. **Ronda de uso elegida por el jugador**, no fijar ronda 4.
- **Sombra Ahogada:** élite único LianQi III; diseño T0 **V72 de 110 HP**, DEF1, Espejo del Remanso 8 tras golpe de 16 HP reales, Velo de Ahogo cadencia 4 y veneno `1d2+2` ×2. **Cierre numérico de diseño**, no HTML.
- V67 histórico Metal, V67 Viento y cinco guardianes no se alteran. Inventario 31 identidades. No merge, main o código runtime.

## Batería ejecutada: 31.680 secuencias, 66.240 acciones
Reproducción física `V78` basada en E1 V66 sellado, con iteración sintética de 1/2/3 hostiles y acciones consecutivas sin turnos monstruo.

| Secuencia | Casos | Acciones |
|---|---:|---:|
| AOE de raíz A → AOE de raíz B distinta, sensibilidad +0/10/20% | 23.040 | 46.080 |
| AOE de raíz A → defensiva de raíz B distinta | 5.760 | 11.520 |
| Misma AOE ejecutada tres veces | 2.880 | 8.640 |
| **TOTAL** | **31.680** | **66.240** |

**Hallazgos estructurales:** De 20 pares dirigidos de AOE distintas, 14 exponen un hook base, y seis son `BASE NONE`. Solo cinco exponen `DIRECT_DAMAGE` y uno `AREA_EFFICIENCY`. En los demás **no se inventa bono de daño**; precisan penetración, debuff, duración, estructuras u otro canal propio. AOE→defensiva resuelve selector de hook, coste único y activación de defensa E1. Misma AOE tres veces no puede consumir Eco en relación misma raíz: son tres acciones, tres pagos, Eco sustituido y **cero Concordancias A→A**.

### Sensibilidad de daño: valores SOLO hipotéticos, no autorizados
Un `+10%` o `+20%` proporcional sobre paquete receptor se aplicó **exclusivamente en los seis pares de hook DIRECT_DAMAGE/AREA_EFFICIENCY**. El contrato permite escalado relativo, pero **las magnitudes numéricas globales no están ratificadas**, por lo que estos NO son porcentajes de mejora del juego. Daño directo promedio **total entre todos los objetivos** para la segunda AOE:

| Hook | Enemigos | Base | +10% hipotético | +20% hipotético |
|---|---:|---:|---:|---:|
| DIRECT_DAMAGE (5 pares) | 1 | 3,37 | 3,72 | 4,11 |
| DIRECT_DAMAGE (5 pares) | 2 | 10,87 | 12,09 | 13,46 |
| DIRECT_DAMAGE (5 pares) | 3 | 16,50 | 18,33 | 20,44 |
| AREA_EFFICIENCY (1 par) | 1 | 2,87 | 3,16 | 3,52 |
| AREA_EFFICIENCY (1 par) | 2 | 9,70 | 10,83 | 12,08 |
| AREA_EFFICIENCY (1 par) | 3 | 14,66 | 16,31 | 18,26 |

El motor aplica la regla ×0,65 al único objetivo y ×1 completo a cada uno con dos o más, coste de Qi por ejecución, impactos independientes. La relación Concordancia se selecciona **una vez por ActionContext**, no por enemigo. El único resultado 'on' aquí es escalado de sensibilidad limitado a estos dos hooks: **no afirmar `CONCORDANCE_ON` global**.

## QA independiente
- **600/600 comparaciones exactas** entre una AOE de un blanco y `execute_player_technique` nativo E1 (HP, Qi, DOT, absorb, estados), **0 diferencias**.
- **15/15** rechazos al no disponer del Qi; sin gasto, sin daño, sin cambio de Eco.
- **15/15** fixtures de supervivientes pasan de 3 blancos a 1; recálculo de alcance correcto.
- **5 raíces × 3 cantidades × 192 semillas** reusaron la misma AOE tres veces, con tres pagos y ninguna Concordancia consigo misma.
- ZIP **autocontenido** reproducido en otra carpeta, **4/4 CSV coincidentes byte por byte**, CRC y SHA256/manifiesto PASS.

## Límites: no confundir pruebas de contrato con balance jugable
El E1 antiguo es 1v1. V78 aplica un bucle sintético 1vN y no resuelve IA enemiga, turnos intercalados, ticks/duración DOT, muerte de jugador, tasas de victoria, control/defensiva Concordance ON ni técnicas extranjeras realmente aprendidas. Los tres hostiles son **fixtures sintéticos**, no habitaciones/spawns. `pez_lunar` y `anguila_estelar` están T0 PENDING en la fuente E1 utilizada. Los números +10/+20% son **hipótesis**, NO valores aprobados. Sin builds 4 PT completas, equipo, Ultis, SAVE/LOAD ni paridad HTML. No tocar registros T0 ni `ROOMS.exits`.

**Siguiente puerta de calidad:** resolver numéricamente los 20 pares/hook sobre motor 1vN con eventos propios y manuales realmente adquiridos; después combate completo POST_AOE con turnos de enemigos y semillas OFF/ON, un/tres objetivos y equipos legales.

### Archivo portable
`GRULLA_V78_AOE_CONCORDANCIAS_BATERIA_INICIAL_2026-10-11.zip`; SHA256 `92fd9f49c9dfeee08796ee4bf0154524b68be08cf28f45b79079e0cd3dff9476`, **204.980 bytes**, **15 entradas**, fuente E1 y catálogos adjuntos, ejecutor, cuatro CSV, QA y manifiesto. Contenedor del chat, no subido a GitHub; reproducido desde carpeta limpia.
