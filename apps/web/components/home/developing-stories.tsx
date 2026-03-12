type DevelopingStoriesProps = {
  stories: Array<{
    slug: string;
    headline: string;
    dek: string;
  }>;
};

export function DevelopingStories({ stories }: DevelopingStoriesProps) {
  return (
    <section className="cw-panel">
      <div className="cw-panel-header">
        <span>Developing Stories</span>
        <span>Low Confidence</span>
      </div>
      <div className="cw-developing-list">
        {stories.map((story) => (
          <article className="cw-developing-item" key={story.slug}>
            <h3>{story.headline}</h3>
            <p>{story.dek}</p>
          </article>
        ))}
      </div>
    </section>
  );
}
