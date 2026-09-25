# Fuente Maestra ver55 — T240 · extracto Núcleo relevante para M17

**Carácter:** extracto técnico/topológico.  
**Uso:** verificar infraestructura y frontera M17→M18.

---

Núcleo — 13 habitaciones:

1. `nucleo_pozo_voto` — Pozo del Voto
2. `nucleo_camara_voto` — Cámara del Voto
3. `nucleo_galeria_primer_pacto` — Galería del Primer Pacto
4. `nucleo_primer_pacto` — Cámara del Primer Pacto
5. `nucleo_archivo_promesa` — Archivo de la Promesa
6. `nucleo_descenso_pulso` — Descenso del Pulso
7. `nucleo_galeria_pulso` — Galería del Pulso
8. `nucleo_camara_regulacion` — Cámara de Regulación
9. `nucleo_sala_relevo` — Sala de Relevo del Ancla
10. `nucleo_exterior_ancla` — Exterior del Ancla
11. `nucleo_camara_memoria` — Cámara de la Memoria
12. `nucleo_umbral_santuario` — Umbral del Santuario
13. `nucleo_santuario_vinculo` — Santuario del Vínculo

Ruta profunda congelada:

```text
nucleo_archivo_promesa
  abajo → nucleo_descenso_pulso

nucleo_descenso_pulso
  arriba → nucleo_archivo_promesa
  abajo  → nucleo_galeria_pulso

nucleo_galeria_pulso
  arriba → nucleo_descenso_pulso
  norte  → nucleo_camara_regulacion

nucleo_camara_regulacion
  sur   → nucleo_galeria_pulso
  norte → nucleo_sala_relevo

nucleo_sala_relevo
  sur   → nucleo_camara_regulacion
  norte → nucleo_exterior_ancla

nucleo_exterior_ancla
  sur   → nucleo_sala_relevo
  oeste → nucleo_camara_memoria
  norte → nucleo_umbral_santuario

nucleo_camara_memoria
  este → nucleo_exterior_ancla

nucleo_umbral_santuario
  sur   → nucleo_exterior_ancla
  norte → nucleo_santuario_vinculo

nucleo_santuario_vinculo
  sur → nucleo_umbral_santuario
```

M17 abre la parte profunda.

`nucleo_galeria_pulso` sustenta R7.

`nucleo_camara_regulacion` explica la relación entre organismo vivo e infraestructura.

`nucleo_sala_relevo` es el alojamiento final, seguro, no purificador.

`nucleo_exterior_ancla` sustenta R10.

`nucleo_camara_memoria` es opcional y no decide LIBERAR/CUSTODIAR.

`nucleo_umbral_santuario` permite retroceder.

`nucleo_santuario_vinculo` pertenece a M18.
