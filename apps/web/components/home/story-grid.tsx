const stories = [
  {
    signal: "Signal Alpha",
    headline: "Policy shift widens pressure on AI infrastructure operators.",
    summary: "Cross-source comparison highlights where operators agree and where incentives diverge.",
  },
  {
    signal: "Signal Beta",
    headline: "Sovereign compute spending accelerates across regional clusters.",
    summary: "Data from multiple outlets suggests infrastructure buildouts are becoming strategic policy.",
  },
  {
    signal: "Signal Gamma",
    headline: "Markets reprice frontier model costs after new deployment benchmarks.",
    summary: "CoreWire analysis distinguishes reported cost facts from the why-this-matters layer.",
  },
];

export function StoryGrid() {
  return (
    <section className="cw-card-grid">
      {stories.map((story) => (
        <article className="cw-panel cw-card" key={story.signal}>
          <div className="cw-panel-header">
            <span>{story.signal}</span>
            <span>Analysis</span>
          </div>
          <div className="cw-card-body">
            <h3>{story.headline}</h3>
            <p>{story.summary}</p>
          </div>
        </article>
      ))}
    </section>
  );
}
