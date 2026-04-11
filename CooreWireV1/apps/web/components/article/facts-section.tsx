type FactsSectionProps = {
  blocks: Array<{ text: string; citations: string[] }>;
};

export function FactsSection({ blocks }: FactsSectionProps) {
  return (
    <section className="cw-support-module">
      <div className="cw-panel-header">
        <span>What is Verified</span>
        <span>Facts</span>
      </div>
      <div className="cw-article-section">
        {blocks.map((block, index) => (
          <article
            className="cw-fact-block"
            key={`fact-${index}-${block.citations.join("|")}`}
          >
            <p>{block.text}</p>
            {block.citations.length > 0 ? (
              <small>Citations: {block.citations.join(", ")}</small>
            ) : null}
          </article>
        ))}
      </div>
    </section>
  );
}
