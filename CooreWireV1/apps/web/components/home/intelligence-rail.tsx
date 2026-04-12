type IntelligenceRailProps = {
  entries: Array<{
    slug: string;
    headline: string;
    dek: string;
  }>;
};

export function IntelligenceRail({ entries }: IntelligenceRailProps) {
  return (
    <aside className="cw-latest-desk">
      <div className="cw-latest-desk__header">
        <p className="cw-kicker">Latest Desk</p>
        <h2>Live signals shaping this edition.</h2>
      </div>
      <div className="cw-latest-stack">
        {entries.map((entry, index) => (
          <article className="cw-latest-card" key={`${entry.slug}-${index}`}>
            <a className="cw-rail-link" href={`/articles/${entry.slug}`}>
              <p className="cw-kicker">Live {index + 1}</p>
              <h3>{entry.headline}</h3>
              <p>{entry.dek}</p>
            </a>
          </article>
        ))}
      </div>
    </aside>
  );
}
