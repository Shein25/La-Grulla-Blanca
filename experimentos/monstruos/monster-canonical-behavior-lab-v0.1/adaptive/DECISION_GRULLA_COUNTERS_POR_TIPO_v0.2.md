# Decisión — Counters aprendidos por tipo de técnica de la Grulla v0.2

**Fecha:** 2026-09-26  
**Estado:** EXPERIMENTAL / NO CANÓNICO  
**Rama:** `experiment/monster-adaptive-survival-lab-v0.1`

## Objetivo

La Grulla no debe reaccionar igual a todas las técnicas del jugador.

Cuando comprende una técnica concreta tras repetición suficiente, la respuesta depende del **tipo real de esa técnica**.

La regla dura se mantiene:

> una estrategia que pretenda resolver todo el jefe usando exclusivamente la misma skill debe tener 0% de victoria.

La adaptación no usa future-read.

---

## 1. Técnicas relevantes al cierre de LianQi

En ver74, las herramientas Mortales relevantes para el examen del Arco 1 pertenecen a estas familias:

- `palma` — ofensiva;
- `filo` — ofensiva;
- `latigo` — ofensiva;
- `paso_nube` — esquiva;
- `piel_cobre` — guardia;
- `filamento` — control.

El contrato también soporta `fortificacion` para compatibilidad futura, pero no se fuerza esa categoría dentro del examen de LianQi IV.

---

## 2. Cuándo se considera aprendida una skill

En Fases II/III:

```text
misma skill
→ misma skill
→ misma skill
→ counter aprendido
```

La tercera ejecución todavía se resuelve normalmente.

Después de resolverla, la UI debe anunciar que la Grulla ha comprendido ese patrón.

La siguiente repetición ya recibe el counter.

Si el jugador llega a Fase II dependiendo de una única skill durante Fase I, la memoria resumida permite comenzar Fase II con esa técnica ya comprendida. Como la Fase I completa funciona como observación, **dos ejecuciones de esa única skill, sin haber mostrado ataque básico u otra técnica, ya bastan para esta herencia entre fases**. El umbral normal dentro de Fase II/III sigue siendo tres usos consecutivos.

Defender o curarse entre usos **no borra** el conocimiento de la Grulla.

Para romper el counter hay que mostrar una variación táctica real:

- otra técnica;
- otro control;
- un ataque básico.

---

## 3. Counter de ofensiva — TRAZO VACÍO

Aplica a:

- Palma Ardiente;
- Filo de Qi Metálico;
- Látigo de Agua;
- cualquier otra ofensiva concreta aprendida.

Lectura:

> la Grulla ya conoce la trayectoria, el ritmo y el cierre de esa técnica.

Telegraph de laboratorio:

> La Grulla deja de seguir el golpe: ya conoce exactamente dónde termina.

Mientras se repita la skill aprendida:

- daño = 0;
- quemadura/veneno/debuff asociado = 0;
- drenaje/efecto de recurso asociado = 0;
- efectos secundarios = 0;
- el qi gastado no se devuelve.

No es inmunidad al elemento.

Otra ofensiva del mismo elemento sigue siendo una herramienta distinta.

---

## 4. Counter de esquiva — PULSO FIJADO

Ejemplo principal:

`Paso de Nube Ligera`

Lectura:

> la Grulla deja de seguir la silueta y sigue la circulación que produce el desplazamiento.

Telegraph:

> La mirada abandona tu silueta y escucha el pulso que mueve tus pasos.

Si el jugador insiste en la misma técnica ya leída:

- la activación repetida no aporta su Esquiva contra la Grulla;
- efectos secundarios de esa misma técnica también se suprimen;
- el coste de qi sigue existiendo.

Esto no significa que la Grulla ignore toda Esquiva del juego.

Ha aprendido **Paso de Nube**, no el concepto universal de moverse.

---

## 5. Counter de guardia — RESONANCIA INTERNA

Ejemplo principal:

`Piel de Cobre`

Lectura:

> la formación encuentra la frecuencia exacta de esa protección repetida.

Telegraph:

> La campana cambia de tono hasta resonar dentro de la misma guardia.

Si vuelve a usarse esa misma técnica:

- no genera la Guardia esperada contra la Grulla;
- no genera su reserva/reducción asociada;
- secundarios de esa activación se anulan;
- el qi se consume.

No elimina DEFENDER ni otras técnicas defensivas.

---

## 6. Counter de control — ANCLA DEL VOTO

Ejemplo principal:

`Filamento de Agua`

Lectura:

> la Grulla aprende exactamente dónde cierra el lazo y ancla el vínculo antes de que vuelva a tensarse.

Telegraph:

> La pata inmóvil fija el vínculo. El mismo lazo ya no encuentra dónde cerrar.

Al repetir Filamento aprendido:

- la atadura/control falla;
- sus efectos secundarios se anulan;
- se mantiene el gasto de qi.

Esto convive con la Tenacidad normal de bosses; no la sustituye ni concede inmunidad universal a control.

Otra herramienta de control diferente puede seguir funcionando.

---

## 7. Counter de fortificación — CAMPANA INVERSA

Se conserva como contrato futuro.

Lectura:

> la Grulla reconoce las mismas juntas de la postura endurecida.

Telegraph:

> El eco encuentra las mismas juntas cada vez que endureces la postura.

Si la misma fortificación aprendida se repite:

- ese buff concreto de Defensa se suprime contra la Grulla;
- no se obtiene inmunidad global contra todas las fortificaciones.

No forma parte obligatoria del examen del Arco 1.

---

## 8. Regla de ruptura

Un conocimiento activo NO desaparece por:

```text
DEFENDER
RECOVER / curarse
usar consumible sin técnica alternativa
esperar
```

Sí puede romperse mediante:

```text
otra técnica
otro control
ataque básico
```

Esto evita el exploit:

```text
Palma
Palma
Palma
DEFENDER
Palma
Palma
Palma
DEFENDER
...
```

La Grulla no olvida una técnica sólo porque el jugador haga una pausa defensiva.

---

## 9. Coste y justicia

Una técnica ya comprendida:

- sigue pagando su coste;
- no recibe reembolso;
- muestra claramente el counter;
- sólo queda anulada si es exactamente la técnica aprendida.

La Grulla no obtiene:

- resistencia elemental universal;
- inmunidad universal a ofensivas;
- inmunidad universal a control;
- lectura de la siguiente acción;
- acceso al inventario oculto;
- acceso a cooldowns secretos.

---

## 10. Papel de los counters frente a las tres fases

### Fase I

No aprende counters activos durante la fase.

Observa y genera un resumen.

Su función sigue siendo PROGRAMADA.

### Fase II

Puede consolidar counters concretos por repetición.

Aquí el jugador descubre:

> la Grulla recuerda lo que le estás enseñando.

### Fase III

Mantiene counters concretos y además utiliza planes cortos.

La dificultad final surge de combinar:

- memoria;
- counters específicos;
- lectura de qi;
- planes rompibles;
- intenciones visibles.

No de aumentar arbitrariamente todos sus stats.

---

## 11. Contrato de habilidades de la Grulla

Se creó:

`adaptive/grulla-boss-ability-contract-v0.1.mjs`

El cerebro decide la intención.

El contrato declara cómo deberá resolverla el futuro executor.

Clasificación actual:

### Fase I

- Golpe de Ala — ataque básico;
- Campanada del Pico — golpe fuerte telegráfico;
- Pata Inmóvil — defensa/anclaje.

### Fase II

- Golpe de Ala;
- Tormenta de Mil Plumas — ataque + presión de qi;
- Cerrar las Alas — Guardia;
- Recordar el Filo — preparación adaptativa;
- Eco del Meridiano — presión sobre gasto de qi.

### Fase III

- Picotazo Blanco — ataque preciso;
- Campana sin Dueño — golpe fuerte + presión de qi;
- Ala Vacía — defensa evasiva;
- Pata Inmóvil — anclaje;
- Silencio entre Campanas — preparación de plan anti-repetición;
- Romper el Ritmo — remate condicionado al plan;
- Buscar el Pulso — preparación contra gasto sostenido de qi.

Todos consumen la acción de la Grulla.

No se introduce silencio/bloqueo general de técnicas.

---

## 12. Estado

Implementado en laboratorio:

- clasificación del counter por tipo;
- supresión completa de la skill concreta ya aprendida;
- no-reset por Defender/curación;
- ruptura por variación táctica real;
- announcement/telegraph exportable;
- contrato declarativo para todas las intenciones de la Grulla.

Todavía falta conectar esto al executor real de ver74 y simular las tres fases completas con builds reales de LianQi IV.
