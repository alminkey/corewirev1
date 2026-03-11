const developingStories = [
  "Funding round reports conflict across early source coverage.",
  "Emergency policy draft still lacks independent confirmation.",
];

export function DevelopingStories() {
  return (
    <section className="cw-panel">
      <div className="cw-panel-header">
        <span>Developing Stories</span>
        <span>Low Confidence</span>
      </div>
      <div className="cw-developing-list">
        {developingStories.map((story) => (
          <article className="cw-developing-item" key={story}>
            <h3>{story}</h3>
            <p>Visible on watchlist only until corroboration improves.</p>
          </article>
        ))}
      </div>
    </section>
  );
}
