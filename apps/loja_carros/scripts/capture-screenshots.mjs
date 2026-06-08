import { chromium, devices } from "playwright";
import { mkdir } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const portfolioDir = path.resolve(__dirname, "..");
const screenshotsDir = path.join(portfolioDir, "screenshots");
const port = process.env.PORTFOLIO_PORT || "8007";
const tenantHost = process.env.PORTFOLIO_TENANT_HOST || "demo.localtest.me";
const publicBaseURL = process.env.PORTFOLIO_PUBLIC_BASE_URL || `http://${tenantHost}:${port}`;
const portalBaseURL = process.env.PORTFOLIO_PORTAL_BASE_URL || publicBaseURL;
const detailSlug = process.env.PORTFOLIO_DETAIL_SLUG || `toyota-corolla-xei-${new Date().getFullYear()}-pmt1a23`;

async function preparePage(page, { theme = "light" } = {}) {
  await page.addInitScript((preferredTheme) => {
    localStorage.setItem("theme", preferredTheme);
  }, theme);
}

async function login(page) {
  await page.goto(`${portalBaseURL}/accounts/login/`, { waitUntil: "networkidle" });
  await page.locator('input[name="username"]').fill("demo");
  await page.locator('input[name="password"]').fill("Demo@123456");
  await page.locator('button[type="submit"], input[type="submit"]').click();
  await page.waitForURL(/\/portal\/$/, { timeout: 10000 });
}

async function openDesktop({ theme = "light" } = {}) {
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext({
    viewport: { width: 1440, height: 1000 },
    locale: "pt-BR",
    timezoneId: "America/Sao_Paulo",
    colorScheme: theme,
  });
  const page = await context.newPage();
  await preparePage(page, { theme });
  return { browser, page };
}

async function openMobile({ theme = "light" } = {}) {
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext({
    ...devices["iPhone 12"],
    viewport: { width: 390, height: 844 },
    locale: "pt-BR",
    timezoneId: "America/Sao_Paulo",
    colorScheme: theme,
  });
  const page = await context.newPage();
  await preparePage(page, { theme });
  return { browser, page };
}

await mkdir(screenshotsDir, { recursive: true });

{
  const { browser, page } = await openDesktop({ theme: "light" });
  await page.goto(`${publicBaseURL}/estoque/`, { waitUntil: "networkidle" });
  await page.waitForTimeout(1200);
  await page.screenshot({ path: path.join(screenshotsDir, "01-estoque-publico-desktop.png"), type: "png" });
  await browser.close();
}

{
  const { browser, page } = await openDesktop({ theme: "light" });
  await page.goto(`${publicBaseURL}/veiculo/${detailSlug}/`, { waitUntil: "networkidle" });
  await page.waitForTimeout(1200);
  await page.screenshot({ path: path.join(screenshotsDir, "02-veiculo-detalhe-desktop.png"), type: "png" });
  await browser.close();
}

{
  const { browser, page } = await openDesktop({ theme: "dark" });
  await login(page);
  await page.goto(`${portalBaseURL}/portal/`, { waitUntil: "networkidle" });
  await page.waitForTimeout(1200);
  await page.screenshot({ path: path.join(screenshotsDir, "03-dashboard-portal-desktop.png"), type: "png" });
  await browser.close();
}

{
  const { browser, page } = await openDesktop({ theme: "dark" });
  await login(page);
  await page.goto(`${portalBaseURL}/portal/veiculos/`, { waitUntil: "networkidle" });
  await page.waitForTimeout(1000);
  await page.screenshot({ path: path.join(screenshotsDir, "04-veiculos-portal-desktop.png"), type: "png" });
  await browser.close();
}

{
  const { browser, page } = await openDesktop({ theme: "dark" });
  await login(page);
  await page.goto(`${portalBaseURL}/portal/despesas/`, { waitUntil: "networkidle" });
  await page.waitForTimeout(1000);
  await page.screenshot({ path: path.join(screenshotsDir, "05-despesas-portal-desktop.png"), type: "png" });
  await browser.close();
}

{
  const { browser, page } = await openMobile({ theme: "light" });
  await page.goto(`${publicBaseURL}/veiculo/${detailSlug}/`, { waitUntil: "networkidle" });
  await page.waitForTimeout(1000);
  await page.evaluate(() => window.scrollTo({ top: 980, behavior: "instant" }));
  await page.waitForTimeout(300);
  await page.screenshot({ path: path.join(screenshotsDir, "06-veiculo-detalhe-mobile.png"), type: "png" });
  await browser.close();
}

console.log(`Screenshots salvos em ${screenshotsDir}`);
