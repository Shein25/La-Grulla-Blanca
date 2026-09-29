# ETAPA 10A — Cuerpo de Roca · screen estructural 1v1

Fecha: 2026-09-29  
Rama: `experiment/combat-stat-contract-v0.1`  
Estado: **CERRADA COMO SCREEN / CANDIDATO LAB SELECCIONADO**

## Pregunta única

¿Cómo debe culminar **Cuerpo de Roca (Tramo III / LianQi IV)** la ruta de
fortificación sin convertir la progresión en DEF7+ permanente?

Además debe:

- funcionar aunque no se haya elegido Corteza;
- funcionar aunque no se haya elegido Estratos;
- conservar retornos decrecientes si se combina con ambos;
- no impedir que Piel llegue a Arraigo máximo.

## Variante descartada: activación desde 2 Arraigos

Se probó conceptualmente una ventana defensiva activa desde `Arraigo >= 2`.

Resultado:

- bloquea daño demasiado pronto;
- reduce ON_HP_DAMAGE;
- reduce generación posterior de Arraigo;
- reduce con fuerza la extensión;
- empieza a interferir con la identidad de “asentarse bajo presión”.

Por tanto, Cuerpo de Roca no debe adelantarse al asentamiento de Piel.

## Arquitectura seleccionada

**ROCA_GUARD_MAX_3**

```text
Piel activa
+
Arraigo == 3
↓
primer impacto directo conectado
de cada turno del usuario
↓
+3 DEF sólo para ese impacto
↓
la Guardia se consume para ese turno
```

Reglas:

- se rearma al comenzar el siguiente turno del usuario si Piel sigue activa y
  Arraigo sigue en 3;
- una evasión no consume la Guardia;
- no aumenta DEF permanente;
- no aumenta Tenacidad;
- no aumenta duración;
- no aumenta máximo de Arraigo;
- no modifica retroactivamente el impacto que llevó a Arraigo 3;
- funciona con o sin Corteza/Estratos.

## Magnitudes cribadas

Se comparó la ventana con:

- +2 DEF;
- +3 DEF;
- +4 DEF.

### Perfil común 2d4+1

Con Piel base, +2/+3/+4 aumentan progresivamente la supervivencia.

Con la ruta previa completa (Corteza + Estratos), el retorno marginal cae mucho:

| Ventana | Win aproximado |
|---|---:|
| sin Cuerpo | 96.41% |
| +2 | 96.52% |
| +3 | 96.52% |
| +4 | 96.52% |

En un enemigo común, +4 prácticamente no aporta nada adicional sobre +3.

### Perfil pesado 1d6+3

Ruta previa completa:

| Ventana | Win aproximado |
|---|---:|
| sin Cuerpo | 94.44% |
| +2 | 94.74% |
| +3 | 94.80% |
| +4 | 94.81% |

De nuevo, +4 entra casi completamente en retorno decreciente.

## Candidato de magnitud

Se selecciona **+3 DEF**.

Motivo:

- +2 funciona, pero deja margen útil frente a golpes pesados;
- +3 mejora esa protección;
- +4 aporta muy poco cuando ya existen Corteza y Estratos;
- no hace falta pagar complejidad/potencia extra por una ganancia marginal.

## Replicación de ROCA_GUARD_MAX_3

Cuatro semillas independientes de 40.000 combates.

### Piel base · perfil común

Delta de win:

- +1.105 pp;
- +1.008 pp;
- +1.013 pp;
- +1.000 pp.

Delta de HP restante:

- +4.49 pp;
- +4.46 pp;
- +4.42 pp;
- +4.47 pp.

Usos medios:

- ~1.22 Guardias por combate.

### Ruta previa completa · perfil común

Delta de win:

- +0.110 pp;
- +0.088 pp;
- +0.075 pp;
- +0.065 pp.

Delta de HP:

- +0.43 a +0.49 pp.

Usos:

- ~0.45 por combate.

Esto muestra retorno decreciente muy fuerte cuando las capas anteriores ya
mitigan suficiente daño.

### Piel base · perfil pesado

Delta de win:

- +1.773 pp;
- +1.860 pp;
- +2.125 pp;
- +1.785 pp.

Delta de HP:

- +6.32 a +6.60 pp.

Usos:

- ~1.47 por combate.

### Ruta previa completa · perfil pesado

Delta de win:

- +0.335 pp;
- +0.325 pp;
- +0.318 pp;
- +0.338 pp.

Delta de HP:

- +1.35 a +1.42 pp.

Usos:

- ~0.80 por combate.

## Lectura

El candidato tiene el patrón buscado:

```text
enemigo común + ruta ya fortificada
→ beneficio pequeño

golpe más pesado
→ beneficio más visible
```

Por tanto Cuerpo de Roca no necesita empujar la DEF permanente.

Su valor aparece precisamente cuando Piel:

1. consiguió llegar a Arraigo máximo;
2. sigue activa;
3. enfrenta impactos suficientemente peligrosos como para que una ventana
   puntual de +3 DEF importe.

## Relación con LianQi IV

Todavía no existe un perfil enemigo numérico autoritativo para LianQi IV.

Por tanto esta etapa:

- selecciona arquitectura;
- selecciona magnitud LAB;
- NO demuestra todavía balance final de LianQi IV.

El perfil pesado `1d6+3` es sólo sensibilidad LAB ya existente.

## Resultado de Etapa 10A

**ROCA_GUARD_MAX_3 pasa a candidato principal LAB para Cuerpo de Roca.**

Regla candidata:

```text
a Arraigo 3:
primer impacto directo conectado de cada turno
→ +3 DEF sólo para ese impacto
```

Todavía:

- NO PROVISIONAL;
- NO CANON;
- NO runtime.

## Próxima etapa

**ETAPA 10B — ROCA_GUARD_MAX_3 contra 2 enemigos.**

Pregunta única:

¿limitar Cuerpo de Roca al primer impacto conectado de cada turno evita que
escale con la cantidad de atacantes?

No abrir otras defensivas.
