# ESTADO DE ARCHIVOS Y CUARENTENA — cierre 2026-10-08

## Clasificación de experimentos
**Admitidos como históricos LI/LII**
- `GRULLA_CONCORDANCIAS_MOTOR_REAL_TESTEADO_V03.zip`: resolver Python V03, motor nativo, suite 46/46 y 11.200 combates reportados. Resultado técnico, no freeze de balance.
- `GRULLA_BALANCE_MONSTRUOS_LI_LII_V01.zip`: campaña 55.680 peleas, resultado piloto sin freeze; contiene Sapo de Ceniza y Escarabajo de Hierro y cinco enemigos de LI.
- `GRULLA_LII_PENDIENTES_T0_V01/resultados/FINAL_VERIFY/eco_caido_5000_5255.csv`: 7.680 filas de candidato E8 en T0. No canon.

**CUARENTENA — NO USAR PARA LianQi II**
- `GRULLA_LII_PENDIENTES_T0_V01/resultados/FINAL_VERIFY/sapo_caldera_5000_5255.csv`: 7.680 filas (guardián AOE LIII).
- `GRULLA_LII_PENDIENTES_T0_V01/resultados/FINAL_VERIFY/rey_escarabajo_5000_5255.csv`: 7.680 filas (guardián AOE LIII).
- `GRULLA_LII_PENDIENTES_T0_V01/resultados/SCREEN_128/`: 23.040 filas mezcladas; segmentar por `monster`. **No** sumar como resultados aprobados.
- `GRULLA_LII_PENDIENTES_T0_V01/resultados/REFINE_192/`: 28.890 filas físicamente existentes, corrida interrumpida/incompleta: el log registra 28.800 peleas terminadas por candidatos hasta R12, resto sin cierre del lote siguiente; **no** tratar como 30.720 validadas.
- `GRULLA_LII_PENDIENTES_T0_V01/resultados/REFINE_R13/`: 1.920 filas experimentales del jefe excluido.
- `SMOKE`, `SMOKE2` y `FINAL_SMOKE`: diagnósticos. No sumar junto con las campañas sin comprobar seeds y duplicaciones.

## Historial de afirmaciones vs integridad
En la conversación se mencionaron «53.760 combates preliminares» para los tres pendientes. La inspección de los archivos detectó la corrida REFINE_192 truncada (28.890 filas vs lote esperado de 28.800/30.720 según candidatos), por lo que **ese total no es un conteo de ejecución de la entrega certificada**. El manifest del backup representa archivos reales e individuales, sin inflar conteos.

El registro autoritativo nativo marca `eco_caido` ELITE y PENDING, `sapo_ceniza` NORMAL READY, `escarabajo_hierro` TANK READY; ambos guardianes aún se etiquetan `native_stage=LianQi_II` por deuda de datos. Esa etiqueta **no** cambia la decisión humana LIII.

## Entrega Git
Rama separada `handoff/lii-monsters-close-2026-10-08`: 3 documentos de cierre, sin modificación a `main` ni al runtime. Resultados CSV y ZIP completos forman parte del **backup descargable del chat**, no del árbol Git, salvo que una subida posterior los incorpore explícitamente. Nunca declarar que todo el ZIP está en Git si no se verifica.
