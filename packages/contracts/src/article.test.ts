import { describe, expect, it } from "vitest";

import { articleConfidence, articleStatus } from "./article";

describe("article contracts", () => {
  it("validates article status values", () => {
    expect(articleStatus.safeParse("published").success).toBe(true);
    expect(articleStatus.safeParse("bad").success).toBe(false);
  });

  it("validates article confidence values", () => {
    expect(articleConfidence.safeParse("high").success).toBe(true);
    expect(articleConfidence.safeParse("unknown").success).toBe(false);
  });
});
