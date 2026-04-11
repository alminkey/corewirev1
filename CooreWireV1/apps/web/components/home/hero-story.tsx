type HeroStoryProps = {
  story: {
    slug: string;
    headline: string;
    dek: string;
    status: string;
    confidence: string;
    source_count: number;
  };
};

const heroImage =
  "https://images.unsplash.com/photo-1505664194779-8beaceb93744?auto=format&fit=crop&w=1600&q=80";

export function HeroStory({ story }: HeroStoryProps) {
  return (
    <section className="cw-lead-stage">
      <a className="cw-lead-frame" href={`/articles/${story.slug}`}>
        <div className="cw-lead-media" style={{ backgroundImage: `url(${heroImage})` }} />
        <div className="cw-lead-content">
          <div className="cw-lead-copy">
            <p className="cw-kicker">Lead Analysis</p>
            <h1>{story.headline}</h1>
            <p className="cw-summary">{story.dek}</p>
          </div>
          <div className="cw-lead-actions">
            <div className="cw-meta">
              <span>Sources: {story.source_count}</span>
              <span>Confidence: {story.confidence}</span>
              <span>Status: {story.status}</span>
            </div>
            <div className="cw-lead-buttons">
              <span className="cw-hero-cta">Read full report</span>
              <span className="cw-hero-cta cw-hero-cta--ghost">Open issue brief</span>
            </div>
          </div>
        </div>
      </a>
    </section>
  );
}
