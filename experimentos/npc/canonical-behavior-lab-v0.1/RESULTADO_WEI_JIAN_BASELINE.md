# Wei Jian — baseline marcial reactivo / LAB v0.1

## Objetivo

Probar una hipótesis de Behavior Tree para una autoridad marcial:

```text
amenaza alta
→ responder seguridad

sospecha
→ investigar

entrenamiento pendiente
→ supervisar entrenamiento
```

La política es experimental. No convierte estos intents en canon.

## Canon relevante

- Responsable marcial / Pabellón Marcial;
- movilidad RUTA;
- acceso a Interior mediante `SECTA_INTERIOR`;
- M16: Seguridad/respuesta;
- no es responsable formal de uno de los seis frentes T281.

## Qué se prueba

- entrenamiento ordinario;
- anomalía que interrumpe entrenamiento;
- crisis que preempta tanto entrenamiento como sospecha;
- recuperación al entrenamiento una vez terminada la respuesta.

## Límites

`RESPOND_SECURITY` es sólo un intent.

El Behavior Tree no:

- resuelve combate;
- mueve físicamente al NPC;
- atraviesa `SECTA_INTERIOR`;
- selecciona técnicas marciales.

El Utility genérico tampoco posee actualmente una acción marcial equivalente.

## Estado

`WEI_JIAN_MARTIAL_BT_BASELINE: 17_PASS_0_FAIL_CONFIRMED`


## Confirmación

```text
PASS: 17
FAIL: 0
```

Trazas clave:

```text
trainingDue
→ SUPERVISE_TRAINING

training RUNNING + suspicious
→ training PREEMPTADA
→ INVESTIGATE_MARTIAL_ANOMALY

training RUNNING + highThreat
→ training PREEMPTADA
→ RESPOND_SECURITY

security_response SUCCESS + trainingDue
→ SUPERVISE_TRAINING
```

No se detectó falsa preempción al finalizar la respuesta.
