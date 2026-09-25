# Encargo de auditoría externa — Motor NPC Vivo v0.3.1, relaciones derivadas

Auditar la cabeza actual de `experiment/motor-npc-v0.3-memory`, carpeta `experimentos/memoria/motor-npc-vivo-v0.3.1-relaciones/`. Registrar el SHA exacto. La v0.3.0 de `experimentos/memoria/motor-npc-vivo-v0.3-memory/` está congelada en `340d6ec0d2402eae2bd4b1b306b4e6f05c39a623`; verificar que sus blobs no cambiaron. No modificar juego principal, Utility AI, GOAP, Executor, v0.3.0, NPC canónicos ni topología canónica. No hacer merge ni marcar ready/cerrar PR #4.

## Comprobaciones

1. Leer `README.md`, `CAMBIOS_v0.3.1.md`, `relation-deriver.mjs`, `tests.mjs` y `stress.mjs`. Confirmar que la capa obtiene recuerdos activos exclusivamente a través de `recallMemory()` y no lee `memory.entries` para decidir vigencia.
2. Ejecutar `node tests.mjs` y reportar PASS/FAIL reales y exit code. Repetir `node stress.mjs 1000 SEED` para `1337`, `1`, `42`, `999`, `20260924`; reportar por seed calls, eventos, contribuciones, ignorados, digest y exit code. Confirmar que misma seed produce el mismo resultado.
3. Ejecutar la regresión congelada v0.3.0: `node tests.mjs` y `node stress.mjs 10000 1337` desde su carpeta. Verificar 29/29 y ausencia de diferencias de blobs en esa carpeta.
4. Auditar casos de ayuda verdadera (+12 afinidad, +10 confianza, +8 deuda) y mentira verdadera (−18 confianza, −6 respeto, +12 rivalidad); todas las demás relaciones deben recibir cero. Verificar factor `(importance/100)*(confidence/100)` con 50/80, ceros, varios recuerdos, decimales y ausencia de bonus por `count`.
5. Verificar expiración inclusiva en `expiresTurn`, rechazo de reloj regresivo, `value !== true`, kinds sin regla social (`ORDER_RECEIVED`, `SIGHTING_RELEVANT`, y los nombres heredados `toString`, `constructor`, `__proto__`). Distinguir recuerdo ignorado activo de recuerdo expirado, que `recallMemory()` no devuelve.
6. Probar orden invertido de entradas y factores adversariales donde el clamp por contribución daría un resultado diferente. Los deltas se agregan antes de clampear; comparar `rawDeltas`, `relations`, `contributions` e `ignoredMemories`. Buscar diferencias numéricas por orden de suma.
7. Repetir llamadas con los mismos inputs; confirmar resultados idénticos, no acumulación, inputs y resultados anteriores intactos. Mutar la respuesta y comprobar que no altera memoria ni relaciones base.
8. Atacar la frontera de relaciones: faltantes, extras, símbolo extra, heredadas, `undefined`, getter en cualquier campo, setter-only, getter+setter, accessor no enumerable, `Proxy.get` hostil, `NaN`, `±Infinity`, string, objeto, array, `-1`, `101`. Un getter no debe ejecutarse. Buscar entrada que pase validación y produzca salida no finita o fuera de `0..100`.
9. Revisar que los fixtures son sintéticos, que no se modifica Utility AI ni GOAP, y que no se implementa integración con objetivos, decay, scheduler o NPC↔NPC.

## Informe y veredicto

Describir SHA, comandos, evidencia, bugs reproducibles, límites de diseño y alcance de la regresión. Terminar exactamente con **uno** de:

```text
V031_RELATIONS_APTO_PARA_ITERAR
V031_RELATIONS_REQUIERE_CORRECCIONES
V031_RELATIONS_FALLO_CONCEPTUAL
```

No aprobar merge automáticamente.
