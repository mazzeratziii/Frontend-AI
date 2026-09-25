import AxeBuilder from "@axe-core/playwright";
import { expect, test } from "@playwright/test";

test("core task scenario and accessibility", async ({ page }) => {
  await page.goto("/");
  await expect(page.getByRole("heading", { level: 1 })).toBeVisible();
  const title = page.getByLabel(/task title/i);
  await title.fill("MVP evaluator task");
  await page.getByRole("button", { name: /add|create/i }).click();
  await expect(page.getByText("MVP evaluator task")).toBeVisible();
  const results = await new AxeBuilder({ page }).analyze();
  expect(results.violations).toEqual([]);
});

test("does not overflow viewport", async ({ page }) => {
  await page.goto("/");
  const overflow = await page.evaluate(() => document.documentElement.scrollWidth > document.documentElement.clientWidth);
  expect(overflow).toBe(false);
});