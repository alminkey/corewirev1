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
    <section className="admin-shell cw-panel">
      <section className="admin-shell__hero">
        <div className="admin-shell__signal" aria-hidden="true">
          <span />
          <span />
          <span />
        </div>
        <div>
          <p className="admin-shell__eyebrow">Owner Control Plane</p>
          <h1>Signal Desk for the newsroom command center</h1>
          <p>
            Control autonomy, inspect operational health, and review publish decisions from one
            owner-only surface.
          </p>
        </div>
      </section>

      <section className="admin-shell__grid">
        <article className="admin-shell__panel">
          <h2>System Health</h2>
          <p>{systemHealth}</p>
        </article>
        <article className="admin-shell__panel">
          <h2>Publish Mode</h2>
          <p>{publishMode}</p>
        </article>
        <article className="admin-shell__panel">
          <h2>Review Queue</h2>
          <p>{reviewQueueCount} stories waiting</p>
        </article>
      </section>
    </section>
  );
}
