# PRE-A08 V25 — Balance puro / eficacia de Embalse
**2026-10-09 · LAB PASS / NO CANON / SIN ECONOMÍA / SIN RUNTIME**

## Autoridad
Retoma V24 y V17 sin reabrir V17–V24. Monstruos V19 originales y Sobretúnica DEF2 actual frente a DEF1 candidata. El frente de comercio/precios no se estudia ni se modifica. No A08, HTML, A07, main, merge ni ROOMS.exits.

## Batería física Embalse
6 monstruos normales; SOLO raíz Agua con eco Tierra (TIERRA_TO_AGUA); T1/T2 adaptativos; 16 builds; 2 políticas EARLY/DELAYED_TRIGGER; 3 kits M03, COAT_DEF1, COAT_DEF2.
Pareos de 5 brazos: OFF, V17 escala 0,15 y sensibilidades DIAGNÓSTICAS 0,30, 0,60, 1,00. **0,30/0,60/1,00 NO SON CANDIDATOS**.
DISCOVERY semillas 99700–99703: 23.040 duelos nuevos. HOLDOUT 99800–99803: 23.040. Total **46.080**, sin timeout ni due_missed, capacidades de monstruos restauradas. COLD 99700 **5.760/5.760 filas reproducidas exactas** salvo etiqueta cohort; no se suman a combates nuevos. Contextos de cinco brazos pareados: **9.216**.

| Comparación contra OFF | Cambios en victoria | HP final diferente | Absorción métrica diferente | Absorción liberada total | Diferencia de absorción realmente contabilizada |
|---|---:|---:|---:|---:|---:|
| V17 0,15 | **0** | 21 | 24 | 1.786,160 | 4,548 |
| Diagnóstico 0,30 | **0** | 21 | 24 | 3.330,123 | 6,380 |
| Diagnóstico 0,60 | **0** | 21 | 24 | 5.798,732 | 6,848 |
| Diagnóstico 1,00 | **0** | 21 | 24 | 7.752,992 | 6,848 |

**Hallazgo:** reserva almacenada/liberada ≠ daño absorbido posteriormente. Embalse funciona en secuencia sintética de dos golpes (libera 0,5 y evita 0,5 del golpe siguiente), pero su consumo útil es prácticamente nulo en estos duelos 1v1. No incrementar escala ni promover un fix sin auditar el orden recarga→golpe→liberación→siguiente golpe→expiración.

T2 OFF (y todos los brazos ON sin cambios de victoria): M03 66,21%; COAT_DEF1 69,34%; COAT_DEF2 88,09%; 1.536 combates por kit y brazo. La Sobretúnica DEF+1/HP+2 **sigue candidata** y NO se ha aprobado ni aplicado.

## Secuencias sintéticas, NO batallas de monstruos
12.000 contextos, 36.000 trayectorias pareadas de motor de absorción (un golpe o tres golpes por ronda durante como máximo tres rondas; 3 kits, 3 brazos). V17 Embalse aporta 1,20–1,36 HP medio contra un golpe, pero no altera supervivencia de las 6.000 secuencias de ese patrón. Tres golpes: solo 9–11 contextos por 2.000 mejoran HP, ninguno cambia supervivencia. La escala contrafactual 1,00 sí cambia 7–9 supervivencias por 2.000 con 3 golpes; es prueba de sensibilidad extrema, **NO recomendación**. La secuencia usa daño resuelto fijo tras defensa, no IA ni ataques de monstruos.

## Concordancias condicionales — GAP honesto
V17 guarda `conditional_effects_physical_validation=false`; el adaptador físico histórico usado en V24/V25 no expone seis handlers requeridos: AGUA_TO_FUEGO INTERNAL_RESOURCE, AGUA_TO_VIENTO REACTIVE_RESPONSE, METAL_TO_AGUA y VIENTO_TO_AGUA QI_COST_PERCENT, METAL_TO_FUEGO y TIERRA_TO_FUEGO INTERNAL_RESOURCE(CALOR). **6/6 escenarios bloqueados, NO físicamente testeados**. Prohibido declarar PRE_COST, ROUND_HALF_UP, prioridad y respuestas como QA superado sin adaptador. No extrapolar desde BASE.

## Próximo gate
Diseñar y auditar adaptador de laboratorio para condicionales, sin promoverlo al runtime; hacer event-trace de absorción Embalse antes de tocar números; después persistencia de veneno/quemadura y antídotos con contrato real. No freeze integral. V19 Cangrejo/Jabalí permanecen originales y candidatos sin ratificar; no se aplican cambios a monstruos.

## Paquete portátil
`GRULLA_PRE_A08_V25_BALANCE_PURO_EMBALSE_SENSIBILIDAD_2026-10-09.zip` (SHA256 `6be1c3a41fce22230f60dd6d0d2eb21c4d6f2ab5c293a30bed3443a6fd3ed2e8`), **114 archivos**, CRC y manifest SHA256 PASS, prueba COLD desde carpeta extraída PASS. Incluye ejecutables, raws, análisis y dependencias V17–V24. ZIP adjunto en conversación, NO subido a Git.
