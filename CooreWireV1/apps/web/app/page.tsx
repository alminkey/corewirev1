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
    <main className="cw-shell">
      <div className="cw-overlay" />
      <header className="cw-topbar">
        <div>
          <p className="cw-kicker">COREWIRE_OS</p>
          <h1>Command Center</h1>
        </div>
        <nav className="cw-nav">
          <span>// Terminal</span>
          <span>// Database</span>
          <span>// Archive</span>
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
