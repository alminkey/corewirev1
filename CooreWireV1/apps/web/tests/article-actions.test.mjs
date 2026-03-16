import test from "node:test";
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { resolve } from "node:path";

test("renders article lifecycle actions for the owner", () => {
  const actionsSource = readFileSync(
    resolve("components/admin/article-actions.tsx"),
    "utf8",
  );

  assert.match(actionsSource, /Approve/i);
  assert.match(actionsSource, /Reject/i);
  assert.match(actionsSource, /Retract/i);
  assert.match(actionsSource, /Correct/i);
  assert.match(actionsSource, /Supersede/i);
});
