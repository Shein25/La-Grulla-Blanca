# Encargo para agente externo — Test Motor NPC Vivo v0.1

Audita el laboratorio `experimentos/motor-npc-vivo-v0.1/` como sistema experimental independiente.

NO modifiques el juego de producción.
NO integres nada en `grulla-blanca_ver73.html`.
NO conviertas los fixtures ficticios en NPC canónicos.
NO ajustes pesos para forzar un resultado sin documentarlo.

## 1. Ejecuta la regresión

```bash
node tests.mjs
```

Reporta PASS/FAIL exacto y cualquier stack trace.

## 2. Ejecuta stress reproducible

```bash
node stress.mjs 10000 1337
```

Después repite con al menos cuatro seeds distintos:

```bash
node stress.mjs 10000 1
node stress.mjs 10000 42
node stress.mjs 10000 999
node stress.mjs 10000 20260923
```

Reporta distribución de acciones y cualquier invariante roto.

## 3. Prueba adversarial

Busca activamente:

- NaN / Infinity;
- acciones bloqueadas que ganen;
- hablar/ayudar con jugador ausente;
- revelar un tema DESCONOCIDO;
- presentar SOSPECHA como COMPARTE;
- una sola acción dominando casi todos los contextos;
- cambios pequeños que produzcan oscilaciones enormes;
- rango anulando completamente personalidad;
- afinidad/confianza anulando siempre el deber;
- prudencia/temor generando parálisis constante;
- inercia `lastAction` atrapando al NPC indefinidamente;
- empates inestables/no deterministas;
- mutación del objeto NPC de entrada;
- combinaciones extremas 0/100.

## 4. Prueba de sensibilidad

Para cada fixture, mantené fijo el resto y barré de 0 a 100:

- confianza;
- afinidad;
- respeto;
- importancia del puesto;
- urgencia;
- peligro;
- rango del jugador 0..6.

Identificá umbrales donde cambia la acción y si son razonables.

## 5. Prueba de personalidad

Usá la misma situación para los tres fixtures.

Queremos verificar patrones distinguibles, no forzar una única acción exacta.

Explicá qué variables hacen que cada personalidad se comporte diferente.

## 6. Conocimiento y diálogo

Probá R1/R2/R3 en:

- DESCONOCIDO
- SOSPECHA
- SABE
- CONFIRMADO

con combinaciones extremas de vínculo, rango, sensibilidad y restricción institucional.

Reglas duras:

- DESCONOCIDO nunca revela.
- SOSPECHA nunca se convierte en afirmación confirmada.

## 7. Revisión de diseño

Evaluá si el motor es:

- determinista;
- explicable;
- testeable;
- extensible hacia GOAP;
- suficientemente desacoplado del juego;
- apto para incorporar 32 NPC sin lógica especial por NPC.

## 8. Entregable

No edites archivos salvo que se te pida después.

Devuelve:

`Informe_Test_Motor_NPC_Vivo_v0.1.md`

Debe incluir:

1. entorno usado;
2. comandos ejecutados;
3. regresión;
4. stress por seed;
5. bugs con reproducción mínima;
6. balance de pesos;
7. casos límite;
8. riesgos arquitectónicos;
9. cambios recomendados para v0.2;
10. un único veredicto:

`V01_APTO_PARA_ITERAR`

`V01_REQUIERE_CORRECCIONES`

`V01_FALLO_CONCEPTUAL`

No propongas integración al juego todavía.
