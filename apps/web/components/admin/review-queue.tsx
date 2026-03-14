type QueueItem = {
  id: string;
  headline: string;
};

type ReviewQueueProps = {
  pendingDrafts: QueueItem[];
  lowConfidence: QueueItem[];
  flaggedItems: QueueItem[];
};

export function ReviewQueue({
  pendingDrafts,
  lowConfidence,
  flaggedItems,
}: ReviewQueueProps) {
  return (
    <section className="admin-shell__grid">
      <article className="admin-shell__panel">
        <h2>Pending Drafts</h2>
        <p>{pendingDrafts[0]?.headline ?? "No pending drafts"}</p>
      </article>
      <article className="admin-shell__panel">
        <h2>Low-confidence Stories</h2>
        <p>{lowConfidence[0]?.headline ?? "No low-confidence stories"}</p>
      </article>
      <article className="admin-shell__panel">
        <h2>Flagged Items</h2>
        <p>{flaggedItems[0]?.headline ?? "No flagged items"}</p>
      </article>
    </section>
  );
}
