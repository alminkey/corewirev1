import test from "node:test";
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { resolve } from "node:path";

test("renders article manager with manual draft inventory", () => {
  const componentSource = readFileSync(
    resolve("components/admin/article-manager.tsx"),
    "utf8",
  );

  assert.match(componentSource, /Article Manager/i);
  assert.match(componentSource, /Manual Drafts/i);
  assert.match(componentSource, /published inventory/i);
  assert.match(componentSource, /drafts\.length/);
  assert.match(componentSource, /published\.length/);
});
