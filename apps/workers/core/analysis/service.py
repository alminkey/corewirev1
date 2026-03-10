def analyze_story(evidence_bundle: dict) -> dict:
    claims = evidence_bundle.get("claims", [])
    verified_facts = [claim["claim_text"] for claim in claims if claim.get("claim_text")]

    why_summary = "Analysis: More source diversity is needed to explain impact."
    if verified_facts:
        why_summary = f"Analysis: {verified_facts[0]} may matter because it changes the story context."

    return {
        "verified_facts": verified_facts,
        "why_analysis": why_summary,
    }

