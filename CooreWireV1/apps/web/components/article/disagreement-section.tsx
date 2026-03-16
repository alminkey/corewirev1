type DisagreementSectionProps = {
  items: string[];
};

export function DisagreementSection({ items }: DisagreementSectionProps) {
  return (
    <section className="cw-panel">
      <div className="cw-panel-header">
        <span>Where Sources Disagree</span>
        <span>Differences</span>
      </div>
      <div className="cw-article-section">
        {items.map((item) => (
          <p className="cw-disagreement-block" key={item}>
            {item}
          </p>
        ))}
      </div>
    </section>
  );
}
