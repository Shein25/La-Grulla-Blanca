# Informe de implementación — 3C.6 Prólogo + M01–M07

**Rama exclusiva:** `implement/3c6-prologo-m01-m07`
**Base contractual:** `b0d90ea70ab17b3d6a7e85951e19f00c7935c8f2`
**Estado:** implementación candidata para auditoría independiente; sin merge.

## Archivos agregados en la rama

- `grulla-blanca_ver75.html` — runtime y once regresiones nuevas 3C.6.
- `docs/3C6A/PROMPT_OPERATIVO_IMPLEMENTACION_3C6.md` — límites y fuente contractual de trabajo.
- `Informe_Implementacion_3C6_Prologo_M01_M07.md` — este informe.

No se editó `grulla-blanca_ver74.html`, las ramas anteriores ni la matriz documental.

## Integridad

| Fuente | SHA-256 |
|---|---|
| Baseline `grulla-blanca_ver74.html` | `8cd2d2f51e15a433d35397fbb31035b3067f5a26bd942d890f07a0f316359566` |
| Resultado `grulla-blanca_ver75.html` | `513d7333abc6d0286603f1368198ba5595e865025995fe10331a9393f0fb8fdc` |
| Matriz REV3.1 | `96d6a73383fdd5636005460bd3483f3e6b7f8f358a5354fdaa1f76cab0e3d881` |

Comparación sobre los objetos runtime entre ver74 y ver75:

| Invariante | Resultado |
|---|---|
| `ROOMS.exits` (329 entradas) | SHA idéntico: `76ba15c0795e9a11341a0b2500584fed9faef8a4426bce847a03afd07584d759` |
| `GATES_329` | SHA idéntico: `4ab928457bdf2721cf6305b644f01a34bfb9611e8f9dfe4521007405ba7aba3b` |
| Identidad, mob, origen y territorio de errantes | SHA idéntico: `cf50c0e35fc9ae03faafd31b90c234d3712cf22786307eac3954e8833141cb41` |
| Auditor de mundo | 329 salas, 17 áreas, 787 salidas, 0 aisladas, 0 rotas, 1 componente |
| Save schema | `2` |

## Cambios de implementación

1. Catálogo `QUESTS` P–M07 con texto para la interfaz; estado `flags.arc1`, normalización y reconciliación idempotente. El primer tipo nuevo de evidencia activa M06 en la misma acción si M04/M05 ya cerraron.
2. Prólogo con tres decisiones de raíz y desempate explícito, uniforme y espada entregados una sola vez al entrar al descansillo, registro ante Tao Ming y cierre P.
3. M01 con inscripción al examinar el jade, traslado de Tao Ming a servicios, asignación por Madre Wen y confirmación al entrar físicamente al dormitorio.
4. M02 con la rata errante existente, sin botín ni registro de Atlas/bestiario durante el tutorial; cadáver protegido mientras se necesita, recreación única si falta, Examen con Chen Bo y entrega a Tao Ming.
5. M03 con enseñanza y preparación de Piel de Cobre, muñeco derivado de práctica y evaluación al meditar antes del control de vaso lleno; promoción institucional con Qiao Ren.
6. M04/M05 con checkpoints posteriores a su activación; incidente opcional determinista (+1 mérito), circuito de Sauces y píldora única protegida, con una sola reemisión posible.
7. M06 con cuatro tipos y las ocho fuentes verificadas; M07 con informe determinista, corrección institucional y actualización monotónica de R1 para cinco NPC.
8. Contribución y mérito separados en libro mayor y servicios económicos que siguen exigiendo mérito 8/20. Un expulsado no cobra.
9. `compruebaPuerta()` bloquea requisitos desconocidos; la etapa 2 exige servicio, evaluación y rango M03; la etapa 3 exige los hitos territoriales y la píldora antes de consumirla. CONSAGRAR conserva el qi previo al ampliar el vaso.
10. Migración de saves ver74 schema 2 sin `flags.arc1`, conservando recursos y progreso previo, cerrando P–M03 sin volver a pagar; si había interior abierto, queda registrado como diagnóstico y se cierra hasta la transición oficial. Carga y normalización se realizan primero sobre una copia aislada.

## Verificación

- `node --check` sobre el script embebido: **PASS**.
- 11 pruebas nuevas `3C.6` bajo Node/DOM simulado: **11/11 PASS**, incluyendo ruta P–M07, guardado intermedio, legacy etapas 1/2/3, corrupción atómica, idempotencia, evidencia adelantada, píldora y servicios.
- Suite histórica comparada con el **mismo simulador limitado**: ver74 = 398 casos / 111 no verificables o fallidos allí; ver75 = 409 casos / 111 en los mismos casos. **Cero fallos nuevos** en esa comparación. Este resultado no equivale a 409/409 ni acredita la interfaz real.
- Navegador/Chromium: **NO_VERIFICADO**. El paquete Playwright está disponible, pero no hay binario Chromium instalado en este entorno. Debe ejecutarse `GB.PRUEBAS.correr()` y comprobarse P–M07 en un navegador real durante la auditoría externa.

## Límites y desvíos

No se identificaron desvíos funcionales deliberados del contrato P–M07. La verificación real de interfaz queda pendiente. Este informe no declara cerrada 3C.6: falta auditoría independiente y cualquier integración posterior requiere autorización expresa. No hubo merge.
