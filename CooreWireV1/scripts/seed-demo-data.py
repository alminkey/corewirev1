from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "apps" / "workers"))

from core.jobs.pipeline import run_pipeline


def seed_demo_data() -> dict[str, int]:
    published_result = run_pipeline(
        "source-item-high",
        document={
            "id": "doc-high-1",
            "body_text": "CoreWire launched the pipeline on Tuesday.",
            "source_id": "source-1",
            "slug": "corewire-launched-the-pipeline",
        },
        related_documents=[
            {
                "id": "doc-high-2",
                "body_text": "CoreWire launched the pipeline on Tuesday.",
                "source_id": "source-2",
            }
        ],
    )
    developing_result = run_pipeline(
        "source-item-low",
        document={
            "id": "doc-low-1",
            "body_text": "CoreWire is still verifying the rollout details.",
            "source_id": "source-3",
            "slug": "corewire-verifying-the-rollout-details",
        },
        related_documents=[],
    )

    seeded_articles = [published_result, developing_result]

    return {
        "published_articles": len(seeded_articles),
        "homepage_articles": sum(
            1 for article in seeded_articles if article["homepage_eligible"]
        ),
        "developing_articles": sum(
            1 for article in seeded_articles if article["status"] == "developing_story"
        ),
    }


if __name__ == "__main__":
    print(seed_demo_data())
