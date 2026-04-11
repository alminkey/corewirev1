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
  const feedEntries = [
    homepage.lead_story,
    ...homepage.top_stories,
    ...homepage.developing_stories,
  ];

  return (
    <main className="cw-shell cw-shell--home cw-shell--light cw-editorial-shell cw-surface cw-public-luxury">
      <PublicHeader />
      <section className="cw-lead-stage">
        <HeroStory story={homepage.lead_story} />
      </section>
      <section className="cw-support-strip">
        <StoryGrid stories={homepage.top_stories} />
      </section>
      <section className="cw-feature-band">
        <section className="cw-home-feature-media cw-feature-module">
          <div className="cw-feature-copy">
            <p className="cw-kicker">Visual explainer</p>
            <h2>Watch the strategic map behind today&apos;s lead story.</h2>
            <p>
              A short-form briefing surface for timelines, routes, actors, and the stakes that sit
              behind the day&apos;s main analysis.
            </p>
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
      </section>
      <section className="cw-curated-feed">
        <div className="cw-main">
          <DevelopingStories stories={homepage.developing_stories} />
          <NewsletterSignupCard />
          <AdSlot placement="homepage-feed" />
          <AdSlot placement="homepage-lower" />
        </div>
        <IntelligenceRail entries={feedEntries} />
      </section>
    </main>
  );
}
