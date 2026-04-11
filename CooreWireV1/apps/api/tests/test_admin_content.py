from pathlib import Path
import json
import sys
import uuid

from fastapi.testclient import TestClient

sys.path.append(str(Path(__file__).resolve().parents[1]))

from app import app
from core.db.base import Base
from core.db.session import build_engine


def test_owner_can_list_create_and_update_manual_story_drafts(monkeypatch):
    database_path = Path(__file__).resolve().parents[3] / f"test-admin-content-{uuid.uuid4().hex}.db"
    database_url = f"sqlite+pysqlite:///{database_path}"
    monkeypatch.setenv("COREWIRE_DATABASE_URL", database_url)

    engine = build_engine(database_url)
    Base.metadata.create_all(engine)

    try:
        client = TestClient(app)
        headers = {"x-owner-token": "corewire-owner-token"}

        initial_response = client.get("/api/admin/content", headers=headers)
        assert initial_response.status_code == 200
        assert initial_response.json() == {"drafts": [], "published": []}

        create_response = client.post(
            "/api/admin/content/drafts",
            headers=headers,
            json={
                "headline": "Manual owner story",
                "dek": "Owner-created draft",
                "body": "A manual article body.",
                "slug": "manual-owner-story",
                "tags": ["ai", "policy"],
            },
        )

        assert create_response.status_code == 200
        created = create_response.json()
        assert created["headline"] == "Manual owner story"
        assert created["status"] == "draft"
        assert created["slug"] == "manual-owner-story"
        assert created["tags"] == ["ai", "policy"]

        update_response = client.patch(
            f"/api/admin/content/drafts/{created['id']}",
            headers=headers,
            json={
                "headline": "Updated owner story",
                "dek": "Updated owner draft",
                "body": "An updated article body.",
                "tags": ["markets"],
            },
        )

        assert update_response.status_code == 200
        updated = update_response.json()
        assert updated["headline"] == "Updated owner story"
        assert updated["dek"] == "Updated owner draft"
        assert updated["body"] == "An updated article body."
        assert updated["tags"] == ["markets"]

        listing_response = client.get("/api/admin/content", headers=headers)
        assert listing_response.status_code == 200
        listing = listing_response.json()
        assert listing["drafts"][0]["headline"] == "Updated owner story"
        assert listing["drafts"][0]["slug"] == "manual-owner-story"
        assert listing["published"] == []
    finally:
        engine.dispose()
        if database_path.exists():
            database_path.unlink()


def test_owner_can_fetch_one_manual_draft_in_editor_shape(monkeypatch):
    database_path = Path(__file__).resolve().parents[3] / f"test-admin-content-editor-{uuid.uuid4().hex}.db"
    database_url = f"sqlite+pysqlite:///{database_path}"
    monkeypatch.setenv("COREWIRE_DATABASE_URL", database_url)

    engine = build_engine(database_url)
    Base.metadata.create_all(engine)

    try:
        client = TestClient(app)
        headers = {"x-owner-token": "corewire-owner-token"}

        create_response = client.post(
            "/api/admin/content/drafts",
            headers=headers,
            json={
                "headline": "Editor-ready draft",
                "dek": "Editor dek",
                "body": "Editor body",
                "slug": "editor-ready-draft",
                "tags": ["draft", "editor"],
            },
        )

        assert create_response.status_code == 200
        created = create_response.json()

        detail_response = client.get(
            f"/api/admin/content/drafts/{created['id']}",
            headers=headers,
        )

        assert detail_response.status_code == 200
        detail = detail_response.json()
        assert detail == {
            "id": created["id"],
            "headline": "Editor-ready draft",
            "dek": "Editor dek",
            "body": "Editor body",
            "slug": "editor-ready-draft",
            "tags": ["draft", "editor"],
            "status": "draft",
        }
    finally:
        engine.dispose()
        if database_path.exists():
            database_path.unlink()


def test_owner_can_publish_manual_draft_from_editor(monkeypatch):
    database_path = Path(__file__).resolve().parents[3] / f"test-admin-content-publish-{uuid.uuid4().hex}.db"
    database_url = f"sqlite+pysqlite:///{database_path}"
    monkeypatch.setenv("COREWIRE_DATABASE_URL", database_url)

    engine = build_engine(database_url)
    Base.metadata.create_all(engine)

    try:
        client = TestClient(app)
        headers = {"x-owner-token": "corewire-owner-token"}

        create_response = client.post(
            "/api/admin/content/drafts",
            headers=headers,
            json={
                "headline": "Manual publish story",
                "dek": "Publish from owner editor",
                "body": "A manual publish body.",
                "slug": "manual-publish-story",
                "tags": ["manual", "publish"],
            },
        )

        assert create_response.status_code == 200
        created = create_response.json()

        publish_response = client.post(
            f"/api/admin/content/drafts/{created['id']}/publish",
            headers=headers,
        )

        assert publish_response.status_code == 200
        published = publish_response.json()
        assert published["id"] == created["id"]
        assert published["status"] == "published"
        assert published["slug"] == "manual-publish-story"

        content_response = client.get("/api/admin/content", headers=headers)
        assert content_response.status_code == 200
        content_payload = content_response.json()
        assert content_payload["drafts"][0]["status"] == "published"
        assert content_payload["published"][0]["headline"] == "Manual publish story"
        assert content_payload["published"][0]["slug"] == "manual-publish-story"
        assert content_payload["published"][0]["status"] == "published"
    finally:
        engine.dispose()
        if database_path.exists():
            database_path.unlink()


def test_owner_can_archive_manual_draft_from_editor(monkeypatch):
    database_path = Path(__file__).resolve().parents[3] / f"test-admin-content-archive-{uuid.uuid4().hex}.db"
    database_url = f"sqlite+pysqlite:///{database_path}"
    monkeypatch.setenv("COREWIRE_DATABASE_URL", database_url)

    engine = build_engine(database_url)
    Base.metadata.create_all(engine)

    try:
        client = TestClient(app)
        headers = {"x-owner-token": "corewire-owner-token"}

        create_response = client.post(
            "/api/admin/content/drafts",
            headers=headers,
            json={
                "headline": "Manual archive story",
                "dek": "Archive from owner editor",
                "body": "A manual archive body.",
                "slug": "manual-archive-story",
                "tags": ["manual", "archive"],
            },
        )

        assert create_response.status_code == 200
        created = create_response.json()

        publish_response = client.post(
            f"/api/admin/content/drafts/{created['id']}/publish",
            headers=headers,
        )

        assert publish_response.status_code == 200

        archive_response = client.post(
            f"/api/admin/content/drafts/{created['id']}/archive",
            headers=headers,
        )

        assert archive_response.status_code == 200
        archived = archive_response.json()
        assert archived["id"] == created["id"]
        assert archived["status"] == "archived"
        assert archived["slug"] == "manual-archive-story"

        content_response = client.get("/api/admin/content", headers=headers)
        assert content_response.status_code == 200
        content_payload = content_response.json()
        assert content_payload["drafts"][0]["status"] == "archived"
        assert content_payload["published"] == []
    finally:
        engine.dispose()
        if database_path.exists():
            database_path.unlink()
