"""ETAPA 6 — valor del tercer Arraigo frente a Control.

Pregunta única:
si DEF_CAP2 elimina la tercera unidad incremental de DEF,
¿el tercer Arraigo conserva valor mecánico suficiente por Tenacidad + extensión?

No se simula daño.
No se fija una técnica enemiga canónica.
Se usa la fórmula CANON de Control/Tenacidad.

Fórmula:
P(Control) = clamp(control_effective - tenacity, 5, 100)

Tierra aporta +5 Tenacidad CANON.
Piel aporta +3 Tenacidad por Arraigo.
"""
from __future__ import annotations


def clamp(x: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, x))


EARTH_ROOT_TENACITY = 5.0
TENACITY_PER_ARRAIGO = 3.0

TENACITY_EARTH_ONLY = EARTH_ROOT_TENACITY
TENACITY_2 = EARTH_ROOT_TENACITY + 2 * TENACITY_PER_ARRAIGO
TENACITY_3 = EARTH_ROOT_TENACITY + 3 * TENACITY_PER_ARRAIGO


def control_probability(control_effective: float, tenacity: float) -> float:
    return clamp(control_effective - tenacity, 5.0, 100.0) / 100.0


def three_attempt_example(control_effective: float = 65.0) -> dict:
    """Ejemplo ilustrativo, no perfil enemigo canónico.

    Horizonte fijo de tres intentos:
    - estado con 2 Arraigos: dos turnos protegidos y luego Piel expira;
    - estado con 3 Arraigos: la llegada al máximo activa +1 turno y mantiene
      los tres turnos protegidos.
    """
    p_earth = control_probability(control_effective, TENACITY_EARTH_ONLY)
    p_2 = control_probability(control_effective, TENACITY_2)
    p_3 = control_probability(control_effective, TENACITY_3)

    expected_success_2 = 2 * p_2 + p_earth
    expected_success_3 = 3 * p_3

    no_success_2 = (1 - p_2) ** 2 * (1 - p_earth)
    no_success_3 = (1 - p_3) ** 3

    return {
        "control_effective_example": control_effective,
        "earth_only_tenacity": TENACITY_EARTH_ONLY,
        "two_arraigo_tenacity": TENACITY_2,
        "three_arraigo_tenacity": TENACITY_3,
        "p_control_earth_only": p_earth,
        "p_control_two_arraigo": p_2,
        "p_control_three_arraigo": p_3,
        "expected_successes_two_arraigo_horizon3": expected_success_2,
        "expected_successes_three_arraigo_horizon3": expected_success_3,
        "expected_successes_reduction": expected_success_2 - expected_success_3,
        "prob_no_success_two_arraigo_horizon3": no_success_2,
        "prob_no_success_three_arraigo_horizon3": no_success_3,
        "prob_no_success_gain": no_success_3 - no_success_2,
    }


if __name__ == "__main__":
    print("Tenacidad Tierra sin Piel:", TENACITY_EARTH_ONLY)
    print("Tenacidad con 2 Arraigos:", TENACITY_2)
    print("Tenacidad con 3 Arraigos:", TENACITY_3)
    print()
    print("Aporte exacto del tercer Arraigo, fuera de clamps:")
    print("-3 pp de probabilidad de Control por intento mientras Piel sigue activa.")
    print("El turno extra conserva +9 Tenacidad frente a Piel expirada.")
    print()
    print("Ejemplo ilustrativo con Control efectivo 65:")
    for key, value in three_attempt_example().items():
        print(f"{key}: {value}")
