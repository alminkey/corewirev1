from typing import TypedDict


class AnalysisContract(TypedDict):
    thesis: str
    known_facts: list[str]
    actor_map: list[dict]
    obscured_layer: list[str]
    next_moves: list[str]
    unknowns: list[str]
    full_article: str


def build_analysis_contract(payload: dict) -> AnalysisContract:
    return {
        "thesis": payload.get("thesis", ""),
        "known_facts": payload.get("known_facts", []),
        "actor_map": payload.get("actor_map", []),
        "obscured_layer": payload.get("obscured_layer", []),
        "next_moves": payload.get("next_moves", []),
        "unknowns": payload.get("unknowns", []),
        "full_article": payload.get("full_article", ""),
    }
