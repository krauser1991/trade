#!/usr/bin/env node
const fs = require("fs");
const os = require("os");
const path = require("path");

function loadPlaywright() {
  try {
    return require("playwright");
  } catch (error) {
    const bundled = path.join(
      os.homedir(),
      ".cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright"
    );
    try {
      return require(bundled);
    } catch (bundledError) {
      console.error("Playwright is required. Install it with: npm install playwright");
      process.exit(1);
    }
  }
}

async function launchChromium(chromium) {
  try {
    return await chromium.launch();
  } catch (error) {
    const chromePath = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome";
    if (fs.existsSync(chromePath)) {
      return chromium.launch({ executablePath: chromePath });
    }
    throw error;
  }
}

function fileUrl(inputPath) {
  const absolute = path.resolve(inputPath);
  return `file://${absolute.replace(/\\/g, "/")}`;
}

async function main() {
  const htmlPath = process.argv[2];
  if (!htmlPath || !fs.existsSync(htmlPath)) {
    console.error("Usage: node scripts/screenshot_daily_review.js output/html/file.html");
    process.exit(1);
  }

  const outputDir = path.resolve("output/images");
  fs.mkdirSync(outputDir, { recursive: true });
  const baseName = path.basename(htmlPath, path.extname(htmlPath));
  const outputPath = path.join(outputDir, `${baseName}.png`);

  const { chromium } = loadPlaywright();
  const browser = await launchChromium(chromium);
  const page = await browser.newPage({ viewport: { width: 860, height: 1200 }, deviceScaleFactor: 2 });
  await page.goto(fileUrl(htmlPath), { waitUntil: "load" });
  await page.evaluate(() => document.fonts && document.fonts.ready);
  const height = await page.evaluate(() => Math.ceil(document.documentElement.scrollHeight));
  await page.setViewportSize({ width: 860, height: Math.max(1200, height) });
  await page.screenshot({ path: outputPath, fullPage: true });
  await browser.close();
  console.log(outputPath);
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});
