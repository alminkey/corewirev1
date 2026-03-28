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

test("renders review detail page with source summary and decision actions", () => {
  const detailPageSource = readFileSync(
    resolve("app/admin/review/[id]/page.tsx"),
    "utf8",
  );

  assert.match(detailPageSource, /Review Detail/i);
  assert.match(detailPageSource, /Approve/i);
  assert.match(detailPageSource, /Reject/i);
  assert.match(detailPageSource, /Request Rerun/i);
  assert.match(detailPageSource, /Sources/i);
  assert.match(detailPageSource, /Editorial Flags/i);
  assert.match(detailPageSource, /<form/);
  assert.match(detailPageSource, /submitReviewDecision|postReviewDecision/);
  assert.match(detailPageSource, /source\.label/);
  assert.match(detailPageSource, /source\.url/);
  assert.match(detailPageSource, /source\.publisher/);
  assert.match(detailPageSource, /typeof reason === "string"/);
  assert.match(detailPageSource, /reason\.label|reason\.message|reason\.title/);
});
