type DevelopingStoriesProps = {
  stories: Array<{
    slug: string;
    headline: string;
    dek: string;
  }>;
};

export function DevelopingStories({ stories }: DevelopingStoriesProps) {
  return (
    <section className="cw-brief-ribbon">
      <div className="cw-feed-header">
        <p className="cw-kicker">Developing</p>
        <h2>What is still moving under the surface.</h2>
      </div>
      <div className="cw-brief-grid">
        {stories.map((story) => (
          <article className="cw-brief-card" key={story.slug}>
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
