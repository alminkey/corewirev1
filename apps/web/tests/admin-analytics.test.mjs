import test from "node:test";
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { resolve } from "node:path";

test("renders analytics dashboard sections for throughput queue confidence and cost", () => {
  const pageSource = readFileSync(resolve("app/admin/page.tsx"), "utf8");
  const dashboardSource = readFileSync(
    resolve("components/admin/analytics-dashboard.tsx"),
    "utf8",
  );

  assert.match(pageSource, /AnalyticsDashboard/);
  assert.match(dashboardSource, /Article Throughput/i);
  assert.match(dashboardSource, /Queue Status/i);
  assert.match(dashboardSource, /Confidence Distribution/i);
  assert.match(dashboardSource, /Cost Summary/i);
});
