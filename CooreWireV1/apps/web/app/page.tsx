import { DevelopingStories } from "../components/home/developing-stories";
import { HeroStory } from "../components/home/hero-story";
import { IntelligenceRail } from "../components/home/intelligence-rail";
import { AdSlot } from "../components/monetization/ad-slot";
import { NewsletterSignupCard } from "../components/monetization/newsletter-signup-card";
import { StoryGrid } from "../components/home/story-grid";
import { PublicHeader } from "../components/public/public-header";
import { getHomepage } from "../lib/api";
import { generateHomepageMetadata } from "../lib/seo";

export async function generateMetadata() {
  const homepage = await getHomepage();
  return generateHomepageMetadata(homepage);
}

export default async function HomePage() {
  const homepage = await getHomepage();

  return (
    <main className="cw-shell cw-shell--home cw-shell--light cw-editorial-shell cw-surface">
      <PublicHeader />
      <section className="cw-grid cw-grid--public">
        <div className="cw-main">
          <HeroStory story={homepage.lead_story} />
          <StoryGrid stories={homepage.top_stories} />
          <section className="cw-home-feature-media cw-panel">
            <div className="cw-panel-header">
              <span>Video Brief</span>
              <span>Explainer</span>
            </div>
            <div className="cw-home-feature-media__frame">
              <iframe
                src="https://www.youtube-nocookie.com/embed/ysz5S6PUM-U?rel=0"
                title="CoreWire feature video"
                loading="lazy"
                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                referrerPolicy="strict-origin-when-cross-origin"
                allowFullScreen
              />
            </div>
          </section>
          <AdSlot placement="homepage-feed" />
          <NewsletterSignupCard />
          <DevelopingStories stories={homepage.developing_stories} />
          <AdSlot placement="homepage-lower" />
        </div>
        <IntelligenceRail
          entries={[
            homepage.lead_story,
            ...homepage.top_stories,
            ...homepage.developing_stories,
          ]}
        />
      </section>
    </main>
  );
}
