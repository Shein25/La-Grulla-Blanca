# Auditoría independiente 3C.5 — REV2

**Fecha:** 2026-09-23  
**Archivos auditados:**
- Reconciliacion_3C5_NPC_REV2.md
- Matriz_Implementacion_3C5_NPC_REV2.json

**SHA-256**
- Reconciliación: `e833a81c122c4cfef5b62c219b8c1f0bcd51957a78589873bfb02f3b161746bf`
- Matriz: `10444d98da7bbd2fc0516fd65ebadf7e0ea20e22c6deb97baf793a4cdde81d1b`
- ZIP recibido: `733ec0edf2ca8bf12578c487dbf15d7d34a97885d57c1032b4b4aade8fea085e`

## Resultado

REV2 corrige correctamente la mayoría de los hallazgos de REV1, pero **todavía no se congela**. Se requiere una REV3 quirúrgica.

## Comprobaciones que pasan

- 32 NPC exactos.
- Distribución 7 autoridades / 7 intermedios / 12 funcionales / 6 compañeros.
- 0 legacy.
- 0 modo LIBRE.
- 14 salas iniciales CANÓNICAS + 18 ELECCION_TECNICA_3C5.
- Los 13 casos de leakage LI fueron corregidos.
- R1-R10 de los 32 NPC contrastados contra NPC_Arc1_Matriz_Canonica.json.
- Gao Shun R1 = SOSPECHA.
- Feng Zhi R5 = SABE.
- Luo Yan R5 = SABE.
- Ning Cai R1 conserva la ambigüedad y se justifica.
- Han Qiao R6 permanece DESCONOCIDO con justificación.
- Gao Shun EPILOGO corregido.
- Las cinco rutas de continuidad están físicamente cerradas.
- 36/36 tramos de esas cinco rutas son adyacentes.
- Qiao Ren y Wei Jian cruzan únicamente SECTA_INTERIOR.
- Wen Tao y Yu Shun separan territorio_normal de transito_tecnico correctamente.
- Para todos los NPC, posicion_valida = territorio_normal ∪ transito_tecnico.
- Ningún transito_tecnico se solapa con territorio_normal del mismo NPC.
- Ninguna sala inicial del mismo NPC está marcada como transito_tecnico.
- Todos los transito_tecnico aparecen como nodos internos de una ruta de ese NPC.
- Alias de la matriz: 0 colisiones.
- Los 12 tokens ambiguos están correctamente excluidos.

## Hallazgos residuales

### 1. Lista de NPC sin alias corto incorrecta en el MD

La matriz JSON es correcta.

Los 5 NPC sin alias corto son:
- qiao_ren
- chen_bo
- wen_tao
- ren_bo
- mei_lian

El MD, en §6.2 y §9, menciona erróneamente Han Qiao y Mei Shufen y omite Qiao Ren. Han Qiao sí tiene alias `han`; Mei Shufen sí tiene alias `shufen`.

### 2. Test nuevo de transito_tecnico formulado de forma global y falsa

El MD propone:

“Ningún nodo de transito_tecnico se usa como sala_inicial de ningún NPC”.

Eso es conceptualmente incorrecto. Una sala puede ser tránsito técnico para un NPC y territorio/sala inicial legítima de otro.

La matriz contiene casos válidos:
- `pabellon_disciplina` es tránsito técnico de Wei Jian y sala inicial de Qiao Ren/Feng Zhi.
- `patio` es tránsito técnico de Gao Shun y sala inicial de Mei Lian/Guo Chen.

Test correcto, por NPC N:
- `transito_tecnico(N) ∩ territorio_normal(N) = ∅`
- `sala_inicial(N) ∉ transito_tecnico(N)`
- todo `transito_tecnico(N)` es nodo interno de alguna ruta de N.

No imponer restricciones globales entre NPC distintos.

### 3. Ji Xueying M16 contiene una inferencia demasiado fuerte

Fuente:
- no está listada como responsable de frente;
- permanece en su posición institucional;
- la fuente de presencia dice que una posible coordinación en Consejo es presumible, no explícita.

REV2 añade: “está documentado que NO participa activamente”.

Ese cierre no está soportado. Debe eliminarse.

Texto seguro:
“No listada como responsable de ningún frente de T281; permanece en su posición institucional. Su participación activa/coordinación durante M16 no queda cerrada por esta fuente.”

También conviene reemplazar en Madre Wen la frase inferida “es razonable asumir continuidad...” por la formulación fuente: T283 sugiere un rol informal, pero no está cerrado.

### 4. Save/load no contempla explícitamente el validador exacto del baseline

ver73 mantiene validación de claves top-level exactas. Añadir `npc_version`, `posicionNPC` y `conocimientoNPC` sin cambiar `validarSave329()` haría inválido el save nuevo.

El contrato debe exigir dos conjuntos exactos:
- legacy: exactamente las claves actuales de ver73, sin las 3 NPC;
- nuevo NPC v1: exactamente claves legacy + `npc_version`, `posicionNPC`, `conocimientoNPC`.

Además:
- `npc_version === 1`;
- ambas tablas tienen exactamente 32 IDs canónicos;
- cada posicionNPC valida sala/anclaje;
- cada conocimientoNPC valida R1-R10 y valores permitidos;
- `npc_version` ausente + cualquier campo NPC presente = corrupto;
- `npc_version` desconocido = incompatible/corrupto;
- legacy válido se carga con defaults sin mutar el payload original.

`SAVE_SCHEMA_VERSION` permanece 2.

### 5. Baseline documental quedó desactualizado

REV2 todavía declara `grulla-blanca_ver72a.html`.

Desde el cierre de 3C.3, el baseline canónico es:
`grulla-blanca_ver73.html`
SHA-256:
`a66310f06fbf8c76e054df89f9d8cdf6959ac64c79400694474351c0936bc6dc`

3C.3B no alteró ROOMS, GATES ni los sistemas NPC, por lo que no hace falta rehacer la reconciliación; sí hay que actualizar el baseline objetivo antes de preparar el contrato de implementación.

## Veredicto

`3C5_REV2_CORRECTA_EN_NUCLEO_PERO_REQUIERE_REV3_QUIRURGICA`

No cambiar salas iniciales, rutas, conocimiento, categorías ni elecciones técnicas salvo los dos textos M16 indicados y el metadata de baseline.
