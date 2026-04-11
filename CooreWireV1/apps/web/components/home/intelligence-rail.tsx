type IntelligenceRailProps = {
  entries: Array<{
    slug: string;
    headline: string;
    dek: string;
  }>;
};

export function IntelligenceRail({ entries }: IntelligenceRailProps) {
  return (
    <aside className="cw-curated-feed">
      <div className="cw-feed-column">
        <div className="cw-feed-header">
          <p className="cw-kicker">Curated dispatch</p>
          <h2>Signals shaping the edition.</h2>
        </div>
        <div className="cw-feed-stack">
          {entries.map((entry, index) => (
            <article className="cw-feed-card" key={`${entry.slug}-${index}`}>
              <a className="cw-rail-link" href={`/articles/${entry.slug}`}>
                <p className="cw-kicker">Dispatch {index + 1}</p>
                <h3>{entry.headline}</h3>
                <p>{entry.dek}</p>
              </a>
            </article>
          ))}
        </div>
      </div>
    </aside>
  );
}
