# Mei Lian — baseline de frente condicional / LAB v0.1

## Objetivo

Probar si el stack avanzado puede distinguir el requisito canónico M16:

`SAUCES o MEDICINA según estado y responsables disponibles`.

## Resultado conceptual

Con los facts genéricos actuales, dos contextos etiquetados externamente como SAUCES y MEDICINA son indistinguibles para Utility/GOAP:

```text
trabajar
→ FULFILL_DUTY
→ cumplir_deber
```

Utility aislado ignora un campo adicional `front` porque no forma parte de su snapshot requerido. El Autonomous Loop, más estricto, rechaza ese campo como no contractual.

Por tanto no existe actualmente una semántica ejecutable de frente.

## Gap

`M16_FRONT_ASSIGNMENT_SAUCES_OR_MEDICINA`

Se requiere una capa de dominio que represente al menos:

- identidad del frente;
- necesidad/estado del frente;
- responsables disponibles;
- asignación resultante;
- navegación/acción física correspondiente.

No se inventa una prioridad Sauces-vs-Medicina en este baseline.

## Estado

`MEI_LIAN_CONDITIONAL_FRONT_BASELINE: PENDING_CONFIRMATION`
