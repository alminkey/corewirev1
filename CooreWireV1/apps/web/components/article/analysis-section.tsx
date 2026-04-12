type AnalysisSectionProps = {
  blocks: string[];
};

export function AnalysisSection({ blocks }: AnalysisSectionProps) {
  return (
    <section className="cw-support-zone">
      <div className="cw-panel-header">
        <span>Analysis</span>
        <span>Interpretation</span>
      </div>
      <div className="cw-article-section">
        {blocks.map((block, index) => (
          <p className="cw-analysis-block" key={`analysis-${index}`}>
            {block}
          </p>
        ))}
      </div>
    </section>
  );
}
