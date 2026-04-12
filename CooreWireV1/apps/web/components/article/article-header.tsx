type ArticleHeaderProps = {
  article: {
    headline: string;
    dek: string;
    status: string;
    confidence: string;
    sourceCount: number;
    updatedAt: string;
  };
};

export function ArticleHeader({ article }: ArticleHeaderProps) {
  return (
    <header className="cw-article-hero-frame">
      <div className="cw-hero-copy">
        <p className="cw-kicker">Investigative report</p>
        <h1>{article.headline}</h1>
        <p className="article-dek">{article.dek}</p>
        <div className="cw-meta">
          <span>Sources: {article.sourceCount}</span>
          <span>Updated: {article.updatedAt}</span>
          <span>Confidence: {article.confidence}</span>
        </div>
      </div>
    </header>
  );
}
