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
