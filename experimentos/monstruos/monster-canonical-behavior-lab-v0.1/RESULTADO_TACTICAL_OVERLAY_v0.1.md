# Tactical Overlay v0.1 — Monster Canonical Behavior Lab

## Principio

El overlay no modifica `MOBS`, no toca el kernel y no altera la cadencia.

Sólo añade pesos experimentales a la traducción de habilidades canónicas.

## Pesos reutilizados

Todos provienen de patrones ya presentes en los fixtures auditados del Monster Combat AI:

```text
ataque básico OFENSIVA:
  PLAYER_LOW_HP +5

técnica OFENSIVA:
  PLAYER_LOW_HP +6

técnica CONTROL:
  DEFENSA_ABSORCION -8 por memoria efectiva

MANADA:
  MANADA_WITH_ALLY +5 sobre técnica

OPORTUNISTA:
  OPORTUNISTA_LOW_HP +15 sobre técnica
```

No se añaden todavía pesos para COLONIA o TERRITORIAL porque no hay un patrón auditado equivalente que reutilizar sin inventarlo.

## Casos que debe producir

### Sapo Ceniza — INSTINTIVO

Puede tener un peso de memoria en su técnica, pero su perfil usa `usesMemory=false`.

Resultado esperado: la memoria no afecta nada.

### Serpiente — REACTIVO_1

Sólo ve el último evento. Una defensa absorbente efectiva penaliza la técnica una vez, pero no necesariamente cambia la decisión.

### Guardián de Coral — TACTICO_3

Tres recuerdos de control ineficaz pueden acumular penalización suficiente para que elija ataque básico en vez de repetir su técnica de drenaje.

### Lobo — CAZADOR_2 / MANADA

La repetición puede hacer que deje de usar la técnica; la presencia de manada puede volver a inclinar la decisión hacia ella.

### Mono — CAZADOR_2 / OPORTUNISTA

Tras repetir mucho su técnica de drenaje, puede preferir básico; si el jugador queda bajo de vida, el flag oportunista puede devolver prioridad a la técnica.

## Invariante de producción

En `CADENCE_COMPAT` estos pesos **no pueden cambiar qué habilidad se ejecuta** porque el effectiveKit sólo contiene la habilidad permitida por la cadencia oficial.

La adaptividad sólo se observa en `DECISION_EXPERIMENTAL`.

## Estado

`TACTICAL_OVERLAY_V01: PENDING_CONFIRMATION`
