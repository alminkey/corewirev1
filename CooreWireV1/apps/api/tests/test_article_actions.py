from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))

from core.compliance.actions import apply_article_action


def test_article_lifecycle_actions_update_status_and_record_audit_actor():
    approved = apply_article_action(
        article={"id": "draft-1", "status": "draft"},
        action="approve",
        actor="owner",
    )
    corrected = apply_article_action(
        article={"id": "article-1", "status": "published"},
        action="correct",
        actor="owner",
    )
    retracted = apply_article_action(
        article={"id": "article-2", "status": "published"},
        action="retract",
        actor="owner",
    )

    assert approved["status"] == "published"
    assert corrected["status"] == "corrected"
    assert retracted["status"] == "retracted"
    assert approved["audit"]["actor"] == "owner"
    assert corrected["audit"]["action"] == "correct"


def test_article_lifecycle_actions_preserve_existing_article_metadata():
    article = {
        "id": "draft-2",
        "status": "draft",
        "headline": "Manual owner story",
        "slug": "manual-owner-story",
    }

    approved = apply_article_action(
        article=article,
        action="approve",
        actor="owner",
    )

    assert approved["headline"] == "Manual owner story"
    assert approved["slug"] == "manual-owner-story"
