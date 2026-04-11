export function PublicHeader() {
  return (
    <header className="cw-public-header cw-minimal-topbar">
      <div className="cw-public-meta">
        <span>Friday, Apr 11, 2026</span>
        <span>Global dispatch edition</span>
      </div>
      <div className="cw-public-bar">
        <div className="cw-brand-cluster">
          <a className="cw-public-logo" href="/">
            CoreWire
          </a>
          <p className="cw-public-tagline">Global analysis, staged with intent.</p>
        </div>
        <div className="cw-primary-nav">
          <div className="cw-signal-chip">Signal edition</div>
          <nav className="cw-public-nav" aria-label="Primary">
            <a href="/">Front Page</a>
            <a href="/">World</a>
            <a href="/">Security</a>
            <a href="/">Economy</a>
            <a href="/newsletter">Newsletter</a>
            <a href="/admin">Admin</a>
          </nav>
        </div>
      </div>
    </header>
  );
}
