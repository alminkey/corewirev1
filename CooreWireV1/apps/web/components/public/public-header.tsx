export function PublicHeader() {
  return (
    <header className="cw-public-header">
      <div className="cw-public-meta cw-top-signal-bar">
        <span>Friday, Apr 11, 2026</span>
        <span>Global dispatch edition</span>
      </div>
      <div className="cw-public-bar cw-public-header-bar">
        <a className="cw-public-logo" href="/">
          CoreWire
        </a>
        <div className="cw-platform-nav-cluster">
          <div className="cw-signal-chip">Signal edition</div>
          <nav className="cw-public-nav cw-public-section-nav" aria-label="Primary">
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
