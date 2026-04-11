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
  assert.match(componentSource, /Editor Workspace/i);
  assert.match(componentSource, /New Draft/i);
  assert.match(componentSource, /Save Draft/i);
  assert.match(componentSource, /Publish/i);
  assert.match(componentSource, /Archive/i);
  assert.match(componentSource, /id="drafts"/);
  assert.match(componentSource, /id="published"/);
  assert.match(componentSource, /cw-admin-workspace-grid/);
  assert.match(componentSource, /cw-workspace-module/);
  assert.match(componentSource, /cw-admin-editor-panel/);
  assert.match(componentSource, /cw-editor-surface/);
  assert.match(componentSource, /cw-admin-inventory-panel/);
  assert.match(componentSource, /name="headline"/);
  assert.match(componentSource, /name="dek"/);
  assert.match(componentSource, /name="slug"/);
  assert.match(componentSource, /name="body"/);
  assert.match(componentSource, /drafts\.length/);
  assert.match(componentSource, /published\.length/);
  assert.match(componentSource, /published\.map\(\(story, index\)/);
  assert.match(componentSource, /story\.slug \?\? story\.headline \?\? index/);
});
