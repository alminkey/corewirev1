import test from "node:test";
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { resolve } from "node:path";

test("renders autonomy mode controls and publish toggles", () => {
  const pageSource = readFileSync(resolve("app/admin/page.tsx"), "utf8");
  const controlsSource = readFileSync(
    resolve("components/admin/autonomy-controls.tsx"),
    "utf8",
  );

  assert.match(pageSource, /AutonomyControls/);
  assert.match(controlsSource, /Manual/i);
  assert.match(controlsSource, /Hybrid/i);
  assert.match(controlsSource, /Autonomous/i);
  assert.match(controlsSource, /Homepage Auto-publish/i);
  assert.match(controlsSource, /Pause Publish/i);
});
