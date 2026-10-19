// Run with: cd tools/trolley && npm ci && npx playwright install webkit && npm test
import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
import { createServer } from 'node:http';
import { fileURLToPath } from 'node:url';
import { after, before, test } from 'node:test';
import { webkit } from 'playwright';

const root = new URL('../../', import.meta.url);
let browser, server, origin;
before(async () => {
  // Use the real article, layout, styles and scripts without needing Jekyll
  const post = (await readFile(new URL('_posts/2026-10-14-trolley-problem.html', root), 'utf8'))
    .split('---').slice(2).join('---').replace(/{% (?:end)?raw %}/g, '');
  const layout = (await readFile(new URL('_layouts/post.html', root), 'utf8'))
    .split('---').slice(2).join('---').replace('{{ content }}', post)
    .replace(/{%[\s\S]*?%}/g, '').replace(/{{[\s\S]*?}}/g, '');
  const html = '<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">' +
    '<link rel="stylesheet" href="/assets/site.css">' + layout;
  server = createServer(async (req, res) => {
    try {
      const path = new URL(req.url, 'http://localhost').pathname;
      if (path === '/') { res.setHeader('Content-Type', 'text/html; charset=utf-8'); res.end(html); return; }
      if (!path.startsWith('/assets/')) { res.writeHead(404).end(); return; }
      const file = new URL('.' + path, root);
      if (!fileURLToPath(file).startsWith(fileURLToPath(new URL('assets/', root)))) { res.writeHead(403).end(); return; }
      const ext = path.split('.').pop();
      res.setHeader('Content-Type', ({ html: 'text/html', js: 'text/javascript', css: 'text/css', json: 'application/json' })[ext] || 'application/octet-stream');
      res.end(await readFile(file));
    } catch { res.writeHead(404).end(); }
  });
  await new Promise(resolve => server.listen(0, '127.0.0.1', resolve));
  origin = `http://127.0.0.1:${server.address().port}`;
  browser = await webkit.launch();
});
after(async () => { await browser?.close(); await new Promise(resolve => server?.close(resolve)); });

async function sizes(page) {
  // Allow both the host resize and the pane's ResizeObserver messages to settle
  await page.waitForTimeout(400);
  return page.locator('figure.dio iframe').evaluateAll(frames => frames.map(frame => {
    const scene = frame.contentDocument.getElementById('stage-robot').getBoundingClientRect();
    return { width: scene.width, height: scene.height, frameHeight: frame.getBoundingClientRect().height };
  }));
}
async function load(page) {
  await page.goto(origin);
  // Load every lazy pane so the assertions also cover offscreen figures
  await page.locator('figure.dio iframe').evaluateAll(frames => frames.forEach(f => f.loading = 'eager'));
  await page.waitForFunction(() => [...document.querySelectorAll('figure.dio iframe')].every(f =>
    f.contentDocument?.getElementById('stage-robot')?.getBoundingClientRect().height > 0 &&
    f.closest('figure').querySelector('.dio-q-text').dataset.full));
  await page.evaluate(() => document.fonts.ready);
}

for (const height of [852, 664]) {
  test(`iPhone 14 Pro: toolbar changes do not resize scenes (${height}px layout viewport)`, async () => {
    const context = await browser.newContext({ viewport: { width: 393, height }, screen: { width: 393, height: 852 }, deviceScaleFactor: 3, isMobile: true, hasTouch: true });
    try {
      const page = await context.newPage();
      await load(page);
      const initial = await sizes(page);
      // Headless WebKit has no Safari toolbar: model its changing innerHeight and resize event,
      // leaving the layout viewport (and svh) unchanged as native toolbar scrolling does
      for (const innerHeight of [height - 188, height + 80, height]) {
        await page.evaluate(h => {
          Object.defineProperty(window, 'innerHeight', { configurable: true, value: h });
          scrollBy(0, 120);
          dispatchEvent(new Event('resize'));
          document.dispatchEvent(new Event('margins'));
        }, innerHeight);
        assert.deepEqual(await sizes(page), initial);
      }
      await page.locator('figure.dio [data-act="send"]').first().click();
      await page.waitForTimeout(1200);
      assert.deepEqual(await sizes(page), initial, 'The running scene must keep its reserved size');
      await page.waitForFunction(() => document.querySelector('figure.dio iframe').contentDocument.querySelector('#send').textContent === 'Send again');
      assert.deepEqual(await sizes(page), initial, 'The completed verdict must keep its reserved size');
      await page.locator('figure.dio [data-act="reset"]').first().click();
      assert.deepEqual(await sizes(page), initial);
      await page.setViewportSize({ width: 852, height: 393 });
      const landscape = await sizes(page);
      assert.notEqual(landscape[0].width, initial[0].width, 'Rotation must still refit the scene');
    } finally { await context.close(); }
  });
}

test('desktop: real height and width resizes still refit the scenes', async () => {
  const page = await browser.newPage({ viewport: { width: 1280, height: 800 } });
  try {
    await load(page);
    const initial = await sizes(page);
    await page.setViewportSize({ width: 1280, height: 400 });
    const short = await sizes(page);
    assert.ok(short[0].width < initial[0].width);
    await page.setViewportSize({ width: 1000, height: 800 });
    assert.notDeepEqual(await sizes(page), short);
  } finally { await page.close(); }
});
