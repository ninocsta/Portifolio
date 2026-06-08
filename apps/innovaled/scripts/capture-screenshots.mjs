import { chromium, devices } from "playwright";
import { mkdir } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const portfolioDir = path.resolve(__dirname, "..");
const screenshotsDir = path.join(portfolioDir, "screenshots");
const baseURL = process.env.PORTFOLIO_BASE_URL || "http://127.0.0.1:8004";

async function login(page) {
  await page.goto(`${baseURL}/login/`, { waitUntil: "networkidle" });
  await page.locator('input[name="username"]').fill("demo");
  await page.locator('input[name="password"]').fill("Demo@123456");
  await page.getByRole("button", { name: /Entrar|Login/ }).click();
  await page.waitForURL(/\/(contratos\/?|dashboard\/?)/, { timeout: 10000 });
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
  await page.goto(`${baseURL}/dashboard/`, { waitUntil: "networkidle" });
  await page.waitForTimeout(1000);
  await page.screenshot({ path: path.join(screenshotsDir, "01-dashboard-desktop.png"), type: "png" });
  await browser.close();
}

{
  const { browser, page } = await openDesktop();
  await login(page);
  await page.goto(`${baseURL}/contratos/?itens=10`, { waitUntil: "networkidle" });
  await page.waitForTimeout(600);
  await page.screenshot({ path: path.join(screenshotsDir, "02-contratos-desktop.png"), type: "png" });
  await browser.close();
}

{
  const { browser, page } = await openDesktop();
  await login(page);
  await page.goto(`${baseURL}/contrato/2/`, { waitUntil: "networkidle" });
  await page.waitForTimeout(600);
  await page.screenshot({ path: path.join(screenshotsDir, "03-contrato-detalhe-desktop.png"), type: "png" });
  await browser.close();
}

{
  const { browser, page } = await openDesktop();
  await login(page);
  await page.goto(`${baseURL}/pendencias/pagamento/`, { waitUntil: "networkidle" });
  await page.waitForTimeout(600);
  await page.screenshot({ path: path.join(screenshotsDir, "04-pendencias-pagamento-desktop.png"), type: "png" });
  await browser.close();
}

{
  const { browser, page } = await openMobile();
  await login(page);
  await page.goto(`${baseURL}/contratos/?itens=10`, { waitUntil: "networkidle" });
  await page.waitForTimeout(600);
  await page.screenshot({ path: path.join(screenshotsDir, "05-contratos-mobile.png"), type: "png" });
  await browser.close();
}

console.log(`Screenshots salvos em ${screenshotsDir}`);
