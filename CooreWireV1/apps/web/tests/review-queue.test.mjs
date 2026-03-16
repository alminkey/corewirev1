import test from "node:test";
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { resolve } from "node:path";

test("renders review queue sections for drafts, low-confidence stories, and flagged items", () => {
  const queueSource = readFileSync(
    resolve("components/admin/review-queue.tsx"),
    "utf8",
  );

  assert.match(queueSource, /Pending Drafts/i);
  assert.match(queueSource, /Low-confidence Stories/i);
  assert.match(queueSource, /Flagged Items/i);
});
