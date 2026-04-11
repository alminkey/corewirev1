import type { AdminDraftDetail, AdminDraftSummary, StoryCard } from "../../lib/types";
import {
  archiveOwnerDraftAction,
  publishOwnerDraftAction,
  saveOwnerDraftAction,
} from "../../app/admin/actions";

type ArticleManagerProps = {
  drafts: AdminDraftSummary[];
  published: StoryCard[];
  selectedDraft: AdminDraftDetail | null;
};

const emptyDraft: AdminDraftDetail = {
  id: "",
  headline: "",
  dek: "",
  body: "",
  slug: "",
  tags: [],
  status: "draft",
};

export function ArticleManager({
  drafts,
  published,
  selectedDraft,
}: ArticleManagerProps) {
  const draft = selectedDraft ?? emptyDraft;
  const isExistingDraft = Boolean(draft.id);

  return (
    <section className="admin-shell__panel admin-shell__panel--wide cw-panel cw-workspace-module" id="drafts">
      <p className="admin-shell__eyebrow">Manual Story Controls</p>
      <h2>Article Manager</h2>
      <p>
        Work one draft at a time without leaving the admin workspace, while keeping inventory and
        publish visibility within the same panel.
      </p>

      <div className="cw-admin-workspace-grid">
        <div className="cw-admin-inventory-panel">
          <article className="admin-shell__panel cw-workspace-module">
            <div className="admin-shell__panel-header">
              <div>
                <h3>Manual Drafts</h3>
                <p>{drafts.length} drafts in owner editing flow</p>
              </div>
              <a href="/admin?editor=new">New Draft</a>
            </div>
            {drafts.length === 0 ? (
              <p>No manual drafts yet.</p>
            ) : (
              <ul className="story-list">
                {drafts.map((draftItem) => (
                  <li key={draftItem.id}>
                    <article>
                      <h4>
                        <a href={`/admin?draft=${draftItem.id}`}>{draftItem.headline}</a>
                      </h4>
                      <p>{draftItem.dek}</p>
                      <p>Status: {draftItem.status}</p>
                      <p>Slug: {draftItem.slug}</p>
                    </article>
                  </li>
                ))}
              </ul>
            )}
          </article>
          <article className="admin-shell__panel cw-workspace-module" id="published">
            <h3>Published Inventory</h3>
            <p>{published.length} articles currently live</p>
            {published.length === 0 ? (
              <p>No published inventory yet.</p>
            ) : (
              <ul className="story-list">
                {published.map((story, index) => (
                  <li key={`${story.slug ?? story.headline ?? index}-${index}`}>
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
        <article className="admin-shell__panel cw-admin-editor-panel cw-workspace-module cw-editor-surface">
          <h3>Editor Workspace</h3>
          <p>
            {isExistingDraft
              ? "Edit the selected draft and publish when ready."
              : "Create a new manual draft."}
          </p>
          <form action={saveOwnerDraftAction} className="admin-editor">
            <input type="hidden" name="id" value={draft.id} />
            <label>
              Headline
              <input name="headline" defaultValue={draft.headline} />
            </label>
            <label>
              Dek
              <input name="dek" defaultValue={draft.dek} />
            </label>
            <label>
              Slug
              <input name="slug" defaultValue={draft.slug} />
            </label>
            <label>
              Tags
              <input name="tags" defaultValue={draft.tags.join(", ")} />
            </label>
            <label>
              Body
              <textarea name="body" defaultValue={draft.body} rows={14} />
            </label>
            <div className="admin-editor__actions">
              <button type="submit">Save Draft</button>
              <button type="submit" formAction={publishOwnerDraftAction}>
                Publish
              </button>
              {isExistingDraft ? (
                <button type="submit" formAction={archiveOwnerDraftAction}>
                  Archive
                </button>
              ) : null}
            </div>
          </form>
        </article>
      </div>
    </section>
  );
}
