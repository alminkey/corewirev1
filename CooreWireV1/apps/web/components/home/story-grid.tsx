type StoryGridProps = {
  stories: Array<{
    slug: string;
    headline: string;
    dek: string;
  }>;
};

export function StoryGrid({ stories }: StoryGridProps) {
  return (
    <section className="cw-card-grid cw-card-grid--public">
      {stories.map((story, index) => (
        <article className="cw-panel cw-card cw-card--light" key={story.slug}>
          <a className="cw-card-link" href={`/articles/${story.slug}`}>
            <div className="cw-panel-header">
              <span>Story {index + 1}</span>
              <span>Open report</span>
            </div>
            <div className="cw-card-body">
              <h3>{story.headline}</h3>
              <p>{story.dek}</p>
            </div>
          </a>
        </article>
      ))}
    </section>
  );
}
