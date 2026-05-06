/**
 * generate_pdf.js
 * Generates docs/PITCH.pdf from pitch.html using Puppeteer.
 *
 * Usage:
 *   node docs/pitch_source/generate_pdf.js
 *
 * Requirements:
 *   npm install puppeteer (inside docs/pitch_source/)
 */

const puppeteer = require('puppeteer');
const path = require('path');
const fs = require('fs');

async function generatePitch() {
  const htmlPath = path.resolve(__dirname, 'pitch.html');
  const outputPath = path.resolve(__dirname, '..', 'PITCH.pdf');

  if (!fs.existsSync(htmlPath)) {
    console.error('ERROR: pitch.html not found at', htmlPath);
    process.exit(1);
  }

  console.log('Launching Chromium...');
  const browser = await puppeteer.launch({
    headless: 'new',
    args: [
      '--no-sandbox',
      '--disable-setuid-sandbox',
      '--disable-dev-shm-usage',
    ],
  });

  const page = await browser.newPage();

  // Load the HTML file. file:// URL ensures local assets resolve correctly.
  const fileUrl = 'file://' + htmlPath;
  console.log('Loading:', fileUrl);

  await page.goto(fileUrl, {
    waitUntil: 'networkidle0',
    timeout: 30000,
  });

  // Wait for Google Fonts to load (with a reasonable timeout fallback)
  try {
    await page.waitForFunction(
      () => document.fonts && document.fonts.ready,
      { timeout: 8000 }
    );
    // Extra pause to ensure fonts render
    await new Promise(resolve => setTimeout(resolve, 1500));
  } catch (e) {
    console.warn('Font loading timeout - proceeding with system fonts fallback.');
  }

  console.log('Generating PDF...');
  await page.pdf({
    path: outputPath,
    format: 'A4',
    printBackground: true,
    preferCSSPageSize: false,
    margin: {
      top: '0mm',
      bottom: '0mm',
      left: '0mm',
      right: '0mm',
    },
  });

  await browser.close();

  const stats = fs.statSync(outputPath);
  const sizeKB = Math.round(stats.size / 1024);
  console.log('PDF generated successfully.');
  console.log('Output :', outputPath);
  console.log('Size   :', sizeKB, 'KB');
}

generatePitch().catch(err => {
  console.error('PDF generation failed:', err.message);
  process.exit(1);
});
