const { test, expect } = require("@playwright/test");

test.describe("NVLink site", () => {
  test("desktop homepage renders key content and source-backed sections", async ({ page }) => {
    await page.goto("/");

    await expect(page).toHaveTitle(/NVLink Explained/i);
    await expect(page.locator("h1")).toHaveText("NVLink, explained for multi-GPU systems.");
    await expect(page.locator('meta[name="description"]')).toHaveAttribute("content", /source-backed bandwidth figures/i);
    await expect(page.locator('link[rel="canonical"]')).toHaveAttribute("href", "https://nvlink.lol/");

    await expect(page.getByRole("link", { name: "Overview" })).toBeVisible();
    await expect(page.getByRole("heading", { name: "The official generation curve is steep." })).toBeVisible();
    await expect(page.locator(".bandwidth-value").last()).toHaveText("3.6 TB/s");
    await expect(page.getByRole("heading", { name: "The fast answers people usually need first." })).toBeVisible();

    await page.getByText("Is NVLink the same thing as NVSwitch?").click();
    await expect(page.getByText("NVSwitch is the switch fabric", { exact: false })).toBeVisible();

    expect(await page.locator("img").count()).toBeGreaterThanOrEqual(1);
    const imagesLoaded = await page.evaluate(() =>
      Array.from(document.images).every((image) => image.complete && image.naturalWidth > 0)
    );
    expect(imagesLoaded).toBe(true);
  });

  test("mobile layout stays within viewport and keeps timeline reachable", async ({ browser }) => {
    const context = await browser.newContext({
      viewport: { width: 390, height: 844 },
      isMobile: true
    });
    const page = await context.newPage();

    await page.goto("/");

    await expect(page.locator("h1")).toBeVisible();
    await page.getByRole("link", { name: "Timeline" }).click();
    await expect(page.locator("#timeline")).toBeInViewport();

    const overflow = await page.evaluate(() => document.documentElement.scrollWidth - window.innerWidth);
    expect(overflow).toBeLessThanOrEqual(1);

    await expect(page.locator(".timeline-item")).toHaveCount(5);
    await context.close();
  });
});
