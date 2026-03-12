import type { ArticleDetail, HomepagePayload } from "./types";

const SITE_URL = process.env.COREWIRE_SITE_URL ?? "http://localhost:3000";

export function buildCanonical(path: string): string {
  return `${SITE_URL}${path}`;
}

export function generateHomepageMetadata(homepage: HomepagePayload) {
  return {
    title: "CoreWire Command Center",
    description: homepage.lead_story.dek,
    alternates: {
      canonical: buildCanonical("/"),
    },
    openGraph: {
      title: homepage.lead_story.headline,
      description: homepage.lead_story.dek,
      url: buildCanonical("/"),
      type: "website",
    },
  };
}

export function buildArticleMetadata(article: ArticleDetail) {
  const isDeveloping = article.status === "developing_story";

  return {
    title: article.headline,
    description: article.dek,
    alternates: {
      canonical: buildCanonical(`/articles/${article.slug}`),
    },
    robots: isDeveloping
      ? {
          index: false,
          follow: false,
        }
      : {
          index: true,
          follow: true,
        },
    openGraph: {
      title: article.headline,
      description: article.dek,
      url: buildCanonical(`/articles/${article.slug}`),
      type: "article",
    },
  };
}

export function buildSitemapEntries(homepage: HomepagePayload) {
  const allStories = [
    homepage.lead_story,
    ...homepage.top_stories,
    ...homepage.developing_stories,
  ];

  return [
    {
      url: buildCanonical("/"),
      lastModified: new Date().toISOString(),
    },
    ...allStories.map((story) => ({
      url: buildCanonical(`/articles/${story.slug}`),
      lastModified: story.updated_at,
    })),
  ];
}
