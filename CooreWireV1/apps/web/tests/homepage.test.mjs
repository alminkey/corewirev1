import test from "node:test";
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { resolve } from "node:path";

test("renders clickable public homepage sections with light editorial header", () => {
  const pageSource = readFileSync(resolve("app/page.tsx"), "utf8");
  const heroSource = readFileSync(resolve("components/home/hero-story.tsx"), "utf8");
  const railSource = readFileSync(resolve("components/home/intelligence-rail.tsx"), "utf8");
  const gridSource = readFileSync(resolve("components/home/story-grid.tsx"), "utf8");
  const developingSource = readFileSync(resolve("components/home/developing-stories.tsx"), "utf8");
  const headerSource = readFileSync(resolve("components/public/public-header.tsx"), "utf8");

  assert.match(pageSource, /PublicHeader/);
  assert.match(pageSource, /cw-home-feature-media/);
  assert.match(pageSource, /cw-grid--public/);
  assert.match(headerSource, /cw-public-header-bar/);
  assert.match(headerSource, /cw-public-section-nav/);
  assert.match(headerSource, /CoreWire/);
  assert.match(headerSource, /Newsletter/);
  assert.match(heroSource, /cw-home-hero-media/);
  assert.match(heroSource, /href=\{`\/articles\/\$\{story\.slug\}`\}/);
  assert.match(heroSource, /Read full report/i);
  assert.match(gridSource, /cw-story-card-media/);
  assert.match(gridSource, /href=\{`\/articles\/\$\{story\.slug\}`\}/);
  assert.match(railSource, /cw-rail-stack/);
  assert.match(railSource, /href=\{`\/articles\/\$\{entry\.slug\}`\}/);
  assert.match(developingSource, /href=\{`\/articles\/\$\{story\.slug\}`\}/);
});
