import { AnalysisSection } from "../../../components/article/analysis-section";
import { ArticleHeader } from "../../../components/article/article-header";
import { DisagreementSection } from "../../../components/article/disagreement-section";
import { FactsSection } from "../../../components/article/facts-section";
import { SourcesSection } from "../../../components/article/sources-section";

const article = {
  headline: "CoreWire separates reporting from analysis on every article page.",
  dek: "Facts, analysis, disagreements, and sources stay visually distinct in the reading experience.",
  status: "Published",
  confidence: "High",
  sourceCount: 6,
  updatedAt: "March 11, 2026",
  facts: [
    {
      text: "CoreWire article pages expose a dedicated facts block at the top of the story.",
      citations: ["Reuters", "AP"],
    },
    {
      text: "Developing stories are excluded from homepage lead placement by the publish gate.",
      citations: ["Internal policy", "Source model"],
    },
  ],
  analysis: [
    "Analysis is framed separately so interpretation never appears as raw fact.",
    "The layout favors trust signals over generic content density.",
  ],
  disagreements: [
    "Some sources emphasize market impact, while others focus on policy implications.",
  ],
  sources: [
    "Reuters",
    "Associated Press",
    "Financial Times",
    "Bloomberg",
  ],
};

export default function ArticlePage() {
  return (
    <main className="cw-shell">
      <div className="cw-overlay" />
      <article className="cw-article">
        <ArticleHeader article={article} />
        <FactsSection blocks={article.facts} />
        <AnalysisSection blocks={article.analysis} />
        <DisagreementSection items={article.disagreements} />
        <SourcesSection citations={article.sources} />
      </article>
    </main>
  );
}
