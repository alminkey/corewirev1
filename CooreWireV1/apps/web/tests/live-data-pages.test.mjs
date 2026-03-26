import test from "node:test";
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { resolve } from "node:path";

test("homepage and article page call the API client", () => {
  const homepageSource = readFileSync(resolve("app/page.tsx"), "utf8");
  const articlePageSource = readFileSync(
    resolve("app/articles/[slug]/page.tsx"),
    "utf8",
  );
  const adminPageSource = readFileSync(resolve("app/admin/page.tsx"), "utf8");
  const apiSource = readFileSync(resolve("lib/api.ts"), "utf8");

  assert.match(homepageSource, /from "..\/lib\/api"|from "\.\/\.\.\/lib\/api"/);
  assert.match(homepageSource, /getHomepage\(/);
  assert.match(articlePageSource, /from "..\/..\/..\/lib\/api"/);
  assert.match(articlePageSource, /getArticleBySlug\(/);
  assert.match(adminPageSource, /getAdminOverview\(/);
  assert.match(adminPageSource, /getAutonomySettings\(/);
  assert.match(adminPageSource, /getReviewQueue\(/);
  assert.match(adminPageSource, /getPublishedArticles\(/);
  assert.match(apiSource, /getAdminOverview\(/);
  assert.match(apiSource, /getAutonomySettings\(/);
  assert.match(apiSource, /getReviewQueue\(/);
  assert.match(apiSource, /getPublishedArticles\(/);
  assert.match(apiSource, /\/admin\/published/);
  assert.match(apiSource, /getReviewDetail\(/);
  assert.match(apiSource, /x-owner-token/);
  assert.match(apiSource, /COREWIRE_OWNER_TOKEN/);
});
