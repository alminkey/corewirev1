import type { AdminDraftSummary, StoryCard } from "../../lib/types";

type ArticleManagerProps = {
  drafts: AdminDraftSummary[];
  published: StoryCard[];
};

export function ArticleManager({ drafts, published }: ArticleManagerProps) {
  return (
    <section className="admin-shell__panel admin-shell__panel--wide cw-panel">
      <p className="admin-shell__eyebrow">Manual Story Controls</p>
      <h2>Article Manager</h2>
      <p>
        Track manual drafts alongside the published inventory so the owner can see what is still
        being prepared versus what is already live.
      </p>

      <div className="admin-shell__grid">
        <article className="admin-shell__panel">
          <h3>Manual Drafts</h3>
          <p>{drafts.length} drafts in owner editing flow</p>
          {drafts.length === 0 ? (
            <p>No manual drafts yet.</p>
          ) : (
            <ul className="story-list">
              {drafts.map((draft) => (
                <li key={draft.id}>
                  <article>
                    <h4>{draft.headline}</h4>
                    <p>{draft.dek}</p>
                    <p>Status: {draft.status}</p>
                    <p>Slug: {draft.slug}</p>
                  </article>
                </li>
              ))}
            </ul>
          )}
        </article>
        <article className="admin-shell__panel">
          <h3>Published Inventory</h3>
          <p>{published.length} articles currently live</p>
          {published.length === 0 ? (
            <p>No published inventory yet.</p>
          ) : (
            <ul className="story-list">
              {published.map((story) => (
                <li key={story.slug}>
                  <article>
                    <h4>{story.headline}</h4>
                    <p>{story.status}</p>
                  </article>
                </li>
              ))}
            </ul>
          )}
        </article>
      </div>
    </section>
  );
}
