type HeroStoryProps = {
  story: {
    headline: string;
    dek: string;
    status: string;
    confidence: string;
    source_count: number;
  };
};

export function HeroStory({ story }: HeroStoryProps) {
  return (
    <section className="cw-panel cw-hero">
      <div className="cw-panel-header">
        <span>Priority Alert Stream</span>
        <span>Signal Mesh // NW_001_SIG</span>
      </div>
      <div className="cw-hero-body">
        <p className="cw-tag">Signal Mesh: Hot lane</p>
        <h2>{story.headline}</h2>
        <p className="cw-summary">{story.dek}</p>
        <div className="cw-meta">
          <span>{story.status}</span>
          <span>Sources: {story.source_count}</span>
          <span>Confidence: {story.confidence}</span>
        </div>
      </div>
    </section>
  );
}
