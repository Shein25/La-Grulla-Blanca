# ETAPA 19A — Piloto de escala defensiva frente a monstruos nativos

Fecha: 2026-09-29
Estado: **PILOTO LAB / NO BALANCE FINAL**

## Propósito

Comprobar rápidamente si la progresión de Vestidura:

```text
LI +1 DEF
LII +2
LIII +3
LIV +4
```

está en una escala absurda frente a los monstruos nativos, antes de implementar el motor completo de habilidades.

Este piloto NO incluye:
- técnicas del jugador;
- raíz;
- resto del equipo;
- Qi;
- Control;
- C_STAGGERED;
- decisiones completas de Monster AI;
- timing real de DOT.

Usa:
- HP por etapa 30/36/42/48;
- Precisión100;
- EVA5;
- DEF base1;
- Golpe básico 1d4+4/+5/+6/+7;
- monstruos traducidos LAB;
- daño/técnicas directas de ver74;
- 15,000 duelos por celda.

Los DOT fueron aplicados de manera conservadora/agresiva como presión total al producirse la técnica, por lo que NO son evidencia de timing final.

## Resultados

### LianQi I — armadura +1 DEF

| Monstruo | Rol | naked win | armadura win | Δ pp |
|---|---|---:|---:|---:|
| Rata de Qi | NORMAL | 100.00% | 100.00% | +0.00 |
| Avispa de Jade | NORMAL | 99.99% | 100.00% | +0.01 |
| Serpiente de Qi | NORMAL | 98.45% | 99.53% | +1.07 |
| Macaco ladrón | SKIRMISHER | 98.74% | 99.75% | +1.01 |
| Lobo espiritual | APEX_BRIDGE | 90.33% | 96.89% | +6.57 |

Lectura:
+1 DEF es perceptible contra el apex, pero no cambia la naturaleza tutorial de los normales.

### LianQi II — armadura +2 DEF

| Monstruo | Rol | naked | armadura | Δ pp |
|---|---|---:|---:|---:|
| Sapo Ceniza | NORMAL | 88.20% | 97.22% | +9.02 |
| Escarabajo Hierro | TANK | 53.85% | 89.37% | +35.52 |
| Eco del Caído | ELITE | 38.35% | 75.53% | +37.19 |
| Sapo Caldera | BOSS | 1.73% | 4.39% | +2.65 |
| Rey Escarabajo | BOSS | 0.00% | 0.06% | +0.06 |

Lectura:
+2 DEF importa muchísimo en encuentros de daño medio/repetido, pero no convierte los bosses en encuentros triviales.

### LianQi III — armadura +3 DEF

| Monstruo | Rol | naked | armadura | Δ pp |
|---|---|---:|---:|---:|
| Pez Lunar | NORMAL | 89.43% | 99.92% | +10.49 |
| Anguila Estelar | SKIRMISHER | 58.48% | 93.36% | +34.88 |
| Sombra Ahogada | ELITE | 10.93% | 40.54% | +29.61 |
| Guardián Coral | BOSS | 0.02% | 0.71% | +0.69 |

Lectura:
la armadura cambia mucho la supervivencia normal/skirmisher/elite, mientras el boss todavía exige técnicas, equipo adicional y preparación.

### LianQi IV — armadura +4 DEF

| Monstruo | Rol | naked | armadura | Δ pp |
|---|---|---:|---:|---:|
| Devorador Niebla | NORMAL | 43.19% | 96.49% | +53.29 |
| Halcón Tormenta | SKIRMISHER | 47.75% | 92.10% | +44.35 |
| Mantis Nube | BOSS | 0.38% | 9.15% | +8.77 |
| Centinela Plumas | BOSS | 0.21% | 8.59% | +8.38 |

Lectura:
+4 DEF es un aumento grande —como debe ser una armadura de final de Arco—, pero incluso bajo este piloto simplificado los bosses siguen aplastando a un personaje que sólo trae crecimiento intrínseco + armadura.

## Conclusión del piloto

No hay evidencia para volver a limitar Vestidura a +1 DEF.

Al contrario:
- la progresión +1/+2/+3/+4 produce una diferencia real;
- frente a bosses no basta por sí sola;
- el motor completo deberá determinar si +4 es correcto una vez añadidos técnicas, roots, Qi y resto del equipo.

La enorme diferencia contra NORMAL/SKIRMISHER en LIV es un WATCH:
podría ser correcta si esos encuentros representan fauna ya dominable por un cultivador bien armado, o podría requerir más daño/precisión nativa al traducir definitivamente los monstruos.

No modificar todavía.
