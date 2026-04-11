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
    <main className="cw-shell cw-shell--admin cw-shell--light cw-app-shell cw-surface">
      <div className="cw-overlay" />
      <div className="cw-admin-layout">
        <aside className="cw-admin-sidebar">
          <a className="cw-admin-brand" href="#overview">
            CoreWire
          </a>
          <p className="cw-admin-sidebar__label">Owner Workspace</p>
          <nav className="cw-admin-sidebar__nav" aria-label="Admin sections">
            <a href="#overview">Overview</a>
            <a href="#review">Review Queue</a>
            <a href="#drafts">Drafts</a>
            <a href="#published">Published</a>
            <a href="#programming">Programming</a>
            <a href="#analytics">Analytics</a>
          </nav>
        </aside>

        <div className="cw-admin-main">
          <section className="cw-admin-utility">
            <div className="cw-admin-utility__item">
              <span>Health</span>
              <strong>{systemHealth}</strong>
            </div>
            <div className="cw-admin-utility__item">
              <span>Mode</span>
              <strong>{publishMode}</strong>
            </div>
            <div className="cw-admin-utility__item">
              <span>Review Queue</span>
              <strong>{reviewQueueCount || overview.queue?.review || overview.review_queue_count}</strong>
            </div>
          </section>

          <div className="cw-admin-workspace">
            <AdminShell
              publishMode={publishMode}
              systemHealth={systemHealth}
              reviewQueueCount={reviewQueueCount || overview.queue?.review || overview.review_queue_count}
            />

            <section id="review">
              <ReviewQueue
                pendingDrafts={reviewQueue.pending_drafts}
                lowConfidence={reviewQueue.low_confidence}
                flaggedItems={reviewQueue.flagged_items}
              />
            </section>

            <ArticleManager
              drafts={adminContent.drafts}
              published={publishedArticles}
              selectedDraft={selectedDraft}
            />

            <div className="cw-admin-section-grid">
              <section>
                <AutonomyControls
                  mode={autonomySettings.mode}
                  homepageAutoPublish={autonomySettings.homepage_auto_publish}
                  developingStoryAutoPublish={autonomySettings.developing_story_auto_publish}
                  pauseIngest={autonomySettings.pause_ingest}
                  pausePublish={autonomySettings.pause_publish}
                />
              </section>
              <section id="programming">
                <ProgrammingControls
                  topics={programming.topics}
                  intervals={programming.intervals}
                  scheduleWindows={programming.schedule_windows}
                />
              </section>
            </div>

            <section id="analytics">
              <AnalyticsDashboard
                articleThroughput={`${publishedArticles.length} published stories in the live feed`}
                queueStatus={`${reviewQueue.pending_drafts.length} pending drafts, ${reviewQueue.low_confidence.length} low-confidence, ${reviewQueue.flagged_items.length} flagged`}
                confidenceDistribution={`${publishedArticles.filter((story) => story.confidence === "high").length} high-confidence published`}
                costSummary={`Mode ${publishMode}, health ${systemHealth}`}
              />
            </section>

            <ArticleActions />
          </div>
        </div>
      </div>
    </main>
  );
}
