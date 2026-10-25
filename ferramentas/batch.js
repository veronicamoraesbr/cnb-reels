// Gera todos os Reels do dia a partir do JSON da pauta.
// uso: node batch.js data/AAAA-MM-DD.json pasta_saida [trilha.mp3]
// Regras: n ímpar = notícia em fundo preto, n par = fundo branco; a tela de CTA usa o fundo oposto. CTA vem de it.cta ("seguir" ou "venda"). Copys dos CTAs ficam no template.html.
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path'), os = require('os'), { execFileSync } = require('child_process');

const ARROBA = '@canalnewsdobrasil';
const NOME = 'CNB – Canal de News do Brasil';
const MESES = ['jan','fev','mar','abr','mai','jun','jul','ago','set','out','nov','dez'];
const esc = s => String(s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));

(async () => {
  const [,, dayPath, outDir, trilhaArg] = process.argv;
  const trilha = trilhaArg || path.join(__dirname, 'trilha_cnb.mp3');
  const day = JSON.parse(fs.readFileSync(dayPath, 'utf8'));
  const [y, m, d] = day.data.split('-').map(Number);
  const quando = `${d} ${MESES[m - 1]} ${y}`;
  fs.mkdirSync(outDir, { recursive: true });
  const FPS = 30, DUR = 10;
  const browser = await chromium.launch();
  for (const it of day.itens) {
    const par = it.n % 2 === 0;
    const data = {
      tema: par ? 'claro' : 'escuro', nome: NOME, arroba: ARROBA, quando, fonte: it.fonte,
      texto: `<strong>${esc(it.titulo)}.</strong> ${esc(it.resumo)}`.replace('..</strong>', '.</strong>'),
      cta: it.cta || (par ? 'venda' : 'seguir'),
    };
    const frames = fs.mkdtempSync(path.join(os.tmpdir(), 'cnbf-'));
    const page = await browser.newPage({ viewport: { width: 1080, height: 1920 } });
    await page.goto('file://' + path.join(__dirname, 'template.html'));
    await page.evaluate(x => setup(x), data);
    for (let f = 0; f < FPS * DUR; f++) {
      await page.evaluate(ms => seek(ms), f * 1000 / FPS);
      await page.screenshot({ path: `${frames}/${String(f).padStart(4, '0')}.png` });
    }
    await page.close();
    const out = path.join(outDir, `cnb-${day.data}-${String(it.n).padStart(3, '0')}.mp4`);
    execFileSync('ffmpeg', ['-y', '-loglevel', 'error', '-framerate', String(FPS), '-i', `${frames}/%04d.png`,
      '-i', trilha, '-shortest', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '20', '-pix_fmt', 'yuv420p',
      '-r', String(FPS), '-c:a', 'aac', '-b:a', '192k', '-movflags', '+faststart', out]);
    fs.rmSync(frames, { recursive: true });
    console.log('ok', out);
  }
  await browser.close();
})();
