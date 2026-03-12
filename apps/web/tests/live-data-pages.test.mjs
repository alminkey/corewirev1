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

  assert.match(homepageSource, /from "..\/lib\/api"|from "\.\/\.\.\/lib\/api"/);
  assert.match(homepageSource, /getHomepage\(/);
  assert.match(articlePageSource, /from "..\/..\/..\/lib\/api"/);
  assert.match(articlePageSource, /getArticleBySlug\(/);
});
