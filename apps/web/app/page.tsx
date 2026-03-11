import { DevelopingStories } from "../components/home/developing-stories";
import { HeroStory } from "../components/home/hero-story";
import { IntelligenceRail } from "../components/home/intelligence-rail";
import { StoryGrid } from "../components/home/story-grid";

export default function HomePage() {
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
          <HeroStory />
          <StoryGrid />
          <DevelopingStories />
        </div>
        <IntelligenceRail />
      </section>
    </main>
  );
}
