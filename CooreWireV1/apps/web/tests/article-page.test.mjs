import test from "node:test";
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { resolve } from "node:path";

test("renders facts and analysis in separate labeled sections", () => {
  const pageSource = readFileSync(resolve("app/articles/[slug]/page.tsx"), "utf8");
  const factsSource = readFileSync(resolve("components/article/facts-section.tsx"), "utf8");
  const analysisSource = readFileSync(
    resolve("components/article/analysis-section.tsx"),
    "utf8",
  );
  const sourcesSource = readFileSync(resolve("components/article/sources-section.tsx"), "utf8");

  assert.match(pageSource, /FactsSection/);
  assert.match(pageSource, /AnalysisSection/);
  assert.match(pageSource, /SourcesSection/);
  assert.match(factsSource, /What is Verified/i);
  assert.match(analysisSource, /Analysis/i);
  assert.match(sourcesSource, /Sources/i);
});

test("renders article sources as structured links instead of raw strings", () => {
  const typesSource = readFileSync(resolve("lib/types.ts"), "utf8");
  const sourcesSource = readFileSync(resolve("components/article/sources-section.tsx"), "utf8");

  assert.match(typesSource, /type ArticleSource =/);
  assert.match(typesSource, /sources:\s*ArticleSource\[\]/);
  assert.match(sourcesSource, /href=\{citation\.url \?\? "#"\}/);
  assert.match(sourcesSource, /citation\.label/);
});
