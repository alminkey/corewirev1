type DevelopingStoriesProps = {
  stories: Array<{
    slug: string;
    headline: string;
    dek: string;
  }>;
};

export function DevelopingStories({ stories }: DevelopingStoriesProps) {
  return (
    <section className="cw-panel cw-panel--light cw-module-stack">
      <div className="cw-panel-header">
        <span>Developing Stories</span>
        <span>Low Confidence</span>
      </div>
      <div className="cw-developing-list">
        {stories.map((story) => (
          <article className="cw-developing-item cw-developing-item--light" key={story.slug}>
            <a className="cw-developing-link" href={`/articles/${story.slug}`}>
              <h3>{story.headline}</h3>
              <p>{story.dek}</p>
            </a>
          </article>
        ))}
      </div>
    </section>
  );
}
