from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))

from core.clustering.service import assign_story_clusters


def test_related_claims_join_same_story_cluster():
    claims = [
        {"claim_text": "CoreWire launched a new pipeline in Zagreb."},
        {"claim_text": "A new pipeline was launched in Zagreb by CoreWire."},
    ]

    clustered = assign_story_clusters(claims)

    assert clustered[0]["story_cluster_id"] == clustered[1]["story_cluster_id"]
