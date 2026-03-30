type IntelligenceRailProps = {
  entries: Array<{
    slug: string;
    headline: string;
    dek: string;
  }>;
};

export function IntelligenceRail({ entries }: IntelligenceRailProps) {
  return (
    <aside className="cw-rail cw-rail--light">
      <section className="cw-panel cw-panel--light">
        <div className="cw-panel-header">
          <span>Latest Dispatch</span>
          <span>Live</span>
        </div>
        <div className="cw-rail-list">
          {entries.map((entry) => (
            <article className="cw-rail-item cw-rail-item--light" key={entry.slug}>
              <a className="cw-rail-link" href={`/articles/${entry.slug}`}>
                <h3>{entry.headline}</h3>
                <p>{entry.dek}</p>
              </a>
            </article>
          ))}
        </div>
      </section>
      <section className="cw-panel cw-status cw-panel--light">
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
