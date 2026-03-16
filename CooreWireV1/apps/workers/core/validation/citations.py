def validate_article(draft: dict) -> dict:
    fact_blocks = draft.get("fact_blocks", [])
    is_valid = all(block.get("citations") for block in fact_blocks)
    return {"valid": is_valid}

