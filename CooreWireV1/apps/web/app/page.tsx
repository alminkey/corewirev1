import { DevelopingStories } from "../components/home/developing-stories";
import { HeroStory } from "../components/home/hero-story";
import { IntelligenceRail } from "../components/home/intelligence-rail";
import { AdSlot } from "../components/monetization/ad-slot";
import { NewsletterSignupCard } from "../components/monetization/newsletter-signup-card";
import { StoryGrid } from "../components/home/story-grid";
import { getHomepage } from "../lib/api";
import { generateHomepageMetadata } from "../lib/seo";

export async function generateMetadata() {
  const homepage = await getHomepage();
  return generateHomepageMetadata(homepage);
}

export default async function HomePage() {
  const homepage = await getHomepage();

  return (
    <main className="cw-shell cw-shell--home">
      <div className="cw-overlay" />
      <header className="cw-topbar cw-panel">
        <div className="cw-brand-lockup">
          <span className="cw-signal-mark" aria-hidden="true">
            <span />
            <span />
            <span />
          </span>
          <div>
            <p className="cw-kicker">COREWIRE_OS</p>
            <h1>CoreWire Signal Desk</h1>
            <p className="cw-topbar-note">
              A live editorial wire for autonomous reporting, review, and signal-driven publishing.
            </p>
          </div>
        </div>
        <nav className="cw-nav">
          <span>// Signal Mesh</span>
          <span>// Wire Index</span>
          <span>// Review Queue</span>
        </nav>
      </header>

      <section className="cw-grid">
        <div className="cw-main">
          <HeroStory story={homepage.lead_story} />
          <StoryGrid stories={homepage.top_stories} />
          <AdSlot placement="homepage-feed" />
          <NewsletterSignupCard />
          <DevelopingStories stories={homepage.developing_stories} />
          <AdSlot placement="homepage-lower" />
        </div>
        <IntelligenceRail
          entries={[
            homepage.lead_story.headline,
            ...homepage.top_stories.map((story) => story.headline),
            ...homepage.developing_stories.map((story) => story.headline),
          ]}
        />
      </section>
    </main>
  );
}
