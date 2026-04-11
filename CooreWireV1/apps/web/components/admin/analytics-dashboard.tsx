type AnalyticsDashboardProps = {
  articleThroughput: string;
  queueStatus: string;
  confidenceDistribution: string;
  costSummary: string;
};

export function AnalyticsDashboard({
  articleThroughput,
  queueStatus,
  confidenceDistribution,
  costSummary,
}: AnalyticsDashboardProps) {
  return (
    <section className="admin-shell__grid">
      <article className="admin-shell__panel cw-workspace-module">
        <h2>Article Throughput</h2>
        <p>{articleThroughput}</p>
      </article>
      <article className="admin-shell__panel cw-workspace-module">
        <h2>Queue Status</h2>
        <p>{queueStatus}</p>
      </article>
      <article className="admin-shell__panel cw-workspace-module">
        <h2>Confidence Distribution</h2>
        <p>{confidenceDistribution}</p>
      </article>
      <article className="admin-shell__panel cw-workspace-module">
        <h2>Cost Summary</h2>
        <p>{costSummary}</p>
      </article>
    </section>
  );
}
