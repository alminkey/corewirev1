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
    <main className="cw-shell cw-shell--home cw-shell--light cw-editorial-shell cw-surface cw-public-dw-zdf">
      <PublicHeader />
      <section className="cw-homepage-shell">
        <section className="cw-homepage-top cw-dw-lead-cluster">
          <HeroStory story={homepage.lead_story} />
          <section className="cw-latest-desk">
            <IntelligenceRail entries={feedEntries} />
          </section>
        </section>
        <section className="cw-top-band">
          <StoryGrid stories={homepage.top_stories} />
        </section>
        <section className="cw-analysis-zone">
          <section className="cw-home-feature-media cw-feature-module">
            <div className="cw-feature-copy">
              <p className="cw-kicker">Analysis Zone</p>
              <h2>Context, briefings, and visual explainers built around the lead file.</h2>
              <p>
                A heavier homepage rhythm for the active desk: explainers, strategic maps, and
                short-form issue packaging that makes the front page feel current.
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
        <div className="cw-homepage-bottom">
          <section className="cw-current-feed">
            <DevelopingStories stories={homepage.developing_stories} />
          </section>
          <div className="cw-homepage-extras">
            <NewsletterSignupCard />
            <AdSlot placement="homepage-feed" />
            <AdSlot placement="homepage-lower" />
          </div>
        </div>
      </section>
    </main>
  );
}
