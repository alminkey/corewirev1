import { AdminShell } from "../../components/admin/admin-shell";
import { AnalyticsDashboard } from "../../components/admin/analytics-dashboard";
import { ArticleActions } from "../../components/admin/article-actions";
import { ArticleManager } from "../../components/admin/article-manager";
import { AutonomyControls } from "../../components/admin/autonomy-controls";
import { ProgrammingControls } from "../../components/admin/programming-controls";
import { ReviewQueue } from "../../components/admin/review-queue";
import {
  getAdminContent,
  getAdminDraft,
  getAdminOverview,
  getAutonomySettings,
  getPublishedArticles,
  getProgrammingSettings,
  getReviewQueue,
} from "../../lib/api";

type AdminPageProps = {
  searchParams?: Promise<{
    draft?: string;
    editor?: string;
  }>;
};

export default async function AdminPage({ searchParams }: AdminPageProps) {
  const params = (await searchParams) ?? {};
  const requestedDraftId = params.draft;

  const [overview, autonomySettings, reviewQueue, publishedArticles, adminContent, programming] =
    await Promise.all([
      getAdminOverview(),
      getAutonomySettings(),
      getReviewQueue(),
      getPublishedArticles(),
      getAdminContent(),
      getProgrammingSettings(),
    ]);

  const selectedDraftId =
    params.editor === "new" ? "" : requestedDraftId || adminContent.drafts[0]?.id || "";
  const selectedDraft = selectedDraftId ? await getAdminDraft(selectedDraftId) : null;
  const reviewQueueCount =
    reviewQueue.pending_drafts.length +
    reviewQueue.low_confidence.length +
    reviewQueue.flagged_items.length;
  const publishMode = overview.autonomy?.mode ?? overview.publish_mode;
  const systemHealth = overview.health?.system ?? overview.system_health;
  return (
    <main className="cw-shell cw-shell--admin">
      <div className="cw-overlay" />
      <div className="cw-admin-stack">
        <AdminShell
          publishMode={publishMode}
          systemHealth={systemHealth}
          reviewQueueCount={reviewQueueCount || overview.queue?.review || overview.review_queue_count}
        />
        <AutonomyControls
          mode={autonomySettings.mode}
          homepageAutoPublish={autonomySettings.homepage_auto_publish}
          developingStoryAutoPublish={autonomySettings.developing_story_auto_publish}
          pauseIngest={autonomySettings.pause_ingest}
          pausePublish={autonomySettings.pause_publish}
        />
        <ReviewQueue
          pendingDrafts={reviewQueue.pending_drafts}
          lowConfidence={reviewQueue.low_confidence}
          flaggedItems={reviewQueue.flagged_items}
        />
        <ArticleManager
          drafts={adminContent.drafts}
          published={publishedArticles}
          selectedDraft={selectedDraft}
        />
        <ProgrammingControls
          topics={programming.topics}
          intervals={programming.intervals}
          scheduleWindows={programming.schedule_windows}
        />
        <AnalyticsDashboard
          articleThroughput={`${publishedArticles.length} published stories in the live feed`}
          queueStatus={`${reviewQueue.pending_drafts.length} pending drafts, ${reviewQueue.low_confidence.length} low-confidence, ${reviewQueue.flagged_items.length} flagged`}
          confidenceDistribution={`${publishedArticles.filter((story) => story.confidence === "high").length} high-confidence published`}
          costSummary={`Mode ${publishMode}, health ${systemHealth}`}
        />
        <section className="admin-shell__panel admin-shell__panel--wide cw-panel">
          <p className="admin-shell__eyebrow">System Overview</p>
          <h2>Published Articles</h2>
          {publishedArticles.length === 0 ? (
            <p>No published articles yet.</p>
          ) : (
            <ul className="story-list">
              {publishedArticles.map((story, index) => (
                <li key={`${story.slug ?? story.headline ?? index}-${index}`}>
                  <article>
                    <h3>
                      <a href={`/articles/${story.slug}`}>{story.headline}</a>
                    </h3>
                    <p>{story.dek}</p>
                    <dl>
                      <div>
                        <dt>Published Status</dt>
                        <dd>{story.status}</dd>
                      </div>
                      <div>
                        <dt>Confidence</dt>
                        <dd>{story.confidence}</dd>
                      </div>
                      <div>
                        <dt>Sources</dt>
                        <dd>{story.source_count}</dd>
                      </div>
                      <div>
                        <dt>Updated</dt>
                        <dd>{story.updated_at}</dd>
                      </div>
                    </dl>
                    <p>
                      <a href={`/articles/${story.slug}`}>Open article</a>
                    </p>
                  </article>
                </li>
              ))}
            </ul>
          )}
        </section>
        <ArticleActions />
      </div>
    </main>
  );
}
