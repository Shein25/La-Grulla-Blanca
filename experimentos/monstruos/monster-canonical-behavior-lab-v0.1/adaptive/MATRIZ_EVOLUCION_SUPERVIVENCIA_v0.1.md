# Matriz experimental — Evolución de Supervivencia v0.1

**Estado:** EXPERIMENTAL / NO CANÓNICO.

## Regla de diseño

La primera evolución no aumenta daño ni HP. Enseña al monstruo a **sobrevivir**:

```text
encuentros repetidos
→ experiencia adaptativa
→ Evolución I
→ perfil cognitivo avanza como máximo un escalón
→ se desbloquea 1 acción defensiva
→ el Monster Combat AI existente decide cuándo usarla
```

La técnica canónica conserva prioridad absoluta cuando `CADENCE_COMPAT` marca su ronda.

## Umbrales provisionales

- criatura común: `6 XP`;
- criatura única: `4 XP`;
- encuentro con al menos una ronda: `+1 XP`;
- si durante ese encuentro llegó a HP bajo **o** sufrió un golpe fuerte observado: `+1 XP` adicional;
- máximo: `2 XP` por encuentro.

Por tanto:

- común: 3 encuentros duros o 6 ordinarios;
- único: 2 encuentros duros o 4 ordinarios.

Esto evita evolucionar por permanecer inactivo dentro de un combate.

## Evolución I candidata

| Monstruo | Cognición base → E1 | Defensa aprendida | Efecto candidato | XP |
|---|---|---|---|---:|
| Rata de qi | INSTINTIVO → REACTIVO_1 | **Reflejo de Madriguera** | +25 esquiva, 1 acción | 6 |
| Serpiente de qi | REACTIVO_1 → CAZADOR_2 | **Muda del Cauce** | +20 esquiva, 1 acción | 6 |
| Lobo espiritual | CAZADOR_2 → TACTICO_3 | **Paso de la Cola Vigilante** | +20 esquiva, 1 acción | 6 |
| Eco del Caído | REACTIVO_1 → CAZADOR_2 | **Guardia del Último Ensayo** | −35% próximo golpe | 4 |
| Pez lunar | CAZADOR_2 → TACTICO_3 | **Giro de Corriente Ciega** | +20 esquiva, 1 acción | 6 |
| Sombra ahogada | TACTICO_3 → MASTER_4 | **Disolverse en Marea** | −30% próximo golpe | 4 |
| Centinela de plumas | REACTIVO_1 → CAZADOR_2 | **Cierre de Plumas Pétreas** | −35% próximo golpe | 4 |
| Devorador de niebla | TACTICO_3 → MASTER_4 | **Cuerpo de Bruma Replegada** | −30% próximo golpe | 6 |
| Avispa de jade | INSTINTIVO → REACTIVO_1 | **Quiebro de Jade** | +25 esquiva, 1 acción | 6 |
| Macaco ladrón | CAZADOR_2 → TACTICO_3 | **Salto del Ladrón** | +20 esquiva, 1 acción | 6 |
| Sapo de ceniza | INSTINTIVO → REACTIVO_1 | **Piel de Brasa Muerta** | −30% próximo golpe | 6 |
| Sapo Caldera | REACTIVO_1 → CAZADOR_2 | **Cierre de las Tres Gargantas** | −35% próximo golpe | 4 |
| Escarabajo de hierro | INSTINTIVO → REACTIVO_1 | **Cierre de Caparazón** | −40% próximo golpe | 6 |
| Rey Escarabajo | CAZADOR_2 → TACTICO_3 | **Diagrama de Placas** | −40% próximo golpe | 4 |
| Anguila estelar | REACTIVO_1 → CAZADOR_2 | **Desliz de Meridiano** | +20 esquiva, 1 acción | 6 |
| Guardián de coral | TACTICO_3 → MASTER_4 | **Arrecife Replegado** | −35% próximo golpe | 4 |
| Halcón de tormenta | CAZADOR_2 → TACTICO_3 | **Ascenso Contraviento** | +25 esquiva, 1 acción | 6 |
| Mantis de nube | MASTER_4 → MASTER_4 | **Velo de Nube Cortada** | +20 esquiva, 1 acción | 4 |

Todas las defensas consumen la acción del monstruo y proponen **2 rondas de cooldown**. No son buffs gratuitos añadidos al ataque.

## Política de decisión balanceada

La defensa de Evolución I se calibra contra la preferencia ofensiva que el monstruo ya posee.

Objetivo:

```text
sano                         → atacar
HP bajo                      → ~50/50 atacar o sobrevivir
golpe fuerte pero HP sano    → atacar
HP bajo + golpe fuerte       → supervivencia prioritaria
defensa en cooldown          → atacar
jugador también bajo de HP   → el perfil más inteligente tiende a arriesgar y rematar
```

Esto evita dos extremos:

- **tortuga:** defenderse constantemente;
- **evolución decorativa:** aprender defensa pero casi nunca usarla.

## Separación de responsabilidades

Esta matriz no crea un motor nuevo.

```text
persistencia adaptativa (futura)
→ survivalXp / evolutionStage
→ effectiveKit + perfil cognitivo efectivo
→ Monster Combat AI existente
→ intent defensivo
→ [GAP] executor defensivo de monstruos
```

El último paso aún no existe en ver74. La decisión puede probarse, pero ejecutar `EVADE_NEXT` / `MITIGATE_NEXT` requiere un bridge/executor de combate. Ese gap debe cerrarse antes de producción.
