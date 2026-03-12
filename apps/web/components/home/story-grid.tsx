type StoryGridProps = {
  stories: Array<{
    slug: string;
    headline: string;
    dek: string;
  }>;
};

export function StoryGrid({ stories }: StoryGridProps) {
  return (
    <section className="cw-card-grid">
      {stories.map((story, index) => (
        <article className="cw-panel cw-card" key={story.slug}>
          <div className="cw-panel-header">
            <span>Signal {index + 1}</span>
            <span>Analysis</span>
          </div>
          <div className="cw-card-body">
            <h3>{story.headline}</h3>
            <p>{story.dek}</p>
          </div>
        </article>
      ))}
    </section>
  );
}
