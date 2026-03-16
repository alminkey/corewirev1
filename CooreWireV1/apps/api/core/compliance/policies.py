from fastapi import APIRouter


router = APIRouter(prefix="/compliance", tags=["compliance"])


@router.get("/policies")
def get_policy_metadata() -> dict:
    return {
        "ai_disclosure": {
            "slug": "ai-disclosure",
            "title": "AI Disclosure Policy",
        },
        "corrections": {
            "slug": "corrections",
            "title": "Corrections and Retractions Policy",
        },
    }
