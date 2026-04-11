type AutonomyControlsProps = {
  mode: "manual" | "hybrid" | "autonomous";
  homepageAutoPublish: boolean;
  developingStoryAutoPublish: boolean;
  pauseIngest: boolean;
  pausePublish: boolean;
};

export function AutonomyControls({
  mode,
  homepageAutoPublish,
  developingStoryAutoPublish,
  pauseIngest,
  pausePublish,
}: AutonomyControlsProps) {
  return (
    <section className="admin-shell__panel cw-workspace-module">
      <p className="admin-shell__eyebrow">Autonomy Controls</p>
      <h2>Publishing policy</h2>
      <ul>
        <li>Manual: {mode === "manual" ? "active" : "available"}</li>
        <li>Hybrid: {mode === "hybrid" ? "active" : "available"}</li>
        <li>Autonomous: {mode === "autonomous" ? "active" : "available"}</li>
      </ul>
      <dl>
        <div>
          <dt>Homepage Auto-publish</dt>
          <dd>{homepageAutoPublish ? "On" : "Off"}</dd>
        </div>
        <div>
          <dt>Developing Story Auto-publish</dt>
          <dd>{developingStoryAutoPublish ? "On" : "Off"}</dd>
        </div>
        <div>
          <dt>Pause Ingest</dt>
          <dd>{pauseIngest ? "On" : "Off"}</dd>
        </div>
        <div>
          <dt>Pause Publish</dt>
          <dd>{pausePublish ? "On" : "Off"}</dd>
        </div>
      </dl>
    </section>
  );
}
