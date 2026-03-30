export function PublicHeader() {
  return (
    <header className="cw-public-header">
      <div className="cw-public-meta">
        <span>Sunday, Mar 30, 2026</span>
        <span>Signal edition</span>
      </div>
      <div className="cw-public-bar">
        <a className="cw-public-logo" href="/">
          CoreWire
        </a>
        <nav className="cw-public-nav" aria-label="Primary">
          <a href="/">Home</a>
          <a href="/newsletter">Newsletter</a>
          <a href="/advertise">Advertise</a>
          <a href="/admin">Admin</a>
        </nav>
      </div>
    </header>
  );
}
