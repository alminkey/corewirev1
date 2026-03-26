import test from "node:test";
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { resolve } from "node:path";

test("renders owner admin shell with control and review sections", () => {
  const pageSource = readFileSync(resolve("app/admin/page.tsx"), "utf8");
  const shellSource = readFileSync(resolve("components/admin/admin-shell.tsx"), "utf8");

  assert.match(pageSource, /AdminShell/);
  assert.match(pageSource, /Published Articles/i);
  assert.match(pageSource, /System Overview/i);
  assert.match(shellSource, /Owner Control Plane/i);
  assert.match(shellSource, /Review Queue/i);
  assert.match(shellSource, /System Health/i);
});
