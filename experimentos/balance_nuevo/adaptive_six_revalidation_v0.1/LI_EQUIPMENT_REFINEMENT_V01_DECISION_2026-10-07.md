# LianQi I — Equipment Refinement V01 — Decision

Fecha: 2026-10-07
Rama: `experiment/monster-adaptive-six-revalidation-v0.1`
Estado: HUMAN APPROVED FOR MICROGATE / NO PRODUCTIVE FREEZE

## Diagnóstico desde V04B

El sistema LI ya está sano globalmente, pero el equipo muestra cuatro problemas de diseño:

1. La supervivencia básica está muy concentrada en el Uniforme gris. Esto es aceptable porque es dotación garantizada y debe tratarse como parte del baseline del aspirante.
2. La progresión opcional es desigual: HP, precisión y evasión se sienten; Tenacidad pura casi no tiene objetivo relevante en LI PvE.
3. `bandana_lino_simple` con TEN+2 queda mecánicamente casi muerta en LI y además compite en el mismo slot con `cinta_patio_aspirante` (PREC+1/TEN+1).
4. El salto EXPECTED_STAGE -> HIGH_ROLL_STRESS es demasiado tenue (~+0,74 pp ON en V04B). El principal responsable es que `colgante_fragmento_jade` y `anillo_hierro_oxidado` aportan poco combate directo. El anillo no debe retocarse todavía porque conserva utilidad de meditación pendiente; el ajuste debe recaer en el Colgante.

## Candidate pack recomendado

### Mantener sin cambios

- `espada_madera_entrenamiento`: PREC +1
- `cuchillo_hueso_callejero`: BASIC +1 / PREC -1
- `uniforme_gris_aspirante`: DEF +1 / HP +1
- `vendas_antebrazo_practica`: PREC +2
- `fajin_discipulo_externo`: QI +2
- `pantalon_viaje_gris`: HP +2
- `zapatos_suela_blanda`: EVA +2
- `anillo_hierro_oxidado`: QI +1 + meditación pendiente
- `cinta_patio_aspirante`: PREC +1 / TEN +1
- `anillo_cobre_sin_sello`: QI +1 / CONTROL +1

### Candidatos que V04B ya apoyó

- `baston_fresno_practica`: **TEN +1 / PREC +1**
  - V04B: ~+2,00 pp ON.
  - Rol: arma institucional equilibrada, mejora posterior a la espada inicial sin desplazar al cuchillo agresivo.

- `pulsera_fibra_trenzada`: **QI +1 / CONTROL +1**
  - V04B global: ~+0,44 pp.
  - Agua: ~+2,06 pp; Agua+Latigazo ~+3,13 pp.
  - Rol: especialista de flujo/control, no generalista.

### Nuevo candidato — Bandana

- `bandana_lino_simple`: **EVA +1 / TEN +1**
- Mantener en LianQi I; no mover a LII.

Justificación:
- TEN+2 casi no tiene objetivo en LI.
- PREC+1/TEN+1 sería un clon exacto de la Cinta del patio.
- EVA+1/TEN+1 crea una decisión limpia en TOCADO:
  - Bandana = defensa/movilidad.
  - Cinta = precisión/estabilidad.
- Mantiene una escala humilde propia de LI y un presupuesto mecánico comparable a la Cinta.

### Nuevo candidato — Colgante

- `colgante_fragmento_jade`: **QI +1 / CONTROL +3**

Justificación:
- CONTROL+4 probado en V04B es funcional pero demasiado tenue: ~+0,20 pp global y ~+1,09 pp en Agua+Latigazo.
- Añadir QI+1 le da un beneficio pequeño y legible a cualquier raíz sin convertirlo en una mejora universal fuerte.
- CONTROL+3 conserva su identidad especializada para Agua/control.
- Como hallazgo único de exploración puede ser algo más interesante que una pieza institucional común.
- Debe mejorar la transición EXPECTED -> HIGH_ROLL sin convertir HIGH_ROLL en obligatorio.

## Interpretación de piezas fuertes

- `uniforme_gris_aspirante` (~+22 pp): NO nerfear; es baseline garantizado.
- `pantalon_viaje_gris` (~+5,85 pp): conservar. Es una pieza clara de supervivencia, no mostró perjuicios y no reemplaza una alternativa del mismo slot en LI.
- `cuchillo_hueso_callejero` (~+5,45 pp): conservar. Es origin-only, agresivo y paga PREC -1; su potencia está contextualizada.

## Gate siguiente

Ejecutar un microgate dirigido, no otra regresión masiva.

Objetivos:
1. Confirmar Bandana EVA+1/TEN+1 frente a Cinta PREC+1/TEN+1.
2. Confirmar Colgante QI+1/CONTROL+3 frente al candidato V04B CONTROL+4.
3. Verificar que EXPECTED -> HIGH_ROLL gane una mejora visible pero moderada.
4. Confirmar que ninguna pieza opcional se vuelve obligatoria.
5. Revisar raíces/especies T0/T1 y Concordance OFF/ON con mismas semillas.
6. Mantener monstruos, técnicas y raíces congelados como controles.

Si pasa:
- congelar equipo LI;
- ejecutar Concordance NO_TRAP sobre el equipo definitivo;
- cerrar LianQi I.


## Human decision — 2026-10-07

El usuario aprueba explícitamente el candidate pack de equipo LI para validación.

Aprobado para microgate:
- `baston_fresno_practica`: TEN +1 / PREC +1
- `bandana_lino_simple`: EVA +1 / TEN +1
- `pulsera_fibra_trenzada`: QI +1 / CONTROL +1
- `colgante_fragmento_jade`: QI +1 / CONTROL +3
- resto del equipo LI: sin cambios

Regla de integración:
- esta aprobación autoriza **testeo**;
- NO autoriza todavía freeze productivo;
- NO modificar el catálogo/runtime productivo hasta que el microgate de equipo pase;
- si el microgate pasa, se podrá congelar el equipo LI y recién después ejecutar el gate final de Concordancias `NO_TRAP`.
