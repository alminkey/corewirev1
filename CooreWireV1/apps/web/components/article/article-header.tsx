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
    <header className="cw-article-stage">
      <div className="cw-stage-copy">
        <div className="cw-signal-chip">Flagship</div>
        <p className="cw-kicker">Investigative report</p>
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
