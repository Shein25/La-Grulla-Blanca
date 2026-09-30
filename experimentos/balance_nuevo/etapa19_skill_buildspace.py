"""ETAPA 19 — espacio legal de builds para simulación masiva.

Cuenta y enumera configuraciones de habilidades sin mezclar todavía sus efectos.
El objetivo es que Colab pueda recorrer todas las builds legales por etapa sin
confundir "tres ramas por técnica" con un producto cartesiano inválido.

Reglas:
- tres técnicas por raíz: unitarget, defensiva, AOE;
- cada técnica tiene Tramo I/II/III;
- un nodo cuesta 1 punto;
- un Tramo superior requiere cualquier elección del Tramo anterior en ESA técnica;
- no exige seguir la misma familia entre tramos;
- los puntos pueden guardarse;
- LII total2/max T1, LIII total4/max T2, LIV total6/max T3.
"""
from __future__ import annotations

from dataclasses import dataclass
from itertools import product
from typing import Iterator

STAGES = {
    "LianQi_I":  {"max_tramo": 0, "points": 0},
    "LianQi_II": {"max_tramo": 1, "points": 2},
    "LianQi_III":{"max_tramo": 2, "points": 4},
    "LianQi_IV": {"max_tramo": 3, "points": 6},
}

TECHNIQUE_TREES = {
    "fuego": {
        "palma_ardiente": [
            ["Ascua Adherente", "Palma Compacta", "Respiración de Brasa"],
            ["Brasa Devoradora", "Corazón del Horno", "Circulación Incandescente"],
            ["Combustión Persistente", "Golpe Incandescente", "Flujo Constante"],
        ],
        "cuerpo_horno": [
            ["Cámara Sellada", "Horno Latente", "Respiración Mesurada"],
            ["Crisol de Nueve Sellos", "Corazón Reavivado", "Circuito del Horno"],
            ["Muro de Calor", "Calor Acumulado", "Horno Continuo"],
        ],
        "circulo_cien_ascuas": [
            ["Lluvia de Ascuas", "Anillo Incandescente", "Respiración de las Cien Ascuas"],
            ["Mar de Brasas", "Corona Ardiente", "Flujo Circular"],
            ["Brasas Persistentes", "Estallido Circular", "Círculo Estable"],
        ],
    },
    "metal": {
        "destello_plata": [
            ["Filo Abierto", "Corte Preciso", "Flujo de Plata"],
            ["Punta de Acero", "Golpe Certero", "Circulación Ligera"],
            ["Corte Profundo", "Destello Certero", "Ritmo de Plata"],
        ],
        "armadura_plata": [
            ["Placas Gruesas", "Acero Flexible", "Reserva de Plata"],
            ["Núcleo Reforzado", "Temple Reactivo", "Segunda Capa"],
            ["Acero Cerrado", "Temple Perfecto", "Armadura Laminada"],
        ],
        "lluvia_filos": [
            ["Filos Dentados", "Barrido Cerrado", "Paso Ligero"],
            ["Ruptura Profunda", "Tormenta de Acero", "Ritmo de Filos"],
            ["Defensa Quebrada", "Círculo de Acero", "Flujo Continuo"],
        ],
    },
    "agua": {
        "latigazo_marea": [
            ["Corriente Firme", "Golpe de Corriente", "Flujo Continuo"],
            ["Marea Envolvente", "Rompiente", "Circulación Serena"],
            ["Dominio de la Corriente", "Golpe de Marea", "Corriente Constante"],
        ],
        "espejo_luna": [
            ["Marea Profunda", "Agua Renovada", "Circulación Serena"],
            ["Marea Alta", "Corriente de Retorno", "Flujo Ligero"],
            ["Mar Interior", "Marea Eterna", "Corriente Ininterrumpida"],
        ],
        "marea_ocho_orillas": [
            ["Corriente Turbia", "Oleada Fuerte", "Flujo Amplio"],
            ["Marea Inestable", "Rompiente Abierta", "Circulación Extendida"],
            ["Mar Revuelto", "Marea Creciente", "Curso Inagotable"],
        ],
    },
    "tierra": {
        "golpe_montana": [
            ["Paso Pesado", "Golpe Macizo", "Base Firme"],
            ["Carga de Piedra", "Impacto Profundo", "Postura Inamovible"],
            ["Anclaje de Montaña", "Golpe de Cumbre", "Raíz Inamovible"],
        ],
        "piel_cobre": [
            ["Corteza Endurecida", "Centro Firme", "Tierra Persistente"],
            ["Estratos Compactos", "Raíz Profunda", "Suelo que Sostiene"],
            ["Cuerpo de Roca", "Inamovible", "Montaña Persistente"],
        ],
        "temblor_montana": [
            ["Suelo Quebrado", "Golpe Sísmico", "Resonancia"],
            ["Hundimiento", "Réplica", "Eco de la Falla"],
            ["Terreno Hundido", "Sacudida Mayor", "Falla Resonante"],
        ],
    },
    "viento": {
        "lanza_nubes": [
            ["Ojo del Vendaval", "Punta de Tormenta", "Respiración del Cielo"],
            ["Horizonte Claro", "Nube Partida", "Corriente Continua"],
            ["Mirada del Cielo Vacío", "Lanza que Abre el Cielo", "Aliento sin Interrupción"],
        ],
        "paso_nube": [
            ["Nube Velada", "Estela Vacía", "Respiración Ligera"],
            ["Cuerpo de Nube", "Huella del Cielo", "Circulación del Vendaval"],
            ["Nube Inalcanzable", "Paso sin Sombra", "Aliento de las Nubes"],
        ],
        "tijera_vendaval": [
            ["Ojo de la Tormenta", "Alas Cortantes", "Corriente Ordenada"],
            ["Cielo Turbio", "Vendaval Gemelo", "Cauce del Aire"],
            ["Tormenta Ciega", "Cizalla del Cielo", "Corriente Perfecta"],
        ],
    },
}

@dataclass(frozen=True)
class TechniquePath:
    technique_id: str
    choices: tuple[int, ...]  # 0..2 por tramo comprado

    @property
    def points(self) -> int:
        return len(self.choices)

    @property
    def code(self) -> str:
        if not self.choices:
            return "BASE"
        return "".join(str(x + 1) for x in self.choices)


@dataclass(frozen=True)
class SkillBuild:
    root: str
    stage: str
    paths: tuple[TechniquePath, ...]

    @property
    def points_spent(self) -> int:
        return sum(x.points for x in self.paths)

    @property
    def signature(self) -> str:
        return "|".join(f"{x.technique_id}:{x.code}" for x in self.paths)


def technique_paths(technique_id: str, max_tramo: int) -> list[TechniquePath]:
    out=[TechniquePath(technique_id, ())]
    for depth in range(1, max_tramo + 1):
        for choices in product(range(3), repeat=depth):
            out.append(TechniquePath(technique_id, tuple(choices)))
    return out


def enumerate_skill_builds(root: str, stage: str) -> Iterator[SkillBuild]:
    cfg=STAGES[stage]
    techs=list(TECHNIQUE_TREES[root])
    pools=[technique_paths(t, cfg["max_tramo"]) for t in techs]
    for combo in product(*pools):
        spent=sum(x.points for x in combo)
        if spent <= cfg["points"]:
            yield SkillBuild(root=root, stage=stage, paths=tuple(combo))


def skill_build_count(root: str, stage: str) -> int:
    return sum(1 for _ in enumerate_skill_builds(root, stage))


def all_root_build_count(stage: str) -> int:
    return sum(skill_build_count(root, stage) for root in TECHNIQUE_TREES)


def node_names(build: SkillBuild) -> dict[str, list[str]]:
    tree=TECHNIQUE_TREES[build.root]
    out={}
    for path in build.paths:
        names=[]
        for tramo_idx, choice_idx in enumerate(path.choices):
            names.append(tree[path.technique_id][tramo_idx][choice_idx])
        out[path.technique_id]=names
    return out


if __name__ == "__main__":
    for stage in STAGES:
        per_root={root:skill_build_count(root, stage) for root in TECHNIQUE_TREES}
        print(stage, per_root, "all_roots=", sum(per_root.values()))
