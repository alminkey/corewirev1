from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))

from core.articles.service import publish_article


def test_low_confidence_story_publishes_as_developing_story_and_not_homepage():
    article = publish_article(
        draft={"id": "draft-1", "slug": "corewire-story"},
        confidence={"level": "low", "homepage_eligible": False},
    )

    assert article["status"] == "developing_story"
    assert article["homepage_eligible"] is False
