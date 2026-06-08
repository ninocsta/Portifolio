import { chromium, devices } from "playwright";
import { mkdir } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const portfolioDir = path.resolve(__dirname, "..");
const screenshotsDir = path.join(portfolioDir, "screenshots");
const baseURL = process.env.PORTFOLIO_BASE_URL || "http://127.0.0.1:8001";
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

async function captureDesktop(route, filename, ready) {
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext({
    viewport: { width: 1440, height: 1000 },
    locale: "pt-BR",
    timezoneId: "America/Sao_Paulo",
    colorScheme: "dark",
  });
  const page = await context.newPage();
  await login(page);
  await page.goto(`${baseURL}${route}`, { waitUntil: "networkidle" });
  if (ready) {
    await ready(page);
  }
  await page.screenshot({
    path: path.join(screenshotsDir, filename),
    type: "png",
    fullPage: false,
  });
  await browser.close();
}

async function captureMobile(route, filename, ready) {
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext({
    ...devices["iPhone 12"],
    viewport: { width: 390, height: 844 },
    locale: "pt-BR",
    timezoneId: "America/Sao_Paulo",
    colorScheme: "dark",
  });
  const page = await context.newPage();
  await login(page);
  await page.goto(`${baseURL}${route}`, { waitUntil: "networkidle" });
  if (ready) {
    await ready(page);
  }
  await page.screenshot({
    path: path.join(screenshotsDir, filename),
    type: "png",
    fullPage: false,
  });
  await browser.close();
}

await mkdir(screenshotsDir, { recursive: true });

await captureDesktop("/dashboard/?periodo=3m&historico=6", "01-dashboard-desktop.png", async (page) => {
  await page.locator("#recebimentoChart").waitFor();
  await page.waitForTimeout(1200);
});

await captureDesktop("/", "02-alunos-desktop.png", async (page) => {
  await page.locator("table tbody tr").first().waitFor();
});

await captureDesktop("/pagamentos/?status=atrasado", "03-pagamentos-desktop.png", async (page) => {
  await page.locator("table tbody tr").first().waitFor();
});

await captureDesktop("/alunos/create/", "04-cadastro-aluno-desktop.png");

await captureDesktop("/turmas/", "05-turmas-desktop.png", async (page) => {
  await page.locator("table tbody tr").first().waitFor();
});

await captureMobile("/dashboard/?periodo=3m&historico=3", "06-dashboard-mobile.png", async (page) => {
  await page.locator("#recebimentoChart").waitFor();
  await page.waitForTimeout(1200);
});

console.log(`Screenshots salvos em ${screenshotsDir}`);
