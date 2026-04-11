import type { ProgrammingSettings } from "../../lib/types";
import { applyProgrammingSettingsAction } from "../../app/admin/actions";

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
    <section
      id="programming-controls"
      className="admin-shell__panel admin-shell__panel--wide cw-panel"
    >
      <p className="admin-shell__eyebrow">Programming</p>
      <h2>Programming Controls</h2>
      <p>Define which topics the system should target, how often it should run, and when.</p>

      <form action={applyProgrammingSettingsAction} className="admin-editor">
        <input type="hidden" name="topic-count" value={topics.length} />
        <input type="hidden" name="interval-count" value={intervals.length} />
        <input type="hidden" name="window-count" value={scheduleWindows.length} />

        <div className="admin-shell__grid">
          <article className="admin-shell__panel">
            <h3>Topic Targets</h3>
            <ul className="story-list">
              {topics.map((topic, index) => (
                <li key={topic.name}>
                  <article>
                    <label>
                      Topic name
                      <input name={`topic-name-${index}`} defaultValue={topic.name} />
                    </label>
                    <label>
                      Enabled
                      <input
                        type="checkbox"
                        name={`topic-enabled-${index}`}
                        defaultChecked={topic.enabled}
                      />
                    </label>
                  </article>
                </li>
              ))}
            </ul>
          </article>
          <article className="admin-shell__panel">
            <h3>Generation Intervals</h3>
            <ul className="story-list">
              {intervals.map((interval, index) => (
                <li key={interval.label}>
                  <article>
                    <label>
                      Interval label
                      <input name={`interval-label-${index}`} defaultValue={interval.label} />
                    </label>
                    <label>
                      Minutes
                      <input
                        type="number"
                        min={1}
                        name={`interval-minutes-${index}`}
                        defaultValue={interval.minutes}
                      />
                    </label>
                    <label>
                      Enabled
                      <input
                        type="checkbox"
                        name={`interval-enabled-${index}`}
                        defaultChecked={interval.enabled}
                      />
                    </label>
                  </article>
                </li>
              ))}
            </ul>
          </article>
          <article className="admin-shell__panel">
            <h3>Schedule Windows</h3>
            <ul className="story-list">
              {scheduleWindows.map((window, index) => (
                <li key={window.label}>
                  <article>
                    <label>
                      Window label
                      <input name={`window-label-${index}`} defaultValue={window.label} />
                    </label>
                    <label>
                      Start hour
                      <input
                        type="number"
                        min={0}
                        max={23}
                        name={`window-start-${index}`}
                        defaultValue={window.start_hour}
                      />
                    </label>
                    <label>
                      End hour
                      <input
                        type="number"
                        min={0}
                        max={23}
                        name={`window-end-${index}`}
                        defaultValue={window.end_hour}
                      />
                    </label>
                    <label>
                      Timezone
                      <input
                        name={`window-timezone-${index}`}
                        defaultValue={window.timezone}
                      />
                    </label>
                    <label>
                      Enabled
                      <input
                        type="checkbox"
                        name={`window-enabled-${index}`}
                        defaultChecked={window.enabled}
                      />
                    </label>
                  </article>
                </li>
              ))}
            </ul>
          </article>
        </div>

        <div className="admin-editor__actions">
          <button type="submit">Apply Changes</button>
        </div>
      </form>
    </section>
  );
}
