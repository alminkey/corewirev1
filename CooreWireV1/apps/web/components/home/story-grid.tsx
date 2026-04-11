type StoryGridProps = {
  stories: Array<{
    slug: string;
    headline: string;
    dek: string;
  }>;
};

const storyImages = [
  "https://images.unsplash.com/photo-1497366754035-f200968a6e72?auto=format&fit=crop&w=900&q=80",
  "https://images.unsplash.com/photo-1517048676732-d65bc937f952?auto=format&fit=crop&w=900&q=80",
  "https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?auto=format&fit=crop&w=900&q=80",
  "https://images.unsplash.com/photo-1520607162513-77705c0f0d4a?auto=format&fit=crop&w=900&q=80",
];

export function StoryGrid({ stories }: StoryGridProps) {
  return (
    <section className="cw-card-grid cw-card-grid--public">
      {stories.map((story, index) => (
        <article className="cw-panel cw-card cw-card--light" key={story.slug}>
          <a className="cw-card-link" href={`/articles/${story.slug}`}>
            <div
              className="cw-story-card-media"
              style={{ backgroundImage: `url(${storyImages[index % storyImages.length]})` }}
            />
            <div className="cw-card-body">
              <p className="cw-kicker">Story {index + 1}</p>
              <h3>{story.headline}</h3>
              <p>{story.dek}</p>
            </div>
          </a>
        </article>
      ))}
    </section>
  );
}
