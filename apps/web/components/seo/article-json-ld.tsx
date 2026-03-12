type ArticleJsonLdProps = {
  article: {
    slug: string;
    headline: string;
    dek: string;
    updated_at: string;
    status: string;
  };
};

export function ArticleJsonLd({ article }: ArticleJsonLdProps) {
  const payload = {
    "@context": "https://schema.org",
    "@type": "NewsArticle",
    headline: article.headline,
    description: article.dek,
    dateModified: article.updated_at,
    url: `/articles/${article.slug}`,
    articleSection: article.status,
  };

  return (
    <script
      type="application/ld+json"
      dangerouslySetInnerHTML={{ __html: JSON.stringify(payload) }}
    />
  );
}
