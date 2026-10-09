# DECISIÓN HUMANA RATIFICADA — cierre Viento y seis normales LianQi II

**Fecha:** 2026-10-09  
**Estado:** **RATIFICADO / BALANCE NUMÉRICO CERRADO PARA ESTOS DOS FRENTES / PENDIENTE DE INTEGRACIÓN**.  
**Decisión del usuario:** «Entonces está bien, cerremos el balance, avancemos con el élite. Registra eso en Git para que no se te vuelva a pasar».

Este documento **prevalece como decisión humana** cuando las recomendaciones históricas V20–V36 (registradas como `candidate`, `proposal`, `not canon`) entren en conflicto. No reabrir estos parámetros en el frente del élite a menos que lo solicite explícitamente el usuario o una regresión productiva verificable requiera nueva ratificación.

## 1. Seis monstruos normales LianQi II — cifras aceptadas

| ID | Campo | Antes | **Valor ratificado** |
|---|---|---|---|
| `jabali_pizarra` | daño de Embestida | `1d3+6` | **`1d3+8`** |
| `buho_niebla_gris` | daño de Picado | `1d2+7` | **`1d2+8`** |
| `zorro_bancales` | evasión | `19` | **`21`** |
| `cangrejo_cauce` | daño de Pinza | `1d2+7` | **`1d2+8`** |
| `murcielago_resonante` | daño de Pulso | `1d2+5` | **`1d2+6`** |
| `arana_veta_sombria` | HP base | `71` | **`75`** |

V33–V35 sustentan estos valores. El perfil adaptativo T1, DOT, drenajes y cadencias permanecen congelados. **No aplicar** los antiguos candidatos de nerf V19 ni los extremos V34.

## 2. Habilidades de Viento — cifras aceptadas

La corrección solicitada por el usuario fue **mejorar sus habilidades**, no debilitar monstruos para compensar una raíz.

1. `lanza_nubes`, nodo **T1 DAÑO DIRECTO**, solo si se eligió: **`direct_pct=30`**, conforme a V17 (el 20% observado en V35 se debió a una omisión del adaptador LAB; no declarar bug confirmado de producción).
2. `lanza_nubes`, nodo **T1 PRECISIÓN**, solo si se eligió: **`2d4+3 → 2d4+4`** en su instancia compilada.
3. `paso_nube`, nodo **T1 EVASIÓN**, solo si se eligió: evasión **`40 → 45`**. Sin cambiar coste de Qi, duración ni evasión base 35 para builds que no elijan ese nodo.

V36 respalda esos dos nuevos ajustes focales y la restauración de V17; **no** subir daño de todas las builds de Lanza ni añadir crítico extra a Paso.

## 3. Equipo y expectativas del jugador

**Sobretúnica de patrulla: DEF+2 / HP+2 inalterada.** El nerf DEF+1 de V20/V31 queda **suspendido y excluido** de la entrega a Astra. El equipo superior de etapa debe sentirse como recompensa superior.

## 4. Qué significa cerrado

- Se **congela el diseño numérico** de los seis normales y de los ajustes concretos de Viento listados aquí. **NO** significa que el HTML/catálogo productivo ya incorpore las cifras; queda integración posterior y QA de paridad.
- No declarar congelado todo A08, Concordancias V25–V26, aflicciones productivas o balance de jefes/élites por extensión.
- Conservar resultados y propuestas antiguas como historial, no como autorización vigente.
- **Próximo frente exclusivamente: élite `eco_caido` (Eco del Caído)**, comenzando por recuperar el descriptor auténtico **E8** y su contexto de acceso. E8 continúa provisional, no debe canonizarse sin revisión.

## 5. Guardias

Rama `experiment/lii-tramo1-multirraiz-v08-2026-10-08`. **Sin main, sin merge, sin HTML, sin ROOMS.exits, sin A07, sin modificar precios/comercio.** Los cambios de diseño ratificados se registran ahora en Git y se implementarán solo durante la integración productiva controlada. Consultar el contrato JSON hermano para IDs exactos.
