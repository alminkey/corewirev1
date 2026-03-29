import test from "node:test";
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { resolve } from "node:path";

test("renders hero story, intelligence rail, and developing stories section", () => {
  const pageSource = readFileSync(resolve("app/page.tsx"), "utf8");
  const heroSource = readFileSync(resolve("components/home/hero-story.tsx"), "utf8");
  const railSource = readFileSync(resolve("components/home/intelligence-rail.tsx"), "utf8");
  const developingSource = readFileSync(
    resolve("components/home/developing-stories.tsx"),
    "utf8",
  );

  assert.match(pageSource, /HeroStory/);
  assert.match(pageSource, /IntelligenceRail/);
  assert.match(pageSource, /DevelopingStories/);
  assert.match(pageSource, /CoreWire Signal Desk/i);
  assert.match(pageSource, /cw-signal-mark/);
  assert.match(heroSource, /Priority Alert Stream/i);
  assert.match(heroSource, /Signal Mesh/i);
  assert.match(railSource, /Latest Intelligence Log/i);
  assert.match(developingSource, /Developing Stories/i);
});
