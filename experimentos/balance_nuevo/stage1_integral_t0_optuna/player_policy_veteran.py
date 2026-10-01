"""Policy VETERAN para LianQi I.

La policy optimiza decisiones, no estadísticas. Sólo usa estado observable de
la pelea y datos de las propias técnicas del jugador. No inspecciona RNG futuro
ni stats ocultos del monstruo.
"""
from __future__ import annotations

from dataclasses import dataclass

VETERAN_BASIC="__VETERAN_BASIC__"


@dataclass(frozen=True)
class VeteranPolicyConfig:
    critical_hp_ratio: float = 0.35
    defense_hp_ratio: float = 0.60
    reserve_qi_below_hp_ratio: float = 0.70
    observed_pressure_ratio: float = 0.08
    execute_monster_hp_ratio: float = 0.25


DEFAULT_VETERAN_CONFIG=VeteranPolicyConfig()


def _can_pay(state,c) -> bool:
    return float(state.player.qi) >= float(c["qi_cost"])


def _defense_active(state) -> bool:
    return state.player_defense is not None or float(state.player.absorption)>0


def _observed_pressure(state) -> float:
    """Daño ya observado por ronda / HP máximo; nunca estima tiradas futuras."""
    rounds=max(1,int(state.round_no)-1)
    received=(
        float(state.metrics.monster_damage_direct)
        + float(state.metrics.monster_damage_dot)
    )
    return received/rounds/max(1.0,float(state.player.hp_max))


def choose_veteran_action(state,config: VeteranPolicyConfig=DEFAULT_VETERAN_CONFIG) -> str:
    unitarget,defensive,aoe=state.compiled.keys() if False else (None,None,None)
    # La fuente de verdad del orden de técnicas ya vive en el Combat Engine.
    # Se obtiene por rol/targeting para no duplicar ROOT_TECHNIQUES aquí.
    offensive=[
        c for c in state.compiled.values()
        if c.get("role")!="DEFENSIVE" and c.get("technique_id")!=VETERAN_BASIC
    ]
    defenses=[
        c for c in state.compiled.values()
        if c.get("role")=="DEFENSIVE"
    ]
    single=[
        c for c in offensive
        if c.get("targeting")=="UNITARGET"
    ]
    aoes=[
        c for c in offensive
        if c.get("targeting")=="AOE"
    ]

    unit=single[0] if single else None
    defense=defenses[0] if defenses else None
    aoe=aoes[0] if aoes else None

    hp_ratio=max(0.0,float(state.player.hp)/max(1.0,float(state.player.hp_max)))
    monster_hp_ratio=max(
        0.0,
        float(state.monster.hp)/max(1.0,float(state.monster.hp_max)),
    )
    pressure=_observed_pressure(state)
    has_hostile_dot=bool(state.player.dots)

    if defense and not _defense_active(state) and _can_pay(state,defense):
        if hp_ratio<=config.critical_hp_ratio:
            return defense["technique_id"]
        if (
            hp_ratio<=config.defense_hp_ratio
            and (pressure>=config.observed_pressure_ratio or has_hostile_dot)
        ):
            return defense["technique_id"]

    # Si una técnica de Control propia está disponible, el veterano puede usarla
    # como herramienta táctica. Sólo lee su propio kit y el estado de skip ya
    # aplicado, no la Tenacidad oculta del enemigo.
    if unit and unit.get("control") and not state.monster.skip_next_action and _can_pay(state,unit):
        return unit["technique_id"]

    if unit and monster_hp_ratio<=config.execute_monster_hp_ratio and _can_pay(state,unit):
        return unit["technique_id"]

    reserve=0.0
    if (
        defense
        and not _defense_active(state)
        and hp_ratio<=config.reserve_qi_below_hp_ratio
    ):
        reserve=float(defense["qi_cost"])

    if unit and _can_pay(state,unit):
        if float(state.player.qi)-float(unit["qi_cost"])>=reserve:
            return unit["technique_id"]

    # En 1v1 la AOE es secundaria por diseño, pero sigue siendo una opción legal
    # si el unitarget no puede pagarse o su utilidad especial justifica el gasto.
    if aoe and _can_pay(state,aoe):
        if float(state.player.qi)-float(aoe["qi_cost"])>=reserve:
            return aoe["technique_id"]

    # Con HP sano, gastar el último bloque de Qi en el unitarget puede ser mejor
    # que reservar para una defensa que todavía no está justificada.
    if unit and hp_ratio>config.reserve_qi_below_hp_ratio and _can_pay(state,unit):
        return unit["technique_id"]

    return VETERAN_BASIC
