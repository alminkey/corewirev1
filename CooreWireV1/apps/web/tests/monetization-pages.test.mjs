import test from "node:test";
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { resolve } from "node:path";

test("renders newsletter and advertise pages plus homepage/article monetization hooks", () => {
  const newsletterPage = readFileSync(resolve("app/newsletter/page.tsx"), "utf8");
  const advertisePage = readFileSync(resolve("app/advertise/page.tsx"), "utf8");
  const homepageSource = readFileSync(resolve("app/page.tsx"), "utf8");
  const articlePageSource = readFileSync(resolve("app/articles/[slug]/page.tsx"), "utf8");

  assert.match(newsletterPage, /Newsletter/i);
  assert.match(newsletterPage, /Subscribe/i);
  assert.match(advertisePage, /Advertise/i);
  assert.match(advertisePage, /Sponsorship/i);
  assert.match(homepageSource, /NewsletterSignupCard/);
  assert.match(articlePageSource, /NewsletterSignupCard/);
});


test("public pages include AdSense slot components but admin does not", () => {
  const homepageSource = readFileSync(resolve("app/page.tsx"), "utf8");
  const articlePageSource = readFileSync(resolve("app/articles/[slug]/page.tsx"), "utf8");
  const adminPageSource = readFileSync(resolve("app/admin/page.tsx"), "utf8");
  const adSlotSource = readFileSync(resolve("components/monetization/ad-slot.tsx"), "utf8");

  assert.match(homepageSource, /AdSlot/);
  assert.match(articlePageSource, /AdSlot/);
  assert.doesNotMatch(adminPageSource, /AdSlot/);
  assert.match(adSlotSource, /GOOGLE_ADSENSE_CLIENT_ID|COREWIRE_ADSENSE_ENABLED/);
});
