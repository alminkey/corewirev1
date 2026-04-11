import type { ProgrammingSettings } from "../../lib/types";

type ProgrammingControlsProps = {
  topics: ProgrammingSettings["topics"];
  intervals: ProgrammingSettings["intervals"];
  scheduleWindows: ProgrammingSettings["schedule_windows"];
};

export function ProgrammingControls({
  topics,
  intervals,
  scheduleWindows,
}: ProgrammingControlsProps) {
  return (
    <section className="admin-shell__panel admin-shell__panel--wide cw-panel">
      <p className="admin-shell__eyebrow">Programming</p>
      <h2>Programming Controls</h2>
      <p>Define which topics the system should target, how often it should run, and when.</p>

      <div className="admin-shell__grid">
        <article className="admin-shell__panel">
          <h3>Topic Targets</h3>
          <ul className="story-list">
            {topics.map((topic) => (
              <li key={topic.name}>
                <article>
                  <h4>{topic.name}</h4>
                  <p>{topic.enabled ? "Enabled" : "Disabled"}</p>
                </article>
              </li>
            ))}
          </ul>
        </article>
        <article className="admin-shell__panel">
          <h3>Generation Intervals</h3>
          <ul className="story-list">
            {intervals.map((interval) => (
              <li key={interval.label}>
                <article>
                  <h4>{interval.label}</h4>
                  <p>
                    Every {interval.minutes} minutes · {interval.enabled ? "Enabled" : "Disabled"}
                  </p>
                </article>
              </li>
            ))}
          </ul>
        </article>
        <article className="admin-shell__panel">
          <h3>Schedule Windows</h3>
          <ul className="story-list">
            {scheduleWindows.map((window) => (
              <li key={window.label}>
                <article>
                  <h4>{window.label}</h4>
                  <p>
                    {window.start_hour}:00-{window.end_hour}:00 · {window.timezone} ·{" "}
                    {window.enabled ? "Enabled" : "Disabled"}
                  </p>
                </article>
              </li>
            ))}
          </ul>
        </article>
      </div>
    </section>
  );
}
