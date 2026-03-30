import { AnalysisSection } from "../../../components/article/analysis-section";
import { AdSlot } from "../../../components/monetization/ad-slot";
import { ArticleHeader } from "../../../components/article/article-header";
import { DisagreementSection } from "../../../components/article/disagreement-section";
import { FactsSection } from "../../../components/article/facts-section";
import { NewsletterSignupCard } from "../../../components/monetization/newsletter-signup-card";
import { PublicHeader } from "../../../components/public/public-header";
import { ArticleJsonLd } from "../../../components/seo/article-json-ld";
import { SourcesSection } from "../../../components/article/sources-section";
import { getArticleBySlug } from "../../../lib/api";
import { buildArticleMetadata } from "../../../lib/seo";

type ArticlePageProps = {
  params: Promise<{ slug: string }>;
};

export async function generateMetadata({ params }: ArticlePageProps) {
  const { slug } = await params;
  const article = await getArticleBySlug(slug);
  const noindex = article.status === "developing_story";
  const metadata_with_robots = {
    ...buildArticleMetadata(article),
    robots: noindex
      ? { index: false, follow: false }
      : { index: true, follow: true },
  };
  return metadata_with_robots;
}

export default async function ArticlePage({ params }: ArticlePageProps) {
  const { slug } = await params;
  const article = await getArticleBySlug(slug);

  return (
    <main className="cw-shell cw-article-shell cw-article-shell--light">
      <PublicHeader />
      <article className="cw-article cw-article--light">
        <ArticleJsonLd article={article} />
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
        <AdSlot placement="article-upper" />
        <FactsSection blocks={article.facts} />
        <AnalysisSection blocks={article.analysis} />
        <NewsletterSignupCard />
        <AdSlot placement="article-lower" />
        <DisagreementSection items={article.disagreements} />
        <SourcesSection citations={article.sources} />
      </article>
    </main>
  );
}
