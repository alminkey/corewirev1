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
    <header className="cw-panel cw-article-header cw-article-header--light cw-reading-header">
      <div className="cw-panel-header">
        <span>Investigative report</span>
        <span>{article.status}</span>
      </div>
      <div className="cw-article-header-body cw-article-header-intro">
        <div className="cw-signal-chip">Flagship</div>
        <p className="cw-kicker">CoreWire flagship analysis</p>
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
