import { NewsletterSignupCard } from "../../components/monetization/newsletter-signup-card";

export default function NewsletterPage() {
  return (
    <main className="cw-shell">
      <div className="cw-overlay" />
      <section className="cw-article">
        <div className="cw-panel">
          <div className="cw-panel-header">
            <span>Newsletter</span>
            <span>CoreWire Briefing</span>
          </div>
          <div className="cw-article-section">
            <h1>Newsletter</h1>
            <p>
              Subscribe to the weekly premium briefing for AI, tech, and business coverage,
              including flagship stories, developing stories, and sponsor-supported editions.
            </p>
          </div>
        </div>
        <NewsletterSignupCard />
      </section>
    </main>
  );
}
