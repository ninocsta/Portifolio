import { chromium, devices } from "playwright";
import { mkdir } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const portfolioDir = path.resolve(__dirname, "..");
const screenshotsDir = path.join(portfolioDir, "screenshots");
const baseURL = process.env.PORTFOLIO_BASE_URL || "http://127.0.0.1:8003";

async function login(page) {
  await page.goto(`${baseURL}/login/`, { waitUntil: "networkidle" });
  await page.locator('input[name="username"]').fill("demo");
  await page.locator('input[name="password"]').fill("Demo@123456");
  await page.getByRole("button", { name: /Confirmar|Entrar/ }).click();
  await page.waitForURL(/\/(pedidos|$)/, { timeout: 10000 });
}

async function desktopPage() {
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext({ viewport: { width: 1440, height: 1000 }, locale: "pt-BR", timezoneId: "America/Sao_Paulo" });
  const page = await context.newPage();
  return { browser, page };
}

async function mobilePage() {
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext({ ...devices["iPhone 12"], viewport: { width: 390, height: 844 }, locale: "pt-BR", timezoneId: "America/Sao_Paulo" });
  const page = await context.newPage();
  return { browser, page };
}

await mkdir(screenshotsDir, { recursive: true });

{
  const { browser, page } = await desktopPage();
  await login(page);
  await page.goto(`${baseURL}/dashboard/`, { waitUntil: "networkidle" });
  await page.waitForTimeout(1200);
  await page.screenshot({ path: path.join(screenshotsDir, "01-dashboard-desktop.png"), type: "png" });
  await browser.close();
}

{
  const { browser, page } = await desktopPage();
  await login(page);
  await page.goto(`${baseURL}/pedidos/?status=Todos`, { waitUntil: "networkidle" });
  await page.screenshot({ path: path.join(screenshotsDir, "02-pedidos-desktop.png"), type: "png" });
  await browser.close();
}

{
  const { browser, page } = await desktopPage();
  await login(page);
  await page.goto(`${baseURL}/orcamentos/?status=Todos`, { waitUntil: "networkidle" });
  await page.screenshot({ path: path.join(screenshotsDir, "03-orcamentos-desktop.png"), type: "png" });
  await browser.close();
}

{
  const { browser, page } = await desktopPage();
  await login(page);
  await page.goto(`${baseURL}/estoque/`, { waitUntil: "networkidle" });
  await page.waitForTimeout(600);
  await page.screenshot({ path: path.join(screenshotsDir, "04-estoque-desktop.png"), type: "png" });
  await browser.close();
}

{
  const { browser, page } = await mobilePage();
  await login(page);
  await page.goto(`${baseURL}/estoque/`, { waitUntil: "networkidle" });
  await page.waitForTimeout(800);
  await page.screenshot({ path: path.join(screenshotsDir, "05-dashboard-mobile.png"), type: "png" });
  await browser.close();
}

console.log(`Screenshots salvos em ${screenshotsDir}`);
