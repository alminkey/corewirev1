type ArticleBodyProps = {
  fullArticle: string;
};

export function ArticleBody({ fullArticle }: ArticleBodyProps) {
  const paragraphs = fullArticle
    .split(/\n\n+/)
    .map((paragraph) => paragraph.trim())
    .filter(Boolean);

  if (paragraphs.length === 0) {
    return null;
  }

  return (
    <section className="cw-panel cw-panel--light cw-module-card cw-prose-shell">
      <div className="cw-panel-header">
        <span>Flagship Analysis</span>
        <span>Full Article</span>
      </div>
      <div className="cw-article-section cw-article-body cw-article-prose">
        {paragraphs.map((paragraph, index) => (
          <p className="cw-article-body-paragraph" key={`article-body-${index}`}>
            {paragraph}
          </p>
        ))}
      </div>
    </section>
  );
}
