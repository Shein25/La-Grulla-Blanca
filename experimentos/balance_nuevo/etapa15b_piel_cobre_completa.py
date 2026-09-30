"""ETAPA 15B — Piel de Cobre completa.

Benchmark integral de las tres familias:
F = Fortificación
S = Estabilidad
A = Aguante

Incluye:
- base y etapas T1/T2/T3;
- 27 rutas mixables;
- COMMON / PRECISE / HEAVY / DANGEROUS;
- 2 y 3 enemigos;
- stress LAB de Control;
- chequeo de curación/duración.

Guardia:
- usa estadísticas LianQi I como marco mecánico;
- NO sustituye validación futura con enemigos LianQi II–IV;
- no modifica runtime.

Recalibración de Aguante:
AGUANTE_DUR_CAP1:
- la familia Aguante puede aportar como máximo +1 turno a la duración base;
- Tierra Persistente concede ese +1;
- Montaña Persistente también puede concederlo si no existe ya;
- Suelo que Sostiene deja de añadir otro turno por sinergia.
Esto evita reabrir el escalado multiimpacto corregido con DEF_CAP2.
"""
from __future__ import annotations

import argparse
import csv
import itertools
import math
import random
import statistics

PLAYER_HP = 33.0   # Tierra: 30 * 1.10 -> 33
PLAYER_QI = 31
PLAYER_DEF = 1.0
PLAYER_EVA = 5.0
PLAYER_PREC = 100.0
ENEMY_TOTAL_HP = 28
ENEMY_EVA = 20.0
ENEMY_DEF = 2.0

PROFILES = {
    "COMMON": (1, 90.0, "2d4+1"),
    "PRECISE": (1, 100.0, "2d4+1"),
    "HEAVY": (1, 90.0, "1d6+3"),
    "DANGEROUS": (1, 100.0, "1d6+3"),
    "2EN": (2, 90.0, "2d4+1"),
    "3EN": (3, 90.0, "2d4+1"),
}


def round_half_up(x: float) -> int:
    return int(math.floor(x + 0.5))


def roll(rng: random.Random, code: str) -> float:
    if code == "2d4+4":
        return rng.randint(1, 4) + rng.randint(1, 4) + 4
    if code == "1d4+4":
        return rng.randint(1, 4) + 4
    if code == "2d4+1":
        return rng.randint(1, 4) + rng.randint(1, 4) + 1
    if code == "1d6+3":
        return rng.randint(1, 6) + 3
    raise ValueError(code)


def hit_damage(
    rng: random.Random,
    precision: float,
    target_evasion: float,
    dice: str,
    target_def: float,
    crit_chance: float = 5.0,
    crit_damage: float = 1.50,
) -> tuple[bool, int]:
    p_hit = max(5.0, min(100.0, precision - target_evasion)) / 100.0
    if rng.random() >= p_hit:
        return False, 0

    damage = roll(rng, dice)
    if rng.random() < crit_chance / 100.0:
        damage *= crit_damage

    return True, round_half_up(max(0.0, damage - target_def))


def split_hp(total: int, count: int) -> list[float]:
    q, r = divmod(total, count)
    return [float(q + (1 if i < r else 0)) for i in range(count)]


def path_config(t1: str | None, t2: str | None, t3: str | None) -> dict:
    path = "".join(value if value else "-" for value in (t1, t2, t3))

    tierra_persistente = t1 == "A"
    suelo = t2 == "A"
    montana = t3 == "A"

    # AGUANTE_DUR_CAP1:
    # T1 y T3 pueden conceder el mismo +1; nunca se acumulan entre sí.
    duration_bonus = 1 if (tierra_persistente or montana) else 0

    return {
        "path": path,

        "corteza": t1 == "F",
        "estratos": t2 == "F",
        "roca": t3 == "F",

        "centro": t1 == "S",
        "raiz": t2 == "S",
        "inamovible": t3 == "S",

        "tierra_persistente": tierra_persistente,
        "suelo": suelo,
        "montana": montana,

        "base_duration": 3 + duration_bonus,
    }


def tenacity_total(cfg: dict, arraigo: int) -> float:
    # Raíz Tierra +5 Tenacity CANON.
    per_arraigo = 5 if cfg["centro"] else 3

    value = 5 + per_arraigo * arraigo

    if cfg["raiz"] and arraigo >= 2:
        value += 5

    if cfg["inamovible"] and arraigo >= 1:
        value += 5

    return float(value)


def run_variant(
    cfg: dict,
    enemy_count: int,
    enemy_precision: float,
    enemy_damage: str,
    fights: int,
    seed: int,
) -> dict:
    rng = random.Random(seed)

    wins = 0
    hp_remaining = []
    rounds = []
    fallback = 0

    max_arraigo = []
    base_extensions = []
    healing = []
    estrato_uses = []
    roca_uses = []

    for _ in range(fights):
        hp = PLAYER_HP
        qi = PLAYER_QI
        enemy_hps = split_hp(ENEMY_TOTAL_HP, enemy_count)

        round_no = 0
        defense_used = False
        used_basic = False

        peso_stacks = [0] * enemy_count
        peso_duration = [0] * enemy_count

        active = False
        piel_left = 0
        arraigo = 0
        large_hit_used = False
        base_extension_used = False

        estrato = False
        roca_guard = False

        suelo_heal_used = False
        montana_max_heal_used = False
        montana_low_heal_used = False

        fight_max_arraigo = 0
        fight_healing = 0.0
        fight_estrato_uses = 0
        fight_roca_uses = 0

        while hp > 0 and any(value > 0 for value in enemy_hps):
            round_no += 1

            # TURN_START del usuario.
            if (
                active
                and piel_left > 0
                and cfg["roca"]
                and arraigo == 3
            ):
                roca_guard = True

            # Acción del usuario.
            if not defense_used and round_no == 1:
                qi -= 7
                defense_used = True

                active = True
                piel_left = cfg["base_duration"]
                arraigo = 1
                fight_max_arraigo = 1

            else:
                target = next(
                    i for i, value in enumerate(enemy_hps)
                    if value > 0
                )

                target_evasion = ENEMY_EVA - 3.0 * peso_stacks[target]

                if qi >= 6:
                    hit, damage = hit_damage(
                        rng,
                        PLAYER_PREC,
                        target_evasion,
                        "2d4+4",
                        ENEMY_DEF,
                    )
                    qi -= 6

                    if hit:
                        peso_stacks[target] = min(
                            2, peso_stacks[target] + 1
                        )
                        peso_duration[target] = 2
                else:
                    _, damage = hit_damage(
                        rng,
                        PLAYER_PREC,
                        target_evasion,
                        "1d4+4",
                        ENEMY_DEF,
                    )
                    used_basic = True

                enemy_hps[target] -= damage

            # Acciones enemigas.
            for index, enemy_hp in enumerate(enemy_hps):
                if enemy_hp <= 0 or hp <= 0:
                    continue

                p_hit = max(
                    5.0,
                    min(100.0, enemy_precision - PLAYER_EVA),
                ) / 100.0

                if rng.random() >= p_hit:
                    continue

                raw_damage = roll(rng, enemy_damage)
                if rng.random() < 0.05:
                    raw_damage *= 1.50

                target_def = PLAYER_DEF

                if active and piel_left > 0:
                    arraigo_def = (
                        {1: 2.0, 2: 3.0, 3: 3.0}[arraigo]
                        if cfg["corteza"]
                        else {1: 1.0, 2: 2.0, 3: 2.0}[arraigo]
                    )
                    target_def += 2.0 + arraigo_def

                use_estrato = (
                    active and piel_left > 0 and estrato
                )
                use_roca = (
                    active and piel_left > 0 and roca_guard
                )

                if use_estrato:
                    target_def += 2.0

                if use_roca:
                    target_def += 3.0

                hp_damage = round_half_up(
                    max(0.0, raw_damage - target_def)
                )

                if use_estrato:
                    estrato = False
                    fight_estrato_uses += 1

                if use_roca:
                    roca_guard = False
                    fight_roca_uses += 1

                hp -= hp_damage

                # Arraigo sólo si el impacto quitó Vida.
                if active and piel_left > 0 and hp_damage > 0:
                    gain = 1

                    if (
                        not large_hit_used
                        and hp_damage >= 0.10 * PLAYER_HP
                    ):
                        gain = 2
                        large_hit_used = True

                    old_arraigo = arraigo
                    arraigo = min(3, arraigo + gain)
                    fight_max_arraigo = max(
                        fight_max_arraigo, arraigo
                    )

                    if (
                        cfg["estratos"]
                        and arraigo > old_arraigo
                        and arraigo in (2, 3)
                    ):
                        estrato = True

                    if old_arraigo < 3 and arraigo == 3:
                        if not base_extension_used:
                            piel_left += 1
                            base_extension_used = True

                        if cfg["suelo"] and not suelo_heal_used:
                            amount = 0.05 * PLAYER_HP
                            actual = min(amount, PLAYER_HP - hp)
                            hp += actual
                            fight_healing += actual
                            suelo_heal_used = True

                        if (
                            cfg["montana"]
                            and not montana_max_heal_used
                        ):
                            amount = 0.05 * PLAYER_HP
                            actual = min(amount, PLAYER_HP - hp)
                            hp += actual
                            fight_healing += actual
                            montana_max_heal_used = True

                if (
                    cfg["montana"]
                    and active
                    and piel_left > 0
                    and hp > 0
                    and hp / PLAYER_HP < 0.30
                    and not montana_low_heal_used
                ):
                    amount = 0.05 * PLAYER_HP
                    actual = min(amount, PLAYER_HP - hp)
                    hp += actual
                    fight_healing += actual
                    montana_low_heal_used = True

            # TURN_END usuario.
            if active and piel_left > 0:
                piel_left -= 1

                if piel_left <= 0:
                    active = False
                    arraigo = 0
                    estrato = False
                    roca_guard = False

            for index in range(enemy_count):
                if peso_duration[index] > 0:
                    peso_duration[index] -= 1

                    if peso_duration[index] <= 0:
                        peso_stacks[index] = 0

            if round_no > 100:
                raise RuntimeError("combate excedió 100 rondas")

        wins += int(
            all(value <= 0 for value in enemy_hps) and hp > 0
        )
        fallback += int(used_basic)

        hp_remaining.append(max(0.0, hp))
        rounds.append(round_no)
        max_arraigo.append(fight_max_arraigo)
        base_extensions.append(int(base_extension_used))
        healing.append(fight_healing)
        estrato_uses.append(fight_estrato_uses)
        roca_uses.append(fight_roca_uses)

    return {
        "win_rate": wins / fights,
        "mean_rounds": statistics.fmean(rounds),
        "mean_hp_remaining_percent": (
            statistics.fmean(hp_remaining) / PLAYER_HP
        ),
        "fallback_rate": fallback / fights,
        "mean_max_arraigo": statistics.fmean(max_arraigo),
        "base_extension_rate": statistics.fmean(base_extensions),
        "mean_healing_percent": (
            statistics.fmean(healing) / PLAYER_HP
        ),
        "mean_estrato_uses": statistics.fmean(estrato_uses),
        "mean_roca_uses": statistics.fmean(roca_uses),
    }


def run_control_stress(
    cfg: dict,
    fights: int,
    seed: int,
    control_effective: float = 65.0,
) -> dict:
    """Stress LAB ilustrativo; NO perfil enemigo canónico.

    Un enemigo COMMON intenta SKIP_ACTION después de cada impacto directo
    conectado. Para aislar la identidad reactiva de Piel, el intento de
    Control se resuelve después de ON_HP_DAMAGE/Arraigo en este runner.
    """

    rng = random.Random(seed)

    wins = 0
    hp_remaining = []
    skipped_actions = []

    control_attempts = 0
    control_successes = 0

    control_duration_extensions = 0
    precision_triggers = 0

    for _ in range(fights):
        hp = PLAYER_HP
        qi = PLAYER_QI
        enemy_hp = float(ENEMY_TOTAL_HP)

        round_no = 0
        defense_used = False
        skip_next_action = False

        peso_stacks = 0
        peso_duration = 0

        active = False
        piel_left = 0
        arraigo = 0
        large_hit_used = False
        base_extension_used = False

        estrato = False
        roca_guard = False

        control_extension_used = False
        inamovible_trigger_used = False
        precision_buff = False

        suelo_heal_used = False
        montana_max_heal_used = False
        montana_low_heal_used = False

        skipped = 0

        while hp > 0 and enemy_hp > 0:
            round_no += 1

            if (
                active
                and piel_left > 0
                and cfg["roca"]
                and arraigo == 3
            ):
                roca_guard = True

            if skip_next_action:
                skip_next_action = False
                skipped += 1

            elif not defense_used and round_no == 1:
                qi -= 7
                defense_used = True
                active = True
                piel_left = cfg["base_duration"]
                arraigo = 1

            else:
                precision = PLAYER_PREC + (
                    10.0 if precision_buff else 0.0
                )
                target_evasion = ENEMY_EVA - 3.0 * peso_stacks

                if qi >= 6:
                    hit, damage = hit_damage(
                        rng,
                        precision,
                        target_evasion,
                        "2d4+4",
                        ENEMY_DEF,
                    )
                    qi -= 6

                    if precision_buff:
                        precision_buff = False

                    if hit:
                        peso_stacks = min(2, peso_stacks + 1)
                        peso_duration = 2
                else:
                    _, damage = hit_damage(
                        rng,
                        PLAYER_PREC,
                        target_evasion,
                        "1d4+4",
                        ENEMY_DEF,
                    )

                enemy_hp -= damage

            if enemy_hp <= 0:
                break

            p_hit = max(5.0, min(100.0, 90.0 - PLAYER_EVA)) / 100.0

            if rng.random() < p_hit:
                raw_damage = roll(rng, "2d4+1")

                if rng.random() < 0.05:
                    raw_damage *= 1.50

                target_def = PLAYER_DEF

                if active and piel_left > 0:
                    arraigo_def = (
                        {1: 2.0, 2: 3.0, 3: 3.0}[arraigo]
                        if cfg["corteza"]
                        else {1: 1.0, 2: 2.0, 3: 2.0}[arraigo]
                    )
                    target_def += 2.0 + arraigo_def

                use_estrato = (
                    active and piel_left > 0 and estrato
                )
                use_roca = (
                    active and piel_left > 0 and roca_guard
                )

                if use_estrato:
                    target_def += 2.0

                if use_roca:
                    target_def += 3.0

                hp_damage = round_half_up(
                    max(0.0, raw_damage - target_def)
                )

                if use_estrato:
                    estrato = False

                if use_roca:
                    roca_guard = False

                hp -= hp_damage

                # Reacción de Arraigo.
                if active and piel_left > 0 and hp_damage > 0:
                    gain = 1

                    if (
                        not large_hit_used
                        and hp_damage >= 0.10 * PLAYER_HP
                    ):
                        gain = 2
                        large_hit_used = True

                    old_arraigo = arraigo
                    arraigo = min(3, arraigo + gain)

                    if (
                        cfg["estratos"]
                        and arraigo > old_arraigo
                        and arraigo in (2, 3)
                    ):
                        estrato = True

                    if old_arraigo < 3 and arraigo == 3:
                        if not base_extension_used:
                            piel_left += 1
                            base_extension_used = True

                        if cfg["suelo"] and not suelo_heal_used:
                            amount = 0.05 * PLAYER_HP
                            hp += min(amount, PLAYER_HP - hp)
                            suelo_heal_used = True

                        if (
                            cfg["montana"]
                            and not montana_max_heal_used
                        ):
                            amount = 0.05 * PLAYER_HP
                            hp += min(amount, PLAYER_HP - hp)
                            montana_max_heal_used = True

                if (
                    cfg["montana"]
                    and active
                    and piel_left > 0
                    and hp > 0
                    and hp / PLAYER_HP < 0.30
                    and not montana_low_heal_used
                ):
                    amount = 0.05 * PLAYER_HP
                    hp += min(amount, PLAYER_HP - hp)
                    montana_low_heal_used = True

                # Control después de la reacción de Piel, sólo para este LAB.
                if active and piel_left > 0:
                    control_attempts += 1

                    tenacity = tenacity_total(cfg, arraigo)
                    p_control = max(
                        5.0,
                        min(
                            100.0,
                            control_effective - tenacity,
                        ),
                    ) / 100.0

                    if rng.random() < p_control:
                        control_successes += 1
                        skip_next_action = True

                    else:
                        if (
                            cfg["centro"]
                            and cfg["raiz"]
                            and not control_extension_used
                        ):
                            piel_left += 1
                            control_extension_used = True
                            control_duration_extensions += 1

                        if (
                            cfg["inamovible"]
                            and arraigo == 3
                            and not inamovible_trigger_used
                        ):
                            precision_buff = True
                            inamovible_trigger_used = True
                            precision_triggers += 1

            if active and piel_left > 0:
                piel_left -= 1

                if piel_left <= 0:
                    active = False
                    arraigo = 0
                    estrato = False
                    roca_guard = False

            if peso_duration > 0:
                peso_duration -= 1
                if peso_duration <= 0:
                    peso_stacks = 0

            if round_no > 100:
                raise RuntimeError("stress de Control excedió 100 rondas")

        wins += int(enemy_hp <= 0 and hp > 0)
        hp_remaining.append(max(0.0, hp))
        skipped_actions.append(skipped)

    return {
        "win_rate": wins / fights,
        "mean_hp_remaining_percent": (
            statistics.fmean(hp_remaining) / PLAYER_HP
        ),
        "control_success_rate": (
            control_successes / control_attempts
            if control_attempts else 0.0
        ),
        "mean_skipped_actions": statistics.fmean(skipped_actions),
        "control_duration_extension_rate": (
            control_duration_extensions / fights
        ),
        "inamovible_precision_trigger_rate": (
            precision_triggers / fights
        ),
    }


def full_screen(fights: int, seed: int) -> list[dict]:
    rows = []
    serial = 0

    for path_tuple in itertools.product("FSA", repeat=3):
        cfg = path_config(*path_tuple)

        for profile, (count, precision, damage) in PROFILES.items():
            result = run_variant(
                cfg,
                count,
                precision,
                damage,
                fights,
                seed + serial,
            )
            serial += 1

            rows.append({
                "provenance": "LAB",
                "path": cfg["path"],
                "profile": profile,
                "base_duration": cfg["base_duration"],
                **result,
            })

    return rows


def control_screen(fights: int, seed: int) -> list[dict]:
    rows = []

    for serial, path_tuple in enumerate(
        itertools.product("FSA", repeat=3)
    ):
        cfg = path_config(*path_tuple)

        rows.append({
            "provenance": "LAB",
            "path": cfg["path"],
            **run_control_stress(
                cfg,
                fights,
                seed + serial,
            ),
        })

    return rows


def export(rows: list[dict], path: str) -> None:
    fields = sorted({key for row in rows for key in row})

    with open(path, "w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--fights", type=int, default=8_000)
    ap.add_argument("--control-fights", type=int, default=8_000)
    ap.add_argument("--seed", type=int, default=20260929)
    ap.add_argument("--csv", default="etapa15b_piel_27_paths.csv")
    ap.add_argument(
        "--control-csv",
        default="etapa15b_piel_control_27_paths.csv",
    )
    args = ap.parse_args()

    rows = full_screen(args.fights, args.seed)
    control_rows = control_screen(args.control_fights, args.seed)

    export(rows, args.csv)
    export(control_rows, args.control_csv)

    print(f"CSV paths: {args.csv} ({len(rows)} escenarios)")
    print(
        f"CSV control: {args.control_csv} "
        f"({len(control_rows)} escenarios)"
    )
