from sqlalchemy import select
from sqlalchemy.orm import joinedload

from core.db.models.article import ArticleDraft, ArticleStatus, PublishedArticle


class ArticleRepository:
    def __init__(self, session):
        self.session = session

    def create_draft(self, payload: dict) -> ArticleDraft:
        draft = ArticleDraft(**payload)
        self.session.add(draft)
        self.session.flush()
        return draft

    def create_published_article(self, payload: dict) -> PublishedArticle:
        status = payload.get("status")
        article_payload = dict(payload)
        if isinstance(status, str):
            article_payload["status"] = ArticleStatus(status)

        article = PublishedArticle(**article_payload)
        self.session.add(article)
        self.session.flush()
        return article

    def list_published_articles(self) -> list[PublishedArticle]:
        statement = (
            select(PublishedArticle)
            .options(joinedload(PublishedArticle.draft))
            .order_by(PublishedArticle.homepage_eligible.desc(), PublishedArticle.published_at.desc())
        )
        return list(self.session.scalars(statement).all())

    def get_published_article_by_slug(self, slug: str) -> PublishedArticle | None:
        statement = (
            select(PublishedArticle)
            .options(joinedload(PublishedArticle.draft))
            .where(PublishedArticle.slug == slug)
        )
        return self.session.scalars(statement).first()
