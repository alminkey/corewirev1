from core.analysis.service import analyze_story
from core.audit.service import record_pipeline_event
from core.claims.service import extract_claims
from core.clustering.service import assign_story_clusters
from core.confidence.service import score_confidence
from core.corroboration.service import match_evidence
from core.drafting.service import build_draft
from core.editorial.standards import validate_standards
from core.editorial.style import polish_draft
from core.validation.citations import validate_article


def run_pipeline(
    source_item_id: str,
    document: dict,
    related_documents: list[dict] | None = None,
) -> dict:
    related_documents = [document, *(related_documents or [])]

    claims = extract_claims(document)
    clustered_claims = assign_story_clusters(claims)

    evidence: list[dict] = []
    for claim in clustered_claims:
        document_matches = match_evidence(claim, related_documents)
        for related_document, document_match in zip(related_documents, document_matches):
            evidence.append(
                {
                    **document_match,
                    "source_id": related_document.get("source_id"),
                }
            )

    analysis = analyze_story({"claims": clustered_claims, "evidence": evidence})
    confidence = score_confidence({"evidence": evidence})
    draft = build_draft(analysis)
    draft = polish_draft(draft)
    draft["id"] = f"draft-{source_item_id}"
    draft["slug"] = document.get("slug", source_item_id)

    standards_validation = validate_standards(draft)
    validation = validate_article(draft)

    status = "invalid"
    homepage_eligible = False
    if validation["valid"] and standards_validation["valid"]:
        status = "published"
        homepage_eligible = True
        if confidence["level"] == "low":
            status = "developing_story"
            homepage_eligible = False

    audit_event = record_pipeline_event(
        run_type="pipeline",
        target_id=source_item_id,
        status=status,
        metadata={
            "claim_count": len(clustered_claims),
            "cluster_id": clustered_claims[0]["story_cluster_id"]
            if clustered_claims
            else None,
            "draft_id": draft["id"],
        },
    )

    return {
        "source_item_id": source_item_id,
        "status": status,
        "homepage_eligible": homepage_eligible,
        "confidence": confidence,
        "draft": draft,
        "audit_event": audit_event,
    }
