type AnalysisSectionProps = {
  blocks: string[];
};

export function AnalysisSection({ blocks }: AnalysisSectionProps) {
  return (
    <section className="cw-panel">
      <div className="cw-panel-header">
        <span>Analysis</span>
        <span>Interpretation</span>
      </div>
      <div className="cw-article-section">
        {blocks.map((block) => (
          <p className="cw-analysis-block" key={block}>
            {block}
          </p>
        ))}
      </div>
    </section>
  );
}
