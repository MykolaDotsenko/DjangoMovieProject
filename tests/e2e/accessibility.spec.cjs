const AxeBuilder = require("@axe-core/playwright").default;
const { expect, test } = require("@playwright/test");

const accessibilityRoutes = [
  { name: "home", path: "/" },
  { name: "movie catalog", path: "/movies/" },
  { name: "people catalog", path: "/people/" },
  { name: "movie detail", path: "/movies/1/" },
  { name: "person detail", path: "/people/1/" },
  { name: "sign in", path: "/login/" },
  { name: "sign up", path: "/signup/" },
];

for (const route of accessibilityRoutes) {
  test(`${route.name} has no WCAG A/AA violations`, async ({ page }) => {
    const response = await page.goto(route.path, { waitUntil: "networkidle" });
    expect(response?.ok()).toBeTruthy();

    const results = await new AxeBuilder({ page })
      .withTags(["wcag2a", "wcag2aa", "wcag21a", "wcag21aa", "wcag22aa"])
      .analyze();

    expect(results.violations).toEqual([]);
  });
}

test("search flow reaches a movie detail page", async ({ page }) => {
  await page.goto("/movies/", { waitUntil: "networkidle" });

  await page.getByRole("searchbox", { name: "Search movies" }).fill("Signal");
  await page.getByRole("button", { name: "Search" }).click();

  await expect(page.getByRole("heading", { name: "Signal Beyond" })).toBeVisible();
  await page.getByRole("link", { name: /Signal Beyond/ }).click();

  await expect(
    page.getByRole("heading", { level: 1, name: "Signal Beyond" }),
  ).toBeVisible();
});
