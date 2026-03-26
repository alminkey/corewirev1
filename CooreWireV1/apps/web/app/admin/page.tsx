import { AdminShell } from "../../components/admin/admin-shell";
import { AnalyticsDashboard } from "../../components/admin/analytics-dashboard";
import { ArticleActions } from "../../components/admin/article-actions";
import { AutonomyControls } from "../../components/admin/autonomy-controls";
import { ReviewQueue } from "../../components/admin/review-queue";
import {
  getAdminOverview,
  getAutonomySettings,
  getPublishedArticles,
  getReviewQueue,
} from "../../lib/api";

export default async function AdminPage() {
  const [overview, autonomySettings, reviewQueue, publishedArticles] = await Promise.all([
    getAdminOverview(),
    getAutonomySettings(),
    getReviewQueue(),
    getPublishedArticles(),
  ]);
  const reviewQueueCount =
    reviewQueue.pending_drafts.length +
    reviewQueue.low_confidence.length +
    reviewQueue.flagged_items.length;
  return (
    <>
      <AdminShell
        publishMode={overview.publish_mode}
        systemHealth={overview.system_health}
        reviewQueueCount={reviewQueueCount || overview.review_queue_count}
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
      <AnalyticsDashboard
        articleThroughput={`${publishedArticles.length} published stories in the live feed`}
        queueStatus={`${reviewQueue.pending_drafts.length} pending drafts, ${reviewQueue.low_confidence.length} low-confidence, ${reviewQueue.flagged_items.length} flagged`}
        confidenceDistribution={`${publishedArticles.filter((story) => story.confidence === "high").length} high-confidence published`}
        costSummary={`Mode ${overview.publish_mode}, health ${overview.system_health}`}
      />
      <section className="admin-shell__panel">
        <p className="admin-shell__eyebrow">System Overview</p>
        <h2>Published Articles</h2>
        {publishedArticles.length === 0 ? (
          <p>No published articles yet.</p>
        ) : (
          <ul>
            {publishedArticles.map((story) => (
              <li key={story.slug}>
                <a href={`/articles/${story.slug}`}>{story.headline}</a>
              </li>
            ))}
          </ul>
        )}
      </section>
      <ArticleActions />
    </>
  );
}
