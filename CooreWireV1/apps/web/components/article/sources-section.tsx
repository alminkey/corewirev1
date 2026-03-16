type SourcesSectionProps = {
  citations: string[];
};

export function SourcesSection({ citations }: SourcesSectionProps) {
  return (
    <section className="cw-panel">
      <div className="cw-panel-header">
        <span>Sources</span>
        <span>Outbound Links</span>
      </div>
      <div className="cw-article-section">
        <ul className="cw-source-list">
          {citations.map((citation) => (
            <li key={citation}>{citation}</li>
          ))}
        </ul>
      </div>
    </section>
  );
}
