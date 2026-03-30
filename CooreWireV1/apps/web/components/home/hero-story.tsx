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

export function HeroStory({ story }: HeroStoryProps) {
  return (
    <section className="cw-panel cw-hero cw-hero--light">
      <a className="cw-hero-link" href={`/articles/${story.slug}`}>
        <div className="cw-panel-header">
          <span>Investigative report</span>
          <span>{story.status}</span>
        </div>
        <div className="cw-hero-body">
          <p className="cw-tag">Lead dispatch</p>
          <h2>{story.headline}</h2>
          <p className="cw-summary">{story.dek}</p>
          <div className="cw-meta">
            <span>Sources: {story.source_count}</span>
            <span>Confidence: {story.confidence}</span>
          </div>
          <span className="cw-hero-cta">Read full report</span>
        </div>
      </a>
    </section>
  );
}
