import test from "node:test";
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { resolve } from "node:path";

test("renders owner admin shell with control and review sections", () => {
  const pageSource = readFileSync(resolve("app/admin/page.tsx"), "utf8");
  const shellSource = readFileSync(resolve("components/admin/admin-shell.tsx"), "utf8");

  assert.match(pageSource, /AdminShell/);
  assert.match(pageSource, /ArticleManager/);
  assert.match(pageSource, /ProgrammingControls/);
  assert.match(pageSource, /getAdminContent/);
  assert.match(pageSource, /getProgrammingSettings/);
  assert.match(pageSource, /Published Articles/i);
  assert.match(pageSource, /System Overview/i);
  assert.match(pageSource, /Published Status/i);
  assert.match(pageSource, /Confidence/i);
  assert.match(pageSource, /Sources/i);
  assert.match(pageSource, /Updated/i);
  assert.match(pageSource, /Open article/i);
  assert.match(pageSource, /story\.status/);
  assert.match(pageSource, /story\.confidence/);
  assert.match(pageSource, /story\.source_count/);
  assert.match(pageSource, /story\.updated_at/);
  assert.match(pageSource, /href=\{`\/articles\/\$\{story\.slug\}`\}/);
  assert.match(shellSource, /Owner Control Plane/i);
  assert.match(shellSource, /Signal Desk/i);
  assert.match(shellSource, /admin-shell__signal/);
  assert.match(shellSource, /Review Queue/i);
  assert.match(shellSource, /System Health/i);
});
