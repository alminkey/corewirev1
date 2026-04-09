import test from "node:test";
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { resolve } from "node:path";

test("renders programming controls for topics intervals and schedule windows", () => {
  const componentSource = readFileSync(
    resolve("components/admin/programming-controls.tsx"),
    "utf8",
  );

  assert.match(componentSource, /Programming Controls/i);
  assert.match(componentSource, /Topic Targets/i);
  assert.match(componentSource, /Generation Intervals/i);
  assert.match(componentSource, /Schedule Windows/i);
  assert.match(componentSource, /topics\.map/);
  assert.match(componentSource, /intervals\.map/);
  assert.match(componentSource, /scheduleWindows\.map/);
});
