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

export type ArticleDetail = StoryCard & {
  facts: ArticleFactBlock[];
  analysis: string[];
  disagreements: string[];
  sources: string[];
};
