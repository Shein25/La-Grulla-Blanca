# Semantic Memory Recorder v0.1

Cadena objetivo:

```text
Combat Engine resolves
→ normalized resolved outcome
→ Semantic Memory Recorder
→ [{category,result,round}]
→ Monster Combat AI
```

## Eventos soportados

- `PLAYER_ABSORPTION_RESOLVED` → `DEFENSA_ABSORCION`
- `PLAYER_RECOVERY_RESOLVED` → `RECUPERACION`

`effective=true/false` se traduce a `EFECTIVA/FALLIDA`.

## Regla crítica

El recorder **no infiere** resultado desde HP, logs, daño futuro ni estado del próximo turno.

Sólo recibe resultados ya resueltos. Campos extra se rechazan para impedir dependencias ocultas.

## Orden temporal

La memoria debe permanecer en orden cronológico ascendente y un outcome no puede insertarse antes del último evento ya registrado.

## Fuera de alcance

- persistencia entre combates;
- decidir cuánto recuerda cada especie (lo hace `memoryDepth`);
- categorías nuevas;
- interpretación de evasión, guardia u otras técnicas no cubiertas;
- mutar combate.

## Estado

`SEMANTIC_MEMORY_RECORDER_V01: PENDING_CONFIRMATION`
