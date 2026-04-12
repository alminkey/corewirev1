export function PublicHeader() {
  return (
    <header className="cw-public-header">
      <div className="cw-zdf-topbar">
        <div className="cw-zdf-topbar__meta">
          <span>Saturday, Apr 12, 2026</span>
          <span>Global Dispatch Edition</span>
        </div>
        <div className="cw-zdf-topbar__actions">
          <a href="/newsletter">Newsletter</a>
          <a href="/">Video</a>
          <a href="/admin">Admin</a>
        </div>
      </div>
      <div className="cw-zdf-nav">
        <div className="cw-zdf-nav__brand">
          <a className="cw-public-logo" href="/">
            CoreWire
          </a>
          <p>Global analysis for a world under pressure.</p>
        </div>
        <nav className="cw-public-nav" aria-label="Primary">
          <a href="/">Front Page</a>
          <a href="/">World</a>
          <a href="/">Security</a>
          <a href="/">Economy</a>
          <a href="/">Analysis</a>
        </nav>
      </div>
    </header>
  );
}
