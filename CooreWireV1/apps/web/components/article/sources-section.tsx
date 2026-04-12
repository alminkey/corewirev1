import type { ArticleSource } from "../../lib/types";

type SourcesSectionProps = {
  citations: ArticleSource[];
};

export function SourcesSection({ citations }: SourcesSectionProps) {
  return (
    <section className="cw-support-zone cw-source-module">
      <div className="cw-panel-header">
        <span>Sources</span>
        <span>Outbound Links</span>
      </div>
      <div className="cw-article-section">
        <ul className="cw-source-list">
          {citations.map((citation) => (
            <li key={`${citation.label}-${citation.url ?? "local"}`}>
              <a href={citation.url ?? "#"} target="_blank" rel="noreferrer">
                {citation.label}
              </a>
              {citation.title ? ` - ${citation.title}` : ""}
            </li>
          ))}
        </ul>
      </div>
    </section>
  );
}
