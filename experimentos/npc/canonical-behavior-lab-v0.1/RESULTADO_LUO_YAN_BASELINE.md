# Luo Yan — baseline de conocimiento amplio y epílogo / LAB v0.1

## Objetivo

Cubrir dos requisitos que el stack genérico todavía no representa:

1. conocimiento canónico fuera de R1-R3;
2. reacción específica al resultado narrativo LIBERAR/CUSTODIAR.

## Canon relevante

- protocolo/historia oficial; lealtad institucional;
- R1 = SOSPECHA;
- R5 = SABE;
- epílogo = LEALTAD_RESPONSABLE;
- único compañero con reacción concreta documentada a LIBERAR/CUSTODIAR.

## Gap 1 — esquema de conocimiento

Utility v0.1.1 exige exactamente:

```text
R1
R2
R3
```

Al intentar representar el dato canónico:

```text
R5 = SABE
```

el perfil deja de validar.

Por tanto:

`KNOWLEDGE_SCHEMA_R1_TO_R10`

es capacidad pendiente para NPC con conocimiento canónico más amplio.

El dato R1 sí se procesa correctamente como SOSPECHA; el test no convierte sospecha en certeza.

## Gap 2 — LIBERAR/CUSTODIAR

El resultado narrativo del epílogo no forma parte del contexto de Utility ni del vocabulario GOAP.

Dos contextos idénticos salvo una etiqueta externa:

```text
LIBERAR
CUSTODIAR
```

producen actualmente la misma decisión porque el motor no consume esa variable.

Por tanto:

`LIBERAR_CUSTODIAR_DOMAIN_OUTCOME`

debe existir antes de esperar que Luo Yan ejecute su reacción canónica.

## Estado

`LUO_YAN_KNOWLEDGE_EPILOGUE_BASELINE: PENDING_CONFIRMATION`
