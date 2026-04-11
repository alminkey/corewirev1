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
    <section className="cw-reading-column cw-body-flow">
      <div className="cw-article-prose">
        {paragraphs.map((paragraph, index) => (
          <p className="cw-article-body-paragraph" key={`article-body-${index}`}>
            {paragraph}
          </p>
        ))}
      </div>
    </section>
  );
}
