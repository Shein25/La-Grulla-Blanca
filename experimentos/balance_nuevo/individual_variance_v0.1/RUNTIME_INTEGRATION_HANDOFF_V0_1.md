# Handoff de integración runtime — variabilidad individual / Mutante v0.4

Fecha: 2026-10-06

Estado: **HUMAN_RATIFIED_FOR_EXPERIMENTAL_RUNTIME_INTEGRATION — T1 COMPAT PASSED**

## Autoridades

- T0: `T0_LI_EXHAUSTIVE_PASS_2026-10-06`
- T1: `T1_LI_FINAL_FREEZE_2026-10-06`
- config: `monster-individual-variance-v0.4`

La validación heavy del 2026-10-01 (250.000 naturales + 50.000 Mutantes condicionados, incidencia 0,7556%) sigue siendo evidencia de que el **método estadístico y el thresholding** funcionan, pero sus combates no certifican la v0.4 porque se ejecutaron contra T0 antiguos.

## Decisiones conservadas

- `UNIFORM_0_1`;
- tiradas independientes por eje;
- T0 congelado = piso natural;
- un único `species_id`;
- Mutante <1%;
- Mutante: botín x1.5 y XP de combate x1.5;
- objetos únicos no aumentan su probabilidad;
- XP profesional no recibe multiplicador;
- Mutante no concede tiers adaptativos.

## Rebase

Los pisos fueron sincronizados al T0 final. Cuando el techo histórico quedó por debajo del nuevo T0, el eje fue colapsado al piso en vez de inventar un techo.

Identidades corregidas:
- Mono: `QI_DRAIN=6`;
- Lobo: cadencia de Emboscada = 4.

## Dificultad Mutante

No existe guardrail de win-rate mínimo para el jugador.

Una caída fuerte —incluso extrema— de la probabilidad de victoria es válida para una aparición Mutante rara. El compatibility gate sólo debe bloquear por incoherencia mecánica, identidad rota, valores inválidos, timeouts/soft-locks o por una inversión clara donde el Mutante resulte más fácil debido a un bug.

## Runtime adapter

El adapter continúa:
- clonando el perfil canónico;
- aplicando stats/ataques de instancia;
- sin mutar el registro;
- sin conceder T1–T4;
- persistiendo la tirada por instancia.

La config v0.4 volvió a status `HUMAN_RATIFIED_FOR_EXPERIMENTAL_RUNTIME_INTEGRATION` después de pasar el gate Normal/Mutante con T1. Esto habilita integración experimental, no activación automática del runtime canónico.

## Próximo gate

Debe comprobar:
1. incidencia natural <1%;
2. floors y envelopes;
3. normales y Mutantes condicionados para las cinco especies;
4. aplicación posterior de T1 congelado;
5. 0 timeout/NaN/loops;
6. identidad fija;
7. no hard-floor de win rate Mutante.

No activar automáticamente en runtime canónico tras el test: requiere cierre humano.

## Gate de compatibilidad T1 — PASS 2026-10-06

- 1.000.000 spawns.
- 102.400 combates T1.
- 0 timeouts / 0 NaN-Inf / 0 issues.
- review SHA-256: `c4e3c73f8ff907fa3b8e698bbc6ae991b9dfde1015a5eb2b439b154630b4bf34`.
- dificultad extrema de Mutantes permanece válida y no bloqueante.


---

## Regla operativa fija — artefactos pesados / Colab

Decisión humana registrada: 2026-10-06.

Para cualquier experimento, benchmark, gate, notebook o paquete de resultados preparado por el asistente:

- si el artefacto final que debe recibir/ejecutar el usuario pesa **más de 1 MB**, no entregarlo como archivo de importación directa;
- preparar en su lugar una variante **Google Colab-ready**;
- preferir un `.ipynb` autocontenido o un ZIP mínimo que contenga únicamente el notebook y, sólo si es imprescindible, assets pequeños;
- el notebook debe reconstruir/generar dentro de Colab los archivos auxiliares grandes cuando sea razonable, en vez de incrustarlos en el paquete de entrada;
- antes de entregar cualquier `.ipynb`, validar que sea **JSON de notebook real (`nbformat 4`)**, que todas sus celdas sean válidas y que pueda parsearse correctamente;
- si el notebook se entrega dentro de ZIP para evitar transformaciones del navegador/importador, indicar claramente qué `.ipynb` debe extraerse y subirse a Colab;
- conservar seeds, parámetros, CRN, perfiles y guards del experimento original salvo decisión humana explícita;
- esta regla aplica a los frentes de balance/monstruos/técnicas/Ultis y futuros laboratorios pesados;
- no implica tocar `main`, merge ni runtime canónico.

Motivo: el flujo del usuario presenta un límite práctico de **1 MB para importación** en algunas interfaces. Colab queda como vía por defecto para artefactos que superen ese límite.


### Regla de rutas por backend

Decisión humana registrada: 2026-10-06.

- Notebook **Google Colab**: usar únicamente rutas relativas o rutas bajo `/content/...`.
- Notebook **Kaggle**: usar únicamente rutas bajo `/kaggle/input/...` y `/kaggle/working/...` cuando corresponda.
- Prohibido entregar un notebook Colab que contenga rutas `/kaggle/...`.
- Prohibido asumir que Colab resolverá mounts o paths de Kaggle.
- Si se mantiene una misma lógica para ambos backends, separar explícitamente los launchers/configuración de paths por backend.
- Validar antes de entregar: grep/check automático de rutas incompatibles con el backend objetivo.


---

## Cierre Mutantes/sufijos y apertura T2

Decisión humana: 2026-10-06.

La variabilidad individual + Mutantes + sufijos queda **congelada para laboratorios T2**.

Contrato:
`suffix_lab_v0.1/MUTANT_SUFFIX_CONTRACT_V1.json`

Reglas:
- cada spawn repetible es un individuo distinto;
- T0 es piso natural, no ficha normal fija;
- q_axis se tiran una sola vez por instancia;
- Mutante y subtipo emergen de esa misma conjunción;
- CENTER: A15/F25/C20/I25/V2;
- Excepcional = 2 ejes q>=0.95;
- Ascendido = 3+ ejes q>=0.95;
- Excepcional/Ascendido heredan CENTER de sus grupos extremos.

El siguiente frente permitido es **T2**. Debe usar individuos aleatorios y esta taxonomía desde el primer micro-screen.

Nota de autoridad T2:
- la arquitectura poblacional vigente define T2 = RECONOCIMIENTO / memoria persistente / anticipación elegible;
- el contrato histórico de Rata R2_SHORT conserva identidad útil, pero sus referencias T1 +40/CD5 son obsoletas frente al T1 final +70/CD6;
- por tanto T2 debe revalidarse sobre `T1_LI_FINAL_FREEZE_2026-10-06`, sin transplantar numeración vieja.


---

## Estándar UI Colab — panel único

Decisión humana / corrección visual: 2026-10-06.

Los notebooks Colab de experimentos pesados no deben usar `tqdm.write()` ni salidas auxiliares que fuercen re-render de una barra activa.

Estándar desde T3:
- un único panel actualizable mediante `IPython.display(..., display_id=True)` / `update_display`;
- una sola barra visual;
- ancho compacto;
- especie/fase actual;
- progreso n/total y porcentaje;
- CPU por worker o CPU total resumida;
- RAM;
- peleas/s;
- ETA;
- último checkpoint;
- errores/issues;
- no imprimir telemetría repetitiva debajo de la barra.

Objetivo: evitar barras duplicadas/fantasma propias del render de `tqdm` en Google Colab.

La telemetría y checkpoints no cambian; sólo cambia la presentación.
