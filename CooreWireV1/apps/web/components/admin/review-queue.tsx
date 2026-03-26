type QueueItem = {
  id: string;
  headline: string;
  status?: string;
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
  const renderItem = (item: QueueItem | undefined, emptyLabel: string) => {
    if (!item) {
      return <p>{emptyLabel}</p>;
    }
    return (
      <p>
        <a href={`/admin/review/${item.id}`}>{item.headline}</a>
      </p>
    );
  };

  return (
    <section className="admin-shell__grid">
      <article className="admin-shell__panel">
        <h2>Pending Drafts</h2>
        {renderItem(pendingDrafts[0], "No pending drafts")}
      </article>
      <article className="admin-shell__panel">
        <h2>Low-confidence Stories</h2>
        {renderItem(lowConfidence[0], "No low-confidence stories")}
      </article>
      <article className="admin-shell__panel">
        <h2>Flagged Items</h2>
        {renderItem(flaggedItems[0], "No flagged items")}
      </article>
    </section>
  );
}
