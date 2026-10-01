"""Tests puros de VETERAN: no necesitan Combat Engine ni RNG."""
from __future__ import annotations

from dataclasses import dataclass,field
from types import SimpleNamespace

from player_policy_veteran import VETERAN_BASIC,choose_veteran_action


@dataclass
class Metrics:
    monster_damage_direct: float=0.0
    monster_damage_dot: float=0.0


def tech(tid,role,targeting,cost,**extra):
    return {
        "technique_id":tid,
        "role":role,
        "targeting":targeting,
        "qi_cost":cost,
        **extra,
    }


def state(*,hp=30,qi=37,round_no=1,monster_hp=20,damage=0,dot=False,control=False):
    compiled={
        "u":tech("u","OFFENSIVE","UNITARGET",6,control={"base":65} if control else None),
        "d":tech("d","DEFENSIVE","SELF",7),
        "a":tech("a","OFFENSIVE","AOE",9),
        VETERAN_BASIC:tech(VETERAN_BASIC,"BASIC_PROXY","UNITARGET",0),
    }
    return SimpleNamespace(
        player=SimpleNamespace(hp=float(hp),hp_max=30.0,qi=float(qi),absorption=0.0,dots=[{}] if dot else []),
        monster=SimpleNamespace(hp=float(monster_hp),hp_max=20.0,skip_next_action=False),
        compiled=compiled,
        player_defense=None,
        round_no=round_no,
        metrics=Metrics(monster_damage_direct=float(damage)),
    )


def run():
    # No gasta Qi inexistente.
    assert choose_veteran_action(state(qi=0))==VETERAN_BASIC

    # No abre defensa automáticamente en turno 1 a vida completa.
    assert choose_veteran_action(state())=="u"

    # Reacciona a presión ya observada cuando la vida bajó.
    s=state(hp=15,round_no=3,damage=8)
    assert choose_veteran_action(s)=="d"

    # Control propio es una decisión táctica válida sin mirar Tenacidad enemiga.
    assert choose_veteran_action(state(control=True))=="u"

    # Con Qi justo y vida comprometida conserva la reserva defensiva y usa básico.
    s=state(hp=18,qi=6,round_no=3,damage=5)
    assert choose_veteran_action(s)==VETERAN_BASIC

    print("PASS: VETERAN observable-only policy tests")


if __name__=="__main__":
    run()
