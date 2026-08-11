#!/usr/bin/env node
const fs = require("fs");
const os = require("os");
const path = require("path");

function fileUrl(inputPath) {
  const absolute = path.resolve(inputPath);
  return `file://${absolute.replace(/\\/g, "/")}`;
}

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

async function checkViewport(page, width) {
  await page.setViewportSize({ width, height: 1400 });
  await page.goto(fileUrl(process.argv[2]), { waitUntil: "load" });
  const result = await page.evaluate(() => {
    const root = document.querySelector("[data-review-root]");
    const risk = document.querySelector('[data-required="risk-notice"]');
    const metrics = document.querySelector('[data-required="metrics"]');
    const plan = document.querySelector('[data-required="next-day-plan"]');
    return {
      hasRoot: Boolean(root),
      hasRisk: Boolean(risk),
      hasMetrics: Boolean(metrics),
      hasPlan: Boolean(plan),
      riskText: risk ? risk.textContent || "" : "",
      scrollWidth: document.documentElement.scrollWidth,
      clientWidth: document.documentElement.clientWidth,
      height: document.documentElement.scrollHeight,
    };
  });
  const errors = [];
  if (!result.hasRoot) errors.push("missing [data-review-root]");
  if (!result.hasRisk) errors.push("missing risk notice marker");
  if (!result.hasMetrics) errors.push("missing metrics marker");
  if (!result.hasPlan) errors.push("missing next-day plan marker");
  if (!result.riskText.includes("仅作个人复盘与交易计划，不构成投资建议。")) {
    errors.push("risk notice text is missing required disclaimer");
  }
  if (result.scrollWidth - result.clientWidth > 2) {
    errors.push(`horizontal overflow at ${width}px: ${result.scrollWidth} > ${result.clientWidth}`);
  }
  if (result.height < 600) errors.push("page is unexpectedly short");
  return errors;
}

async function main() {
  const htmlPath = process.argv[2];
  if (!htmlPath || !fs.existsSync(htmlPath)) {
    console.error("Usage: node scripts/verify_daily_review_html.js output/html/file.html");
    process.exit(1);
  }

  const { chromium } = loadPlaywright();
  const browser = await launchChromium(chromium);
  const page = await browser.newPage();
  const errors = [
    ...(await checkViewport(page, 430)),
    ...(await checkViewport(page, 1180)),
  ];
  await browser.close();

  if (errors.length) {
    for (const error of errors) console.error(`verification error: ${error}`);
    process.exit(1);
  }
  console.log(`verified ${htmlPath}`);
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});
