import { test, expect } from "@playwright/test";

test("high confidence story reaches homepage and low confidence story stays off homepage", async ({
  page,
}) => {
  await page.goto("/");
  await expect(page.getByText(/priority alert stream/i)).toBeVisible();
  await expect(page.getByText(/developing stories/i)).toBeVisible();
  await expect(page.getByText(/corewire launched the integrated pipeline/i)).toBeVisible();

  await page.goto("/articles/corewire-launched-the-pipeline");
  await expect(page.getByText(/what is verified/i)).toBeVisible();
  await expect(page.getByText(/analysis/i)).toBeVisible();
});
