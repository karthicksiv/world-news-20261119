// Renders page.html to a 1024x1024 PNG and reports any element that overflows its box.
const { chromium } = require('playwright');
const path = require('node:path');
(async () => {
  const [src, out] = process.argv.slice(2);
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1024, height: 1024 }, deviceScaleFactor: 1 });
  await p.goto('file://' + path.resolve(src));
  await p.evaluate(() => document.fonts.ready);
  const report = await p.evaluate(() => {
    const r = [];
    const pg = document.querySelector('.pg').getBoundingClientRect();
    for (const el of document.querySelectorAll('.pg > *, .card, .cols, .kick, h1')) {
      const q = el.getBoundingClientRect();
      if (q.bottom > 1024 - 8 || q.right > 1024 - 16) r.push(['outside', el.className || el.tagName, Math.round(q.right), Math.round(q.bottom)]);
      if (el.scrollWidth > el.clientWidth + 1 || el.scrollHeight > el.clientHeight + 1) r.push(['overflow', el.className || el.tagName, el.scrollWidth, el.clientWidth, el.scrollHeight, el.clientHeight]);
    }
    const ft = document.querySelector('.ft').getBoundingClientRect();
    r.push(['footer-bottom', Math.round(ft.bottom), 'cols-bottom', Math.round(document.querySelector('.cols').getBoundingClientRect().bottom), 'bot-bottom', Math.round(document.querySelector('.bot').getBoundingClientRect().bottom)]);
    return r;
  });
  console.log(JSON.stringify(report));
  await p.screenshot({ path: out, clip: { x: 0, y: 0, width: 1024, height: 1024 } });
  await b.close();
})();
