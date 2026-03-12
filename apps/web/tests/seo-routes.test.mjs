import test from "node:test";
import assert from "node:assert/strict";
import { existsSync, readFileSync } from "node:fs";
import { resolve } from "node:path";

test("sitemap and robots routes exist and article pages define canonical metadata", () => {
  const homepageSource = readFileSync(resolve("app/page.tsx"), "utf8");
  const articlePageSource = readFileSync(
    resolve("app/articles/[slug]/page.tsx"),
    "utf8",
  );
  const seoSource = readFileSync(resolve("lib/seo.ts"), "utf8");

  assert.ok(existsSync(resolve("app/sitemap.ts")));
  assert.ok(existsSync(resolve("app/robots.ts")));
  assert.match(homepageSource, /generateHomepageMetadata|metadata/);
  assert.match(articlePageSource, /generateMetadata/);
  assert.match(articlePageSource, /buildArticleMetadata/);
  assert.match(seoSource, /alternates/);
  assert.match(seoSource, /canonical/);
});
