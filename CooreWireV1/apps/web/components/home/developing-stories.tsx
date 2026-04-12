type DevelopingStoriesProps = {
  stories: Array<{
    slug: string;
    headline: string;
    dek: string;
  }>;
};

export function DevelopingStories({ stories }: DevelopingStoriesProps) {
  const firstBand = stories.slice(0, 2);
  const secondBand = stories.slice(2);

  return (
    <section className="cw-current-feed">
      <section className="cw-section-band">
        <div className="cw-feed-header">
          <p className="cw-kicker">World + Security</p>
          <h2>What moved beneath the lead while the main story took the top frame.</h2>
        </div>
        <div className="cw-brief-grid">
          {firstBand.map((story, index) => (
            <article className="cw-brief-card" key={`${story.slug}-${index}`}>
              <a className="cw-developing-link" href={`/articles/${story.slug}`}>
                <h3>{story.headline}</h3>
                <p>{story.dek}</p>
              </a>
            </article>
          ))}
        </div>
      </section>
      <section className="cw-section-band">
        <div className="cw-feed-header">
          <p className="cw-kicker">Current Feed</p>
          <h2>More reporting from the active desk.</h2>
        </div>
        <div className="cw-brief-grid">
          {secondBand.map((story, index) => (
            <article className="cw-brief-card" key={`${story.slug}-${index}`}>
              <a className="cw-developing-link" href={`/articles/${story.slug}`}>
                <h3>{story.headline}</h3>
                <p>{story.dek}</p>
              </a>
            </article>
          ))}
        </div>
      </section>
    </section>
  );
}
