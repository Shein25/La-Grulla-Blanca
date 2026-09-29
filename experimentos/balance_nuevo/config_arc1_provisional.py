"""Configuración del rediseño Arco 1.

Sólo contiene datos del contrato NUEVO.
Nada de este archivo se deriva de ver74.

Etiquetas:
- CANON: cerrado por contrato.
- PROVISIONAL: cifra actual de diseño pendiente de benchmark.
- LAB: candidato de simulación, nunca canon automático.
"""

ROOTS = {
    "fuego": {
        "status": "CANON",
        "damage_direct_percent": 10.0,
        "crit_chance": 5.0,
    },
    "metal": {
        "status": "CANON",
        "percent_penetration": 10.0,
        "precision": 5.0,
    },
    "agua": {
        "status": "CANON",
        "qi_cost_percent": -10.0,
        "control": 5.0,
    },
    "tierra": {
        "status": "CANON",
        "hp_max_percent": 10.0,
        "tenacity": 5.0,
    },
    "viento": {
        "status": "CANON",
        "evasion": 10.0,
        "crit_damage": 0.05,
    },
}

BASE_OFFENSIVE = {
    "palma_ardiente": {
        "status": "PROVISIONAL",
        "element": "fuego", "nominal_damage": 10.0, "qi_cost": 6.0,
        "precision": 0.0, "crit_chance": 0.0, "percent_penetration": 0.0,
    },
    "destello_plata": {
        "status": "PROVISIONAL",
        "element": "metal", "nominal_damage": 9.0, "qi_cost": 6.0,
        "precision": 0.0, "crit_chance": 0.0, "percent_penetration": 10.0,
    },
    "latigazo_marea": {
        "status": "PROVISIONAL",
        "element": "agua", "nominal_damage": 8.0, "qi_cost": 7.0,
        "precision": 0.0, "crit_chance": 0.0, "percent_penetration": 0.0,
    },
    "golpe_montana": {
        "status": "PROVISIONAL",
        "element": "tierra", "nominal_damage": 9.0, "qi_cost": 6.0,
        "precision": 0.0, "crit_chance": 0.0, "percent_penetration": 0.0,
    },
    "lanza_nubes": {
        "status": "PROVISIONAL",
        "element": "viento", "nominal_damage": 8.0, "qi_cost": 6.0,
        "precision": 5.0, "crit_chance": 5.0, "percent_penetration": 0.0,
    },
}

# Dos amplitudes con la MISMA media nominal para estudiar variabilidad sin
# confundirla con potencia.
DICE_CANDIDATES_LAB = {
    10.0: {"narrow": "2d4+5", "wide": "2d6+3"},
    9.0:  {"narrow": "2d4+4", "wide": "2d6+2"},
    8.0:  {"narrow": "2d4+3", "wide": "2d6+1"},
    7.0:  {"narrow": "2d4+2", "wide": "2d6"},
    6.0:  {"narrow": "2d4+1", "wide": "2d6-1"},
}

# Perfiles puramente LAB para sensibilidad. No representan LianQi I.
TARGET_SENSITIVITY_LAB = {
    "LAB_A": {"defense": 0.0, "evasion": 0.0},
    "LAB_B": {"defense": 2.0, "evasion": 15.0},
    "LAB_C": {"defense": 4.0, "evasion": 30.0},
    "LAB_D": {"defense": 6.0, "evasion": 45.0},
}

# Progresión garantizada: el contrato sólo permite crecer automáticamente
# HP/Qi/acceso. Los valores exactos permanecen intencionalmente vacíos.
STAGES = {
    "LianQi_I":   {"hp": None, "qi": None, "unlocks": "BASE"},
    "LianQi_II":  {"hp": None, "qi": None, "unlocks": "TRAMO_I"},
    "LianQi_III": {"hp": None, "qi": None, "unlocks": "TRAMO_II"},
    "LianQi_IV":  {"hp": None, "qi": None, "unlocks": "TRAMO_III"},
}
