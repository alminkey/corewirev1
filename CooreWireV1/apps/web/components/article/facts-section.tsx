type FactsSectionProps = {
  blocks: Array<{ text: string; citations: string[] }>;
};

export function FactsSection({ blocks }: FactsSectionProps) {
  return (
    <section className="cw-panel">
      <div className="cw-panel-header">
        <span>What is Verified</span>
        <span>Facts</span>
      </div>
      <div className="cw-article-section">
        {blocks.map((block) => (
          <article className="cw-fact-block" key={block.text}>
            <p>{block.text}</p>
            <small>Citations: {block.citations.join(", ")}</small>
          </article>
        ))}
      </div>
    </section>
  );
}
