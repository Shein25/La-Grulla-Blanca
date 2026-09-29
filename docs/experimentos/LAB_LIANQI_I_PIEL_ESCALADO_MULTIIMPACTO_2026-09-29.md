# LAB — Escalado de Piel de Cobre bajo múltiples impactos

Fecha: 2026-09-29  
Rama: experiment/combat-stat-contract-v0.1  
Estado: **LAB / NO CAMBIO DE DISEÑO APROBADO**

## Problema

El stress multi-enemigo mostró que la Piel actual escala demasiado rápido:

- comienza con +2 DEF y 1 Arraigo;
- cada Arraigo añade +1 DEF;
- puede llegar a 3 Arraigos;
- al alcanzar el máximo extiende duración una vez.

Con DEF base1:

~~~text
activación → DEF4
2 Arraigos → DEF5
3 Arraigos → DEF6
~~~

En LianQi I, DEF6 es una barrera muy fuerte contra múltiples ataques de daño moderado.

## Control ofensivo de Tierra

Win aproximado sin Piel:

| Enemigos | Win |
|---:|---:|
| 1 | ~92% |
| 2 | ~61% |
| 3 | ~18% |

## Variantes de Piel

### CURRENT

Contribución de DEF de Arraigo: 1 / 2 / 3.  
Extensión al máximo: sí.

| Enemigos | Win |
|---:|---:|
| 1 | ~96% |
| 2 | ~88% |
| 3 | ~68% |

El salto multiobjetivo es excesivamente grande para promoverlo sin revisión.

### DEF_CAP2

~~~text
Arraigo 1 → +1 DEF
Arraigo 2 → +2 DEF acumulada
Arraigo 3 → sigue +2 DEF acumulada
~~~

La tercera carga conserva Tenacidad y activa la extensión, pero no añade otra unidad de DEF.

DEF total:

~~~text
1 Arraigo → DEF4
2 Arraigos → DEF5
3 Arraigos → DEF5
~~~

Resultados aproximados:

| Enemigos | Win |
|---:|---:|
| 1 | ~96% |
| 2 | ~85% |
| 3 | ~58% |

### DEF_DIMINISHING

Curva de DEF de Arraigo: 1 / 1 / 2.

| Enemigos | Win |
|---:|---:|
| 1 | ~96% |
| 2 | ~84% |
| 3 | ~56% |

Reduce algo más el escalado, pero hace menos intuitivo el segundo Arraigo.

### NO_EXTENSION

Mantiene DEF actual, pero elimina el +1 turno al alcanzar 3 Arraigos.

| Enemigos | Win |
|---:|---:|
| 1 | ~94% |
| 2 | ~80% |
| 3 | ~50% |

Es eficaz para contener multiimpacto, pero elimina una parte distintiva ya diseñada.

### DIMINISHING + NO_EXTENSION

Es la variante más restrictiva:

| Enemigos | Win |
|---:|---:|
| 1 | ~93% |
| 2 | ~76% |
| 3 | ~39% |

No se recomienda como primer ajuste: cambia dos ejes a la vez.

## Hallazgo

Limitar ganancia de Arraigo a una vez por ronda casi no resuelve el problema.

La causa dominante es:

1. DEF plana alta en esta escala de daño;
2. alcanzar DEF6;
3. extender la ventana de esa DEF al máximo de Arraigo.

Por eso conviene tocar primero la **curva de DEF**, no el trigger reactivo.

## Candidato LAB principal

**DEF_CAP2**.

Razones:

- mantiene el mismo inicio de Piel;
- conserva el trigger por acción;
- conserva 3 Arraigos;
- conserva Tenacidad por Arraigo;
- conserva la extensión;
- reduce DEF máxima total de 6 a 5;
- la tercera carga sigue importando por Tenacidad + extensión;
- corrige el escalado sin rediseñar toda la técnica.

No se promueve todavía.

## Próxima validación para Piel

Comparar CURRENT vs DEF_CAP2 contra:

- enemigo común;
- enemigo de daño alto;
- enemigo de pocos impactos fuertes;
- 2 enemigos;
- 3 enemigos;
- posteriormente enemigos con Control para valorar la Tenacidad de la tercera carga.

