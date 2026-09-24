# Motor NPC Vivo v0.1 — Laboratorio

Prototipo **aislado** para experimentar con comportamiento NPC antes de integrar cualquier idea en La Grulla Blanca.

## Regla de seguridad

Este directorio NO es código de producción.

No debe importarse desde `grulla-blanca_ver73.html`, no modifica el baseline y no contiene decisiones canónicas sobre los 32 NPC.

## Objetivo de v0.1

Probar cinco piezas:

1. personalidad numérica;
2. vínculo multidimensional con el jugador;
3. rango institucional del jugador;
4. conocimiento individual;
5. Utility AI determinista con explicación de la decisión.

No incluye todavía GOAP, pathfinding, memoria episódica, relaciones NPC↔NPC ni diálogo textual generativo.

## Archivos

- `engine.mjs`: motor de puntuación, elección de acción y acceso a conocimiento.
- `npc-fixtures.mjs`: tres NPC ficticios extremos para pruebas.
- `scenarios.mjs`: escenarios controlados.
- `tests.mjs`: regresión determinista.
- `stress.mjs`: stress test pseudoaleatorio reproducible.
- `simulator.html`: interfaz visual del laboratorio.
- `PROMPT_AGENTE_TEST.md`: encargo listo para otro agente.

## Ejecutar

Requiere Node.js moderno, sin dependencias externas.

```bash
node tests.mjs
node stress.mjs 10000
```

Para la interfaz, servir este directorio por HTTP y abrir `simulator.html`. Ejemplo:

```bash
python -m http.server 8080
```

## Invariantes de v0.1

- misma entrada => misma decisión;
- puntuaciones disponibles finitas entre 0 y 100;
- una acción bloqueada nunca puede ganar;
- sin jugador presente no se puede hablar/ayudar al jugador;
- `DESCONOCIDO` jamás puede convertirse en información revelada;
- `SOSPECHA` jamás se presenta como hecho confirmado;
- personalidad, vínculo y contexto deben poder cambiar la acción elegida;
- el motor no muta silenciosamente el NPC de entrada;
- el debug explica las contribuciones de la decisión.

## Roadmap experimental

- v0.1: personalidad + vínculos + rango + conocimiento + Utility AI + debug.
- v0.2: objetivos y planificación limitada (GOAP).
- v0.3: memoria episódica y efectos persistentes sobre vínculos.
- v0.4: interacción NPC↔NPC y transmisión controlada de información.
- v0.5: selector de diálogo contextual.
- v1.0: candidato a contrato de integración, sólo si las pruebas lo justifican.
