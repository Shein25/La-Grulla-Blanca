# Fuente Maestra ver55 — T257 · extracto técnico M17

**Carácter:** extracto técnico de transición/idempotencia aplicable a M17.

---

M17 puede comenzar dentro de `LIV_CRISIS`; la fuente prefiere **no añadir otro estado macro**.

Fases:

```text
CONSEJO
→ AUTORIZACION
→ DESCENSO
→ DEPENDENCIA_VIVA
→ GRULLA
```

Precondición:

```text
M16 hecha
```

Inicio:

Convocatoria al Consejo.

Consejo:

```text
NUCLEO_PROFUNDO_AUTORIZADO
```

concede el permiso exactamente una vez.

Descenso:

En Galería/Cámara de Regulación:

```text
dependenciaViva → CONFIRMADO
R7 satisfecho
```

En Exterior del Ancla:

```text
grullaViva → CONFIRMADO
R10 satisfecho
```

Sala de Relevo:

Debe quedar visitable y conocida antes del cierre.

Cierre:

El jugador llega hasta la verdad necesaria y queda preparado para intervenir.

Efectos:

```text
M17 → HECHA
M18 disponible
conocimiento institucional actualizado según escena
```

No inicia M18 automáticamente al entrar al Santuario.
