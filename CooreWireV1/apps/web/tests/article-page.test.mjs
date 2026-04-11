import test from "node:test";
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { resolve } from "node:path";

test("renders article page as a platform reading surface", () => {
  const pageSource = readFileSync(resolve("app/articles/[slug]/page.tsx"), "utf8");
  const bodySource = readFileSync(resolve("components/article/article-body.tsx"), "utf8");
  const factsSource = readFileSync(resolve("components/article/facts-section.tsx"), "utf8");
  const analysisSource = readFileSync(
    resolve("components/article/analysis-section.tsx"),
    "utf8",
  );
  const sourcesSource = readFileSync(resolve("components/article/sources-section.tsx"), "utf8");
  const headerSource = readFileSync(resolve("components/article/article-header.tsx"), "utf8");

  assert.match(pageSource, /PublicHeader/);
  assert.match(pageSource, /cw-editorial-shell/);
  assert.match(pageSource, /cw-surface/);
  assert.match(pageSource, /cw-reading-surface/);
  assert.match(pageSource, /cw-article-shell--light/);
  assert.match(pageSource, /cw-article-layout/);
  assert.match(pageSource, /ArticleBody/);
  assert.match(pageSource, /FactsSection/);
  assert.match(pageSource, /AnalysisSection/);
  assert.match(pageSource, /SourcesSection/);
  assert.match(bodySource, /fullArticle/);
  assert.match(bodySource, /cw-module-card/);
  assert.match(bodySource, /cw-article-prose/);
  assert.match(bodySource, /split\(\/\\n\\n\+\/\)/);
  assert.match(factsSource, /What is Verified/i);
  assert.match(analysisSource, /Analysis/i);
  assert.match(sourcesSource, /Sources/i);
  assert.match(headerSource, /Investigative report/i);
  assert.match(headerSource, /cw-signal-chip/);
  assert.match(headerSource, /cw-article-header-intro/);
  const globalStyles = readFileSync(resolve("app/globals.css"), "utf8");
  assert.match(globalStyles, /\.cw-editorial-shell/);
  assert.match(globalStyles, /\.cw-surface/);
  assert.match(globalStyles, /\.cw-reading-surface/);
  assert.match(globalStyles, /\.cw-article-layout/);
  assert.match(globalStyles, /\.cw-article-prose/);
});

test("renders article sources as structured links instead of raw strings", () => {
  const typesSource = readFileSync(resolve("lib/types.ts"), "utf8");
  const sourcesSource = readFileSync(resolve("components/article/sources-section.tsx"), "utf8");

  assert.match(typesSource, /type ArticleSource =/);
  assert.match(typesSource, /sources:\s*ArticleSource\[\]/);
  assert.match(sourcesSource, /href=\{citation\.url \?\? "#"\}/);
  assert.match(sourcesSource, /citation\.label/);
});

test("article facts and analysis do not use duplicated text as react keys", () => {
  const factsSource = readFileSync(resolve("components/article/facts-section.tsx"), "utf8");
  const analysisSource = readFileSync(
    resolve("components/article/analysis-section.tsx"),
    "utf8",
  );

  assert.doesNotMatch(factsSource, /key=\{block\.text\}/);
  assert.match(factsSource, /key=\{`fact-\$\{index\}-\$\{block\.citations\.join\("\|"\)\}`/);
  assert.match(factsSource, /block\.citations\.length > 0/);
  assert.doesNotMatch(analysisSource, /key=\{block\}/);
  assert.match(analysisSource, /key=\{`analysis-\$\{index\}`\}/);
});
