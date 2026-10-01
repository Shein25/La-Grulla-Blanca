# Rata de Qi — cierre T0 numérico

**Fecha:** 2026-10-01  
**Estado:** T0 READY / T1 PENDIENTE DE RECALIBRACIÓN  
**Rama:** `experiment/arc1-monster-resource-none-v0.1`

## Selección humana

Se selecciona el **trial 4254** de la corrida `RATA_T0_HEAVY`.

La selección no fue automática. El frente Pareto sólo delimitó compromisos; la
elección se realizó por identidad de diseño de la Rata de Qi como amenaza
sobrenatural inicial, sencilla e instintiva.

## Perfil T0 aprobado

```text
id            = rata_qi
resource_model= NONE

HP            = 21
Qi max        = N/A (null)
Precisión     = 80
Evasión       = 0
Defensa       = 0
Tenacidad     = 0
Control       = 0
Crítico       = 5%
Daño crítico  = x1.50
Ataque básico = 2d4
Técnica T0    = NONE

AI cognition  = INSTINTIVO
AI social     = COLONIA
```

## Evidencia Heavy

Configuración de la corrida:

```text
search trials              = 5000
search fights/context      = 200
revalidation candidates    = hasta 100
revalidation fights/context= 2500
high precision candidates  = 7
high precision fights/context = 20000
primary contexts/candidate = 10
```

Trial 4254 en high precision:

```text
peleas                      = 200000
victoria jugador            = 100.000%
HP final medio jugador      = 88.826%
presión HP media            = 11.174%
HP final p10                = 77.419%
HP final mediana            = 90.323%
HP final p90                = 100.000%
rondas medias               = 2.766
```

Sensibilidad por raíz observada:

```text
Agua    HP final medio = 91.91%
Fuego   HP final medio = 90.91%
Metal   HP final medio = 86.42%
Tierra  HP final medio = 87.63%
Viento  HP final medio = 87.26%
```

Sensibilidad por equipo:

```text
EXPECTED_STAGE   HP final medio = 88.98%
MANDATORY_ENTRY  HP final medio = 88.67%
diferencia                      = 0.31 pp
```

No se observó dependencia fuerte del loadout.

## Motivo de selección

El candidato mantiene la identidad con un perfil mecánico simple:

- sin Defensa artificial;
- sin Evasión artificial;
- sin Tenacidad artificial;
- sin Control;
- sin técnica T0;
- presión conseguida principalmente mediante HP suficiente para sostener un
  encuentro corto y un ataque básico moderado.

Los candidatos de presión inferior tendían a ser casi decorativos. Los de
presión superior introducían mortalidad creciente y una identidad menos
adecuada para la amenaza sobrenatural más baja.

## Qi de monstruos

El cierre global del Arco 1 establece:

```text
resource_model = NONE
qi_max = null
```

Por tanto, `qi_max=null` es N/A autoritativo y no bloquea READY.

## Adaptación

El cierre T0 **no valida números adaptativos**.

Secuencia obligatoria:

```text
Rata T0 READY
→ recalibrar T1 Reflejo de Madriguera
→ validar T1
→ T2
→ T3
→ T4 Mordisco Frenético
```

Identidades conservadas del laboratorio adaptativo previo:

- T1: `Reflejo de Madriguera`, familia `EVADE_NEXT`;
- T2: reconocimiento persistente / anticipación elegible;
- T3: counter específico de especie;
- T4: `Mordisco Frenético`, ofensiva física instintiva basada en el ataque
  básico T0 y candidata a multimpacto.

No se conserva ningún bono, escalar, número de impactos, precisión, cooldown
ni daño adaptativo anterior como número canónico.

## Guardias

- no `main`;
- no merge;
- T2–T4 siguen bloqueados;
- Definitivas fuera del balance de monstruos;
- no segunda fuente de stats;
- no compatibilidad con perfiles numéricos antiguos.
