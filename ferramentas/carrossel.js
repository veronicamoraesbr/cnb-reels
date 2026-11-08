// Gera os carrosséis (2 imagens 1080x1350) dos itens da pauta com "formato": "carrossel".
// uso: node carrossel.js <pauta.json> <pasta_saida>
// Saída: cnb-<data>-<NNN>-1.jpg (notícia) e cnb-<data>-<NNN>-2.jpg (CTA "seguir" ou "venda", fundo oposto).
// Regras (VECA, 07/11/2026): n ímpar = notícia no fundo azul, n par = fundo claro; página 2 sempre com o fundo oposto.
// Visual: carrossel.html + visual/ (fontes, logos, fundo azul, imagem de venda). Texto que não cabe diminui sozinho.
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path');

(async () => {
  const [,, dayPath, outDir] = process.argv;
  const day = JSON.parse(fs.readFileSync(dayPath, 'utf8'));
  const itens = day.itens.filter(i => i.formato === 'carrossel');
  fs.mkdirSync(outDir, { recursive: true });
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1080, height: 1350 } });
  let erros = 0;
  for (const it of itens) {
    const tema = it.n % 2 === 1 ? 'escuro' : 'claro', inv = tema === 'claro' ? 'escuro' : 'claro';
    const base = { titulo: it.titulo.replace(/[.!?]$/, ''), resumo: it.resumo, fonte: it.fonte };
    if (it.foto) {
      base.foto = 'file://' + path.resolve(path.dirname(dayPath), it.foto);
      base.foto_credito = it.foto_credito || ''; base.foto_posicao = it.foto_posicao;
    }
    const paginas = [{ ...base, tema, tipo: 'noticia' }, { tema: inv, tipo: it.cta === 'venda' ? 'venda' : 'seguir' }];
    for (let p = 0; p < 2; p++) {
      await page.goto('file://' + path.join(__dirname, 'carrossel.html'));
      await page.evaluate(d => preencher(d), paginas[p]);
      await page.evaluate(async () => { await document.fonts.ready; await Promise.all([...document.images].filter(i => i.getAttribute('src')).map(i => i.decode().catch(() => {}))); });
      const r = await page.evaluate(d => preencher(d), paginas[p]);   // de novo, com as fontes carregadas
      if (r && r.ok === false) { erros++; console.log('AVISO: texto não coube', it.n); }
      const f = path.join(outDir, `cnb-${day.data}-${String(it.n).padStart(3, '0')}-${p + 1}.jpg`);
      await page.screenshot({ path: f, type: 'jpeg', quality: 92 });   // JPG: o TikTok recusa foto em PNG
      console.log('ok', f);
    }
  }
  await browser.close();
  console.log(`CARROSSEIS: ${itens.length}` + (erros ? ` (${erros} com texto apertado)` : ''));
})();
