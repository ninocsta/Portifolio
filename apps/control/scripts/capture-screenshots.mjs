import { chromium, devices } from "playwright";
import { mkdir } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const portfolioDir = path.resolve(__dirname, "..");
const screenshotsDir = path.join(portfolioDir, "screenshots");
const baseURL = process.env.PORTFOLIO_BASE_URL || "http://127.0.0.1:8005";

async function preparePage(page) {
  await page.addStyleTag({
    content: `
      a[href="/salao/dashboard/"] {
        display: none !important;
      }
    `,
  });
}

async function login(page) {
  await page.goto(`${baseURL}/admin/login/`, { waitUntil: "networkidle" });
  await page.locator('input[name="username"]').fill("demo");
  await page.locator('input[name="password"]').fill("Demo@123456");
  await page.locator('input[type="submit"], button[type="submit"]').click();
  await page.waitForLoadState("networkidle");
  await preparePage(page);
}

async function openDesktop() {
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext({
    viewport: { width: 1440, height: 1000 },
    locale: "pt-BR",
    timezoneId: "America/Sao_Paulo",
  });
  const page = await context.newPage();
  return { browser, page };
}

async function openMobile() {
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext({
    ...devices["iPhone 12"],
    viewport: { width: 390, height: 844 },
    locale: "pt-BR",
    timezoneId: "America/Sao_Paulo",
  });
  const page = await context.newPage();
  return { browser, page };
}

await mkdir(screenshotsDir, { recursive: true });

{
  const { browser, page } = await openDesktop();
  await login(page);
  await page.goto(`${baseURL}/financeiro/dashboard/`, { waitUntil: "networkidle" });
  await page.waitForTimeout(1200);
  await page.screenshot({ path: path.join(screenshotsDir, "01-dashboard-desktop.png"), type: "png" });
  await browser.close();
}

{
  const { browser, page } = await openDesktop();
  await login(page);
  await page.goto(`${baseURL}/admin/invoices/invoice/`, { waitUntil: "networkidle" });
  await page.waitForTimeout(600);
  await page.screenshot({ path: path.join(screenshotsDir, "02-invoices-admin-desktop.png"), type: "png" });
  await browser.close();
}

{
  const { browser, page } = await openDesktop();
  await login(page);
  await page.goto(`${baseURL}/admin/contratos/contrato/`, { waitUntil: "networkidle" });
  await page.waitForTimeout(600);
  await page.screenshot({ path: path.join(screenshotsDir, "03-contratos-admin-desktop.png"), type: "png" });
  await browser.close();
}

{
  const { browser, page } = await openDesktop();
  await login(page);
  await page.goto(`${baseURL}/admin/clientes/cliente/`, { waitUntil: "networkidle" });
  await page.waitForTimeout(600);
  await page.screenshot({ path: path.join(screenshotsDir, "04-clientes-admin-desktop.png"), type: "png" });
  await browser.close();
}

{
  const { browser, page } = await openMobile();
  await login(page);
  await page.goto(`${baseURL}/financeiro/dashboard/`, { waitUntil: "networkidle" });
  await page.waitForTimeout(1200);
  await page.screenshot({ path: path.join(screenshotsDir, "05-dashboard-mobile.png"), type: "png" });
  await browser.close();
}

console.log(`Screenshots salvos em ${screenshotsDir}`);
