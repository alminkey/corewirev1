from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))

from core.validation.citations import validate_article


def test_article_validation_fails_when_fact_block_has_no_citation():
    draft = {
        "fact_blocks": [
            {
                "text": "CoreWire launched the pipeline on Tuesday.",
                "citations": [],
            }
        ]
    }

    validation = validate_article(draft)

    assert validation["valid"] is False
