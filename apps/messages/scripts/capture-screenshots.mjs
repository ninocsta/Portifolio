import { chromium, devices } from "playwright";
import { mkdir } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const portfolioDir = path.resolve(__dirname, "..");
const screenshotsDir = path.join(portfolioDir, "screenshots");
const baseURL = process.env.PORTFOLIO_BASE_URL || "http://127.0.0.1:8002";
const credentials = {
  username: process.env.PORTFOLIO_DEMO_USERNAME || "demo",
  password: process.env.PORTFOLIO_DEMO_PASSWORD || "Demo@123456",
};

async function login(page) {
  await page.goto(`${baseURL}/login/`, { waitUntil: "networkidle" });
  await page.locator('input[name="username"]').fill(credentials.username);
  await page.locator('input[name="password"]').fill(credentials.password);
  await page.getByRole("button", { name: "Entrar" }).click();
  await page.waitForURL(/\/$/, { timeout: 10000 });
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
  await page.goto(`${baseURL}/`, { waitUntil: "networkidle" });
  await page.screenshot({ path: path.join(screenshotsDir, "01-dashboard-desktop.png"), type: "png" });
  await browser.close();
}

{
  const { browser, page } = await openDesktop();
  await login(page);
  await page.goto(`${baseURL}/?contact_page=1`, { waitUntil: "networkidle" });
  await page.locator("h2:text('Seus Contatos')").scrollIntoViewIfNeeded();
  await page.waitForTimeout(500);
  await page.screenshot({ path: path.join(screenshotsDir, "02-contatos-desktop.png"), type: "png" });
  await browser.close();
}

{
  const { browser, page } = await openDesktop();
  await login(page);
  await page.goto(`${baseURL}/`, { waitUntil: "networkidle" });
  await page.getByRole("button", { name: /Editar Modelo|Criar Modelo/ }).click();
  await page.waitForTimeout(400);
  await page.screenshot({ path: path.join(screenshotsDir, "03-modelo-mensagem-desktop.png"), type: "png" });
  await browser.close();
}

{
  const { browser, page } = await openDesktop();
  await login(page);
  await page.goto(`${baseURL}/?message_page=1`, { waitUntil: "networkidle" });
  await page.locator("text=Mensagens Enviadas").scrollIntoViewIfNeeded();
  await page.waitForTimeout(500);
  await page.screenshot({ path: path.join(screenshotsDir, "04-historico-desktop.png"), type: "png" });
  await browser.close();
}

{
  const { browser, page } = await openMobile();
  await login(page);
  await page.goto(`${baseURL}/`, { waitUntil: "networkidle" });
  await page.screenshot({ path: path.join(screenshotsDir, "05-dashboard-mobile.png"), type: "png" });
  await browser.close();
}

console.log(`Screenshots salvos em ${screenshotsDir}`);
