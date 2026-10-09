# Handoff del perfil V17 para balancear seis monstruos normales de LianQi II

**Estado:** línea base de laboratorio V17 **FIJA** para el siguiente frente. No es ratificación canónica del HTML; no enviar aún a Astra A08.

Las autoridades numéricas para el jugador son `PROFILE_LII_BALANCE_V17.json`, `CONCORDANCIAS_DEF_LII_V17_CANDIDATE.csv` y `RESOLUCION_HOOKS_TRAMO_I_V17.csv`. El dictamen y la QA V17 acompañan estas tablas. El archivo ZIP reproducible entregado en la conversación incluye los corredores originales y sus archivos fuente, pero **no está subido a Git**.

## Orden inmediato

1. Usar el **perfil V17 sin retocarlo durante los tests de monstruos**. LianQi II: dos puntos de Tramo I, una ofensiva y una defensa BASE por raíz; sin AOE. LI conserva cero puntos, ninguna defensa ni AOE.
2. Comparar Jabalí de Pizarra, Búho de Niebla Gris, Zorro de Bancales, Cangrejo de Cauce, Murciélago Resonante y Araña de Veta Sombría, manteniendo inicialmente sus stats T0/T1/T2 como controles.
3. Separar equipos `POST_M03`, `LI_CARRYOVER` y `EXPECTED_STAGE`. No asumir acceso a piezas no documentadas; medir por raíz, 16 builds legales, política, especie y tier con semillas pareadas.
4. Aplicar perfiles de Concordancia BASE solo donde el runner la soporte. **No considerar que los 24 casos donde ganó hook condicional se ejecutaron físicamente** en V17, ni combinar por suma las ganancias de Placa/Embalse V16 con ON escalar V17.
5. Proponer ajustes focales de los monstruos únicamente tras revisar colas de dificultad y curvas de equipo. Evitar compensar con estadísticas un coste de técnica extranjera aún no documentado.
6. Después del balance de monstruos, cerrar equipo y economía y recién entonces preparar paquete A08 para Astra con números ratificados, reglas y regresiones.

## Condiciones preservadas

Sin tocar `main`, sin merge, no modificar HTML, monstruos, equipo, misiones, `ROOMS.exits`, NPC o comerciantes. Sin élites ni T3/T4 en la batería de seis normales. El nivel de cultivo no equivale al tier adaptativo de monstruos.

## Integración posterior

A08 deberá probar correspondencia evento por evento de los hooks condicionales, transformaciones estructurales, PRE_COST y aprendizaje/coste real de artes ajenas. La tabla NUMÉRICA V17 es una propuesta técnica que todavía requiere ratificación humana antes de convertirse en canon.
