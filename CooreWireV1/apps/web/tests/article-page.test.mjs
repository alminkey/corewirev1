import test from "node:test";
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { resolve } from "node:path";

test("renders article page as a DW/ZDF-style active reading shell", () => {
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
  assert.match(pageSource, /cw-article-reading-shell/);
  assert.match(pageSource, /cw-context-column/);
  assert.match(pageSource, /cw-support-zone/);
  assert.match(pageSource, /ArticleBody/);
  assert.match(pageSource, /FactsSection/);
  assert.match(pageSource, /AnalysisSection/);
  assert.match(pageSource, /SourcesSection/);
  assert.match(bodySource, /fullArticle/);
  assert.match(bodySource, /cw-article-reading-shell/);
  assert.match(bodySource, /cw-body-copy/);
  assert.match(bodySource, /split\(\/\\n\\n\+\/\)/);
  assert.match(factsSource, /What is Verified/i);
  assert.match(factsSource, /cw-support-zone/);
  assert.match(analysisSource, /Analysis/i);
  assert.match(analysisSource, /cw-support-zone/);
  assert.match(sourcesSource, /Sources/i);
  assert.match(sourcesSource, /cw-support-zone/);
  assert.match(headerSource, /Investigative report/i);
  assert.match(headerSource, /cw-article-hero-frame/);
  assert.match(headerSource, /cw-hero-copy/);
  const globalStyles = readFileSync(resolve("app/globals.css"), "utf8");
  assert.match(globalStyles, /\.cw-article-hero-frame/);
  assert.match(globalStyles, /\.cw-article-reading-shell/);
  assert.match(globalStyles, /\.cw-context-column/);
  assert.match(globalStyles, /\.cw-support-zone/);
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
