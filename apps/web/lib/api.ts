import type { ArticleDetail, HomepagePayload } from "./types";

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
    sources: ["Source 1", "Source 2"],
  },
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

export async function getHomepage(): Promise<HomepagePayload> {
  return fetchJson("/articles", homepageFallback);
}

export async function getArticleBySlug(slug: string): Promise<ArticleDetail> {
  return fetchJson(`/articles/${slug}`, articleFallback[slug] ?? articleFallback["corewire-launched-the-pipeline"]);
}
