type AdminShellProps = {
  publishMode: string;
  systemHealth: string;
  reviewQueueCount: number;
};

export function AdminShell({
  publishMode,
  systemHealth,
  reviewQueueCount,
}: AdminShellProps) {
  return (
    <section className="admin-shell cw-panel cw-admin-overview cw-workspace-module" id="overview">
      <section className="admin-shell__hero">
        <div className="admin-shell__signal" aria-hidden="true">
          <span />
          <span />
          <span />
        </div>
        <div>
          <div className="cw-signal-chip">Live system</div>
          <p className="admin-shell__eyebrow">Owner Workspace</p>
          <h1>CoreWire command center built for daily operation.</h1>
          <p>
            Review the newsroom, manage drafts, adjust programming, and keep the publish system
            under control from one owner-only surface.
          </p>
        </div>
      </section>

      <section className="admin-shell__grid cw-admin-stat-grid">
        <article className="admin-shell__panel cw-workspace-module">
          <h2>System Health</h2>
          <p>{systemHealth}</p>
        </article>
        <article className="admin-shell__panel cw-workspace-module">
          <h2>Publish Mode</h2>
          <p>{publishMode}</p>
        </article>
        <article className="admin-shell__panel cw-workspace-module">
          <h2>Review Queue</h2>
          <p>{reviewQueueCount} stories waiting</p>
        </article>
      </section>
    </section>
  );
}
