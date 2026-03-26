export function NewsletterSignupCard() {
  return (
    <section className="cw-panel cw-newsletter-card">
      <div className="cw-panel-header">
        <span>Newsletter</span>
        <span>Weekly Briefing</span>
      </div>
      <div className="cw-article-section">
        <h3>Subscribe to the CoreWire briefing</h3>
        <p>
          Get the weekly AI, tech, and business briefing with source-backed reporting,
          sharper context, and early sponsor-supported releases.
        </p>
        <a className="cw-inline-link" href="/newsletter">
          Subscribe
        </a>
      </div>
    </section>
  );
}
