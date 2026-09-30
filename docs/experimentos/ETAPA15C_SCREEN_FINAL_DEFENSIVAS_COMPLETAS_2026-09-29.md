# ETAPA 15C — Screen conjunto final de las cinco defensivas completas

Fecha: 2026-09-29  
Rama: experiment/combat-stat-contract-v0.1  
Estado: **CERRADA / PASS ESTRUCTURAL GLOBAL / SIN CAMBIOS NUMÉRICOS**

## Objetivo

Comparar las cinco defensivas completas después de cerrar:

- base;
- Tramos I–III;
- 27/27 rutas mixables por técnica.

Esta etapa **no vuelve a simular** las cinco técnicas en un motor unificado.

Agrega y audita los benchmarks ya cerrados por:

- ETAPA 11 — Cuerpo-Horno;
- ETAPA 12 — Espejo de Luna;
- ETAPA 13 — Paso de Nube Ligera;
- ETAPA 14 — Armadura de Plata;
- ETAPA 15B — Piel de Cobre.

Runner agregador:

experimentos/balance_nuevo/etapa15c_screen_final_defensivas_completas.py

---

# 1. Guardia metodológica

No es válido leer estos porcentajes como:

> “qué elemento es mejor”.

Cada raíz usa:

- rasgo CANON diferente;
- ofensiva PROVISIONAL diferente;
- economía de Qi diferente;
- mecánica defensiva diferente.

Además, los nodos de Tramo I–III representan progresión hasta LianQi IV,
mientras los perfiles numéricos disponibles siguen siendo el marco LAB de
LianQi I.

Por tanto esta etapa sólo puede responder:

1. ¿alguna técnica contiene crecimiento ilimitado?
2. ¿alguna rama quedó mecánicamente muerta?
3. ¿alguna familia perdió su identidad?
4. ¿alguna interacción necesita WATCH futuro?
5. ¿hay evidencia suficiente para reabrir números ahora?

---

# 2. Rango 27/27 — COMMON

| Técnica | Win mínimo | Win máximo |
|---|---:|---:|
| Fuego — Cuerpo-Horno | 95.86% | 97.23% |
| Metal — Armadura | 93.19% | 98.55% |
| Agua — Espejo | 89.74% | 92.84% |
| Tierra — Piel | 95.71% | 99.11% |
| Viento — Paso | 90.31% | 93.45% |

Todas las técnicas avanzadas son muy fuertes contra el enemigo COMMON.

Esto era esperable:

> se están usando nodos de progresión superior contra un perfil LianQi I.

No se utiliza este resultado para igualar cifras.

---

# 3. Rango 27/27 — dos enemigos

Stress unitarget con HP total28 dividido entre dos enemigos.

| Técnica | Win mínimo | Win máximo |
|---|---:|---:|
| Fuego | 68.76% | 80.05% |
| Metal | 56.94% | 83.20% |
| Agua | 40.33% | 59.28% |
| Tierra | 84.84% | 96.16% |
| Viento | 65.35% | 78.30% |

Aquí ya se separan claramente las identidades.

## Fuego

La reserva es finita, pero Conversión puede devolver tempo ofensivo.

## Metal

La dispersión entre rutas es grande:

- Resistencia favorece pocos impactos;
- Cantidad cubre presión múltiple;
- mezclas R+Q son especialmente relevantes.

## Agua

Sufre cuando varios enemigos pueden romper el pool antes del siguiente
TURN_START.

Reserva reduce esa debilidad, pero no la elimina.

## Tierra

Cada acción enemiga puede:

- alimentar Arraigo;
- activar más tiempo útil de Piel;
- recibir DEF plana.

Por eso mantiene el mayor escalado multiimpacto.

## Viento

Cada acción enemiga es también una nueva oportunidad de Evasión.

---

# 4. Rango 27/27 — tres enemigos

| Técnica | Win mínimo | Win máximo |
|---|---:|---:|
| Fuego | 30.03% | 50.18% |
| Metal | 11.38% | 34.03% |
| Agua | 4.60% | 12.44% |
| Tierra | 59.06% | 87.01% |
| Viento | 31.24% | 50.33% |

Éste es el perfil con mayor separación.

No se interpreta como balance final de encuentros.

---

# 5. ¿Tierra está rota?

No se puede concluir eso desde este stress.

Sí puede concluirse:

> Piel sigue siendo el principal **WATCH multiimpacto**.

Ya se corrigieron dos amplificadores distintos:

## DEF_CAP2

El tercer Arraigo dejó de añadir otro incremento permanente de DEF.

## AGUANTE_DUR_CAP1

Aguante ya no puede acumular múltiples turnos base adicionales.

Además:

- Estratos está limitado a máximo1 almacenado;
- Guardia de Roca está limitada a una por turno;
- las curaciones son una vez por activación;
- la extensión de Arraigo máximo ocurre una vez.

No existe crecimiento infinito.

Por tanto no se hace otro nerf sin perfiles de encuentro reales.

---

# 6. ¿Agua está demasiado débil contra grupos?

Espejo queda claramente abajo en el stress de tres enemigos.

Pero este escenario prueba exactamente su peor condición:

~~~text
varios enemigos
→ muchos impactos antes del próximo TURN_START
→ pool llega a0
→ Reflujo no opera
~~~

El set actual no incluye todavía un perfil diseñado para su fortaleza:

~~~text
presión sostenida
+
impactos separados por TURN_START
~~~

Tampoco incluye:

- futuros valores de Qi;
- técnicas ofensivas/AOE de etapas superiores;
- encuentros donde Arrastre pueda negar la acción clave correcta.

Por tanto:

~~~text
Agua
→ WATCH burst múltiple
→ NO buff automático
~~~

---

# 7. ¿Metal está demasiado disperso?

No.

Su rango amplio es consecuencia directa de rutas con objetivos diferentes.

## Resistencia

Pocas cargas muy fuertes.

## Cantidad

Muchas cargas moderadas.

## Adaptación

Invierte potencia en Control, que los perfiles de daño puro no activan.

Además, rutas mixtas R+Q superan en ciertos contextos a rutas puras.

Eso demuestra que el sistema 3×3 es funcional.

---

# 8. ¿Fuego tiene un problema por no dominar supervivencia?

No.

Fuego es la familia que más claramente convierte defensa en tempo ofensivo:

~~~text
Absorción
→ Calor
→ daño secundario posterior
→ enemigo muere antes
~~~

La rama Conversión alcanza el extremo alto de Fuego en stress multi-enemigo sin
necesitar un pool infinito.

Pendiente separado:

- cerrar semántica exacta de consumo de Calor si la técnica portadora falla.

No bloquea el balance estructural.

---

# 9. ¿Viento escala demasiado con muchos ataques?

Paso mejora naturalmente cuando hay más intentos enemigos.

Sin embargo existen límites explícitos:

- clamp global de impacto;
- no hay segunda tirada de esquiva;
- no existe Velocidad;
- no existe movimiento defensivo implícito;
- CORRIENTE_CLARA sólo puede generarse una vez por activación.

Además, frente a mayor Precisión la ruta Eficiencia puede competir con Evasión
pura.

No se detecta escalado ilimitado.

---

# 10. Cobertura de nichos

## Fuego

~~~text
pool finito
conversión defensa→ofensa
economía/duración
~~~

## Metal

~~~text
cargas por impacto
fuerza por carga
cantidad
anti-Control
~~~

## Agua

~~~text
pool regenerativo
reconstrucción
eficiencia
~~~

## Tierra

~~~text
crecimiento reactivo
Tenacidad
ventanas defensivas
curación limitada
~~~

## Viento

~~~text
Evasión
respuesta al esquivar
continuidad
~~~

No hay dos técnicas que estén resolviendo exactamente el mismo problema de la
misma forma.

---

# 11. Guardias estructurales globales

## Fuego

- pool finito;
- cap de Calor;
- Calor no vuelve a recibir escalado ofensivo;
- no crit;
- no Penetración.

## Metal

- Placas secuenciales;
- DEF de varias Placas nunca se suma;
- número finito;
- duración4.

## Agua

- pool finito;
- Reflujo exige pool vivo;
- reconstrucción una vez;
- recuperación Qi explícita, no regen universal.

## Tierra

- DEF_CAP2;
- Estrato máximo1;
- Guardia de Roca máximo1 por turno;
- AGUANTE_DUR_CAP1;
- curaciones una vez por activación.

## Viento

- clamp de impacto;
- CORRIENTE una vez por activación;
- no segunda esquiva;
- no movimiento/Velocidad.

---

# 12. Resultado global

Las cinco defensivas pasan el criterio estructural.

~~~text
CUERPO-HORNO       PASS PROVISIONAL
ARMADURA DE PLATA  PASS PROVISIONAL
ESPEJO DE LUNA     PASS PROVISIONAL
PIEL DE COBRE      PASS PROVISIONAL + WATCH
PASO DE NUBE       PASS PROVISIONAL
~~~

No se modifica ningún número en ETAPA 15C.

No se modifica runtime/HTML.

---

# 13. Qué NO está demostrado todavía

Este cierre NO significa:

~~~text
balance final LianQi II
balance final LianQi III
balance final LianQi IV
~~~

Faltan perfiles enemigos numéricos autoritativos de esas etapas.

Por tanto los valores avanzados quedan:

~~~text
PROVISIONAL estructuralmente validados
pendientes de validación por etapa
~~~

---

# 14. WATCH globales

## Tierra

- multiimpacto;
- mezclas Fortificación+Aguante.

## Agua

- burst simultáneo;
- falta perfil específico de presión espaciada.

## Metal

- Adaptación con Control real;
- multihit real.

## Fuego

- consumo exacto de Calor en hit/miss;
- economía Qi futura.

## Viento

- Precisión enemiga II–IV;
- economía/duración futura.

---

# 15. Estado de las cinco defensivas

Por primera vez el estado correcto es:

~~~text
5 / 5 defensivas completas
5 / 5 bases PROVISIONAL
15 / 15 familias de progresión estructuralmente cerradas
135 / 135 rutas conceptuales cubiertas
(27 por defensiva × 5)

runtime: SIN CAMBIOS
HTML: SIN CAMBIOS
~~~

Nota:

Las 135 rutas no fueron ejecutadas todas dentro de un único runner común.
Cada grupo de 27 fue validado por el runner autoritativo de su propia técnica y
ETAPA15C agrega esos resultados.

---

# 16. Próximo bloque correcto

Con las defensivas estabilizadas, el siguiente bloque vuelve a la economía
global:

**ETAPA 16 — validación final de Qi31.**

Objetivo:

- comprobar Qi31 con las cinco defensivas ya cerradas;
- verificar umbrales 29–36;
- decidir si Qi31 pasa de LAB a PROVISIONAL;
- no reabrir daño/DEF salvo contradicción nueva.
