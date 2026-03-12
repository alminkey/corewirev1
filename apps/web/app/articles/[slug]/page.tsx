import { AnalysisSection } from "../../../components/article/analysis-section";
import { ArticleHeader } from "../../../components/article/article-header";
import { DisagreementSection } from "../../../components/article/disagreement-section";
import { FactsSection } from "../../../components/article/facts-section";
import { SourcesSection } from "../../../components/article/sources-section";
import { getArticleBySlug } from "../../../lib/api";

type ArticlePageProps = {
  params: Promise<{ slug: string }>;
};

export default async function ArticlePage({ params }: ArticlePageProps) {
  const { slug } = await params;
  const article = await getArticleBySlug(slug);

  return (
    <main className="cw-shell">
      <div className="cw-overlay" />
      <article className="cw-article">
        <ArticleHeader
          article={{
            headline: article.headline,
            dek: article.dek,
            status: article.status,
            confidence: article.confidence,
            sourceCount: article.source_count,
            updatedAt: article.updated_at,
          }}
        />
        <FactsSection blocks={article.facts} />
        <AnalysisSection blocks={article.analysis} />
        <DisagreementSection items={article.disagreements} />
        <SourcesSection citations={article.sources} />
      </article>
    </main>
  );
}
