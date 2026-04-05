export type StoryCard = {
  slug: string;
  headline: string;
  status: string;
  confidence: string;
  source_count: number;
  updated_at: string;
  dek: string;
};

export type HomepagePayload = {
  lead_story: StoryCard;
  top_stories: StoryCard[];
  developing_stories: StoryCard[];
};

export type ArticleFactBlock = {
  text: string;
  citations: string[];
};

export type ArticleSource = {
  label: string;
  publisher: string | null;
  title: string | null;
  url: string | null;
  role: string;
};

export type ArticleDetail = StoryCard & {
  full_article: string;
  facts: ArticleFactBlock[];
  analysis: string[];
  disagreements: string[];
  sources: ArticleSource[];
};

export type ReviewDetail = {
  id: string;
  headline: string;
  dek: string;
  status: string;
  confidence: string;
  reasons: string[];
  doctrine: {
    passed: boolean;
    violations: string[];
  };
  decision_summary: string;
  recommendation: {
    action: "approve" | "reject" | "request_rerun";
    label: string;
    reason: string;
  };
  source_quality: {
    source_count: number;
    unique_publishers: number;
    authority: string;
    blockers: string[];
  };
  draft: {
    headline: string;
    dek: string;
    narrative: string;
    facts: Array<{ text?: string; label?: string; content?: string }>;
    analysis: Array<{ text?: string; label?: string; content?: string }>;
    sources: ArticleSource[];
    editorial_flags: Array<{ severity?: string; message?: string }>;
  };
};

export type AdminOverview = {
  publish_mode: string;
  system_health: string;
  review_queue_count: number;
};

export type AutonomySettings = {
  mode: "manual" | "hybrid" | "autonomous";
  allowed_modes: string[];
  homepage_auto_publish: boolean;
  developing_story_auto_publish: boolean;
  pause_ingest: boolean;
  pause_publish: boolean;
};

export type ReviewQueuePayload = {
  pending_drafts: Array<{ id: string; headline: string; status?: string }>;
  low_confidence: Array<{ id: string; headline: string; status?: string }>;
  flagged_items: Array<{ id: string; headline: string; status?: string }>;
};

export type ReviewDecisionResult = {
  id: string;
  status: string;
  action: "approve" | "reject" | "request_rerun";
};
