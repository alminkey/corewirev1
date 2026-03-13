import { expect, test } from "@playwright/test";

test("homepage, article page, sitemap, and robots are reachable on a live stack", async ({
  page,
}) => {
  await page.goto("/");
  await expect(page.getByText(/command center/i)).toBeVisible();

  await page.goto("/articles/corewire-launched-the-pipeline");
  await expect(page.getByText(/what is verified/i)).toBeVisible();

  await page.goto("/sitemap.xml");
  await expect(page.locator("body")).toContainText(/articles\/corewire-launched-the-pipeline/i);

  await page.goto("/robots.txt");
  await expect(page.locator("body")).toContainText(/sitemap/i);
});
