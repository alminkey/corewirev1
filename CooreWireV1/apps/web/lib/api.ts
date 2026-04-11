import type {
  AdminContentPayload,
  AdminDraftDetail,
  AdminOverview,
  ArticleDetail,
  AutonomySettings,
  HomepagePayload,
  ProgrammingSettings,
  ReviewDecisionResult,
  ReviewDetail,
  ReviewQueuePayload,
  StoryCard,
} from "./types";

const API_BASE_URL = process.env.COREWIRE_API_BASE_URL ?? "http://localhost:8000/api";

const homepageFallback: HomepagePayload = {
  lead_story: {
    slug: "corewire-launched-the-pipeline",
    headline: "CoreWire launched the integrated pipeline.",
    status: "published",
    confidence: "high",
    source_count: 2,
    updated_at: "2026-03-12T10:00:00Z",
    dek: "Two independent sources support the launch sequence.",
  },
  top_stories: [
    {
      slug: "corewire-seo-hardening-underway",
      headline: "CoreWire continues SEO hardening work.",
      status: "published",
      confidence: "medium",
      source_count: 2,
      updated_at: "2026-03-12T11:00:00Z",
      dek: "Search integrity and metadata work moved into integration scope.",
    },
  ],
  developing_stories: [
    {
      slug: "corewire-verifying-the-rollout-details",
      headline: "CoreWire is still verifying rollout details.",
      status: "developing_story",
      confidence: "low",
      source_count: 1,
      updated_at: "2026-03-12T12:00:00Z",
      dek: "The story remains visible off homepage lead placement while corroboration continues.",
    },
  ],
};

const articleFallback: Record<string, ArticleDetail> = {
  "corewire-launched-the-pipeline": {
    ...homepageFallback.lead_story,
    full_article:
      "Two supporting source documents confirm the pipeline launch. The successful orchestration path reduces the gap between skeleton code and a runnable runtime.",
    facts: [
      {
        text: "Two supporting source documents confirm the pipeline launch.",
        citations: ["Source 1", "Source 2"],
      },
    ],
    analysis: [
      "The successful orchestration path reduces the gap between skeleton code and a runnable runtime.",
    ],
    disagreements: [
      "Sources agree on the launch but differ on how complete the rollout is.",
    ],
    sources: [
      {
        label: "Source 1",
        publisher: "Source 1",
        title: null,
        url: null,
        role: "source",
      },
      {
        label: "Source 2",
        publisher: "Source 2",
        title: null,
        url: null,
        role: "source",
      },
    ],
  },
};

const reviewDetailFallback: ReviewDetail = {
  id: "draft-1",
  headline: "Flagship draft awaiting owner review",
  dek: "A source-backed draft is waiting for a final owner decision.",
  status: "review_required",
  confidence: "medium",
  reasons: ["insufficient_source_authority"],
  draft: {
    headline: "Flagship draft awaiting owner review",
    dek: "A source-backed draft is waiting for a final owner decision.",
    narrative:
      "The review detail page gives the owner one place to inspect narrative, facts, sources, and editorial flags before deciding what to do next.",
    facts: [{ text: "The draft did not auto-publish because the source mix still needs owner judgment." }],
    analysis: [{ text: "This page is optimized for review and action, not inline editing." }],
    sources: [
      {
        label: "Reuters",
        publisher: "Reuters",
        title: "Enterprise AI report",
        url: "https://example.com/reuters",
        role: "article",
      },
    ],
    editorial_flags: [{ severity: "medium", message: "Needs owner authority review." }],
  },
};

const adminOverviewFallback: AdminOverview = {
  health: {
    system: "stable",
  },
  autonomy: {
    mode: "hybrid",
    allowed_modes: ["manual", "hybrid", "autonomous"],
    homepage_auto_publish: true,
    developing_story_auto_publish: true,
    pause_ingest: false,
    pause_publish: false,
  },
  pause_state: {
    ingest: false,
    publish: false,
  },
  queue: {
    review: 3,
    pending_drafts: 0,
    low_confidence: 1,
    flagged_items: 0,
  },
  published: {
    total: 2,
  },
  recent_activity: [],
  publish_mode: "hybrid",
  system_health: "stable",
  review_queue_count: 3,
};

const autonomySettingsFallback: AutonomySettings = {
  mode: "hybrid",
  allowed_modes: ["manual", "hybrid", "autonomous"],
  homepage_auto_publish: true,
  developing_story_auto_publish: true,
  pause_ingest: false,
  pause_publish: false,
};

const reviewQueueFallback: ReviewQueuePayload = {
  pending_drafts: [],
  low_confidence: [],
  flagged_items: [],
};

const adminContentFallback: AdminContentPayload = {
  drafts: [],
  published: [],
};

const programmingSettingsFallback: ProgrammingSettings = {
  topics: [
    { name: "ai", enabled: true },
    { name: "business", enabled: true },
  ],
  intervals: [{ label: "daily-cycle", minutes: 360, enabled: true }],
  schedule_windows: [
    {
      label: "default-daytime",
      start_hour: 6,
      end_hour: 22,
      timezone: "Europe/Zagreb",
      enabled: true,
    },
  ],
};

async function fetchJson<T>(path: string, fallback: T): Promise<T> {
  try {
    const response = await fetch(`${API_BASE_URL}${path}`, {
      cache: "no-store",
    });

    if (!response.ok) {
      return fallback;
    }

    return (await response.json()) as T;
  } catch {
    return fallback;
  }
}

async function fetchJsonWithHeaders<T>(
  path: string,
  fallback: T,
  headers: Record<string, string>,
): Promise<T> {
  try {
    const response = await fetch(`${API_BASE_URL}${path}`, {
      cache: "no-store",
      headers,
    });

    if (!response.ok) {
      return fallback;
    }

    return (await response.json()) as T;
  } catch {
    return fallback;
  }
}

async function postJsonWithHeaders<T>(
  path: string,
  body: object,
  headers: Record<string, string>,
): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    method: "POST",
    cache: "no-store",
    headers: {
      "content-type": "application/json",
      ...headers,
    },
    body: JSON.stringify(body),
  });

  if (!response.ok) {
    throw new Error(`Request failed: ${response.status}`);
  }

  return (await response.json()) as T;
}

async function patchJsonWithHeaders<T>(
  path: string,
  body: object,
  headers: Record<string, string>,
): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    method: "PATCH",
    cache: "no-store",
    headers: {
      "content-type": "application/json",
      ...headers,
    },
    body: JSON.stringify(body),
  });

  if (!response.ok) {
    throw new Error(`Request failed: ${response.status}`);
  }

  return (await response.json()) as T;
}

async function putJsonWithHeaders<T>(
  path: string,
  body: object,
  headers: Record<string, string>,
): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    method: "PUT",
    cache: "no-store",
    headers: {
      "content-type": "application/json",
      ...headers,
    },
    body: JSON.stringify(body),
  });

  if (!response.ok) {
    throw new Error(`Request failed: ${response.status}`);
  }

  return (await response.json()) as T;
}

export async function getHomepage(): Promise<HomepagePayload> {
  return fetchJson("/articles", homepageFallback);
}

export async function getArticleBySlug(slug: string): Promise<ArticleDetail> {
  return fetchJson(`/articles/${slug}`, articleFallback[slug] ?? articleFallback["corewire-launched-the-pipeline"]);
}

function ownerHeaders(): Record<string, string> {
  const ownerToken = process.env.COREWIRE_OWNER_TOKEN ?? "corewire-owner-token";
  return {
    "x-owner-token": ownerToken,
  };
}

export async function getAdminOverview(): Promise<AdminOverview> {
  return fetchJsonWithHeaders("/admin/overview", adminOverviewFallback, ownerHeaders());
}

export async function getAutonomySettings(): Promise<AutonomySettings> {
  return fetchJsonWithHeaders(
    "/admin/settings/autonomy",
    autonomySettingsFallback,
    ownerHeaders(),
  );
}

export async function getReviewQueue(): Promise<ReviewQueuePayload> {
  return fetchJsonWithHeaders("/admin/review-queue", reviewQueueFallback, ownerHeaders());
}

export async function getPublishedArticles(): Promise<StoryCard[]> {
  return fetchJsonWithHeaders("/admin/published", [], ownerHeaders());
}

export async function getAdminContent(): Promise<AdminContentPayload> {
  return fetchJsonWithHeaders("/admin/content", adminContentFallback, ownerHeaders());
}

export async function getAdminDraft(id: string): Promise<AdminDraftDetail | null> {
  return fetchJsonWithHeaders(`/admin/content/drafts/${id}`, null, ownerHeaders());
}

export async function getProgrammingSettings(): Promise<ProgrammingSettings> {
  return fetchJsonWithHeaders(
    "/admin/settings/programming",
    programmingSettingsFallback,
    ownerHeaders(),
  );
}

export async function updateProgrammingSettings(
  payload: ProgrammingSettings,
): Promise<ProgrammingSettings> {
  return putJsonWithHeaders(
    "/admin/settings/programming",
    payload,
    ownerHeaders(),
  );
}

export async function getReviewDetail(id: string): Promise<ReviewDetail> {
  return fetchJsonWithHeaders(
    `/admin/review-queue/${id}`,
    {
      ...reviewDetailFallback,
      id,
    },
    ownerHeaders(),
  );
}

export async function createAdminDraft(payload: {
  headline: string;
  dek: string;
  body: string;
  slug: string;
  tags: string[];
}): Promise<AdminDraftDetail> {
  return postJsonWithHeaders("/admin/content/drafts", payload, ownerHeaders());
}

export async function updateAdminDraft(
  id: string,
  payload: {
    headline: string;
    dek: string;
    body: string;
    slug: string;
    tags: string[];
  },
): Promise<AdminDraftDetail> {
  return patchJsonWithHeaders(`/admin/content/drafts/${id}`, payload, ownerHeaders());
}

export async function publishAdminDraft(id: string): Promise<AdminDraftDetail> {
  return postJsonWithHeaders(`/admin/content/drafts/${id}/publish`, {}, ownerHeaders());
}

export async function archiveAdminDraft(id: string): Promise<AdminDraftDetail> {
  return postJsonWithHeaders(`/admin/content/drafts/${id}/archive`, {}, ownerHeaders());
}

export async function postReviewDecision(
  id: string,
  action: "approve" | "reject" | "request_rerun",
): Promise<ReviewDecisionResult> {
  return postJsonWithHeaders(
    `/admin/review-queue/${id}/decision`,
    { action },
    ownerHeaders(),
  );
}
