type IntelligenceRailProps = {
  entries: string[];
};

export function IntelligenceRail({ entries }: IntelligenceRailProps) {
  return (
    <aside className="cw-rail">
      <section className="cw-panel">
        <div className="cw-panel-header">
          <span>Latest Intelligence Log</span>
          <span>Live</span>
        </div>
        <div className="cw-rail-list">
          {entries.map((entry) => (
            <article className="cw-rail-item" key={entry}>
              <h3>{entry}</h3>
              <p>Source-linked update stream</p>
            </article>
          ))}
        </div>
      </section>
      <section className="cw-panel cw-status">
        <div className="cw-panel-header">
          <span>Network Status</span>
          <span>Stable</span>
        </div>
        <dl>
          <div>
            <dt>Node connection</dt>
            <dd>Stable</dd>
          </div>
          <div>
            <dt>CPU load</dt>
            <dd>12.4%</dd>
          </div>
        </dl>
      </section>
    </aside>
  );
}
