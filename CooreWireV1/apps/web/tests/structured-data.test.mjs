import test from "node:test";
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { resolve } from "node:path";

test("article pages emit json-ld and low-confidence stories are marked for controlled indexing", () => {
  const articlePageSource = readFileSync(
    resolve("app/articles/[slug]/page.tsx"),
    "utf8",
  );
  const seoComponentSource = readFileSync(
    resolve("components/seo/article-json-ld.tsx"),
    "utf8",
  );

  assert.match(articlePageSource, /ArticleJsonLd/);
  assert.match(articlePageSource, /robots/);
  assert.match(articlePageSource, /noindex|index: false|follow: false/);
  assert.match(seoComponentSource, /NewsArticle|Article/);
  assert.match(seoComponentSource, /application\/ld\+json/);
});
