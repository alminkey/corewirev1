import { AdminShell } from "../../components/admin/admin-shell";
import { AnalyticsDashboard } from "../../components/admin/analytics-dashboard";
import { ArticleActions } from "../../components/admin/article-actions";
import { AutonomyControls } from "../../components/admin/autonomy-controls";
import { ReviewQueue } from "../../components/admin/review-queue";


export default function AdminPage() {
  return (
    <>
      <AdminShell
        publishMode="Hybrid"
        systemHealth="Stable"
        reviewQueueCount={3}
      />
      <AutonomyControls
        mode="hybrid"
        homepageAutoPublish={true}
        developingStoryAutoPublish={true}
        pauseIngest={false}
        pausePublish={false}
      />
      <ReviewQueue
        pendingDrafts={[
          { id: "draft-1", headline: "Flagship draft awaiting owner review" },
        ]}
        lowConfidence={[
          {
            id: "story-1",
            headline: "Developing story with limited corroboration",
          },
        ]}
        flaggedItems={[
          { id: "flag-1", headline: "Story requires compliance review" },
        ]}
      />
      <AnalyticsDashboard
        articleThroughput="42 articles published this month"
        queueStatus="3 jobs pending, 0 failed"
        confidenceDistribution="High 60%, Medium 30%, Low 10%"
        costSummary="$182.50 spent this month"
      />
      <ArticleActions />
    </>
  );
}
