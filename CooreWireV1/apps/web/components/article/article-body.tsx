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
    <section className="cw-article-reading-shell">
      <div className="cw-body-copy">
        {paragraphs.map((paragraph, index) => (
          <p className="cw-article-body-paragraph" key={`article-body-${index}`}>
            {paragraph}
          </p>
        ))}
      </div>
    </section>
  );
}
