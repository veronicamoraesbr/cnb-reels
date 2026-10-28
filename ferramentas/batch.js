// Gera todos os Reels do dia a partir do JSON da pauta.
// uso: node batch.js data/AAAA-MM-DD.json pasta_saida [trilha.mp3]
// Plantão: itens com "urgente": true usam o carimbo URGENTE e trilha_urgente.mp3.
// Narração (padrão desde 28/10/2026): cada vídeo é narrado com a voz de narrar.py; a notícia fica na tela o tempo
// da leitura e a fala do CTA entra na tela final. Texto falado = it.narracao (se houver) ou "título. resumo".
// Para gerar sem narração: CNB_SEM_NARRACAO=1 node batch.js ...  ou  "narrar": false no item.
// Regras: n ímpar = notícia em fundo preto, n par = fundo branco; a tela de CTA usa o fundo oposto. CTA vem de it.cta ("seguir" ou "venda"). Copys dos CTAs ficam no template.html.
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path'), os = require('os'), { execFileSync } = require('child_process');

const ARROBA = '@canalnewsdobrasil';
const NOME = 'CNB – Canal de News do Brasil';
const FALA_CTA = {   // o que a voz diz na tela de CTA (mesmas copys do template.html)
  seguir: 'Siga a CNB e fique por dentro de tudo que acontece no mundo.',
  venda: 'Desafio 3 mil reais em 21 dias. Faça um Caixa Rápido e saia do aperto financeiro. Mais de 100 formas de ganhar dinheiro rápido. De 47 por 17 reais. Clique no link da bio e saiba mais.',
};
const MESES = ['jan','fev','mar','abr','mai','jun','jul','ago','set','out','nov','dez'];
const esc = s => String(s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));

(async () => {
  const [,, dayPath, outDir, trilhaArg] = process.argv;
  const trilha = trilhaArg || path.join(__dirname, 'trilha_cnb.mp3');
  const day = JSON.parse(fs.readFileSync(dayPath, 'utf8'));
  const [y, m, d] = day.data.split('-').map(Number);
  const quando = `${d} ${MESES[m - 1]} ${y}`;
  fs.mkdirSync(outDir, { recursive: true });
  const FPS = 30;
  const TEMPLATE = fs.readFileSync(path.join(__dirname, 'template.html'), 'utf8');
  const tmpHtml = path.join(os.tmpdir(), `cnb-template-${process.pid}.html`);
  // narrar.py devolve "<duração> <voz>"; voz = elevenlabs | gratis
  const narrar = (wav, txt, env = process.env) => {
    const [dur, voz] = execFileSync('python3', [path.join(__dirname, 'narrar.py'), wav, txt], { env }).toString().trim().split(/\s+/);
    return { dur: Number(dur), voz };
  };
  const vozes = { elevenlabs: 0, gratis: 0 };
  const browser = await chromium.launch();
  for (const it of day.itens) {
    const urg = !!it.urgente;              // Plantão: fundo preto, carimbo URGENTE, trilha de alerta, CTA seguir
    const par = !urg && it.n % 2 === 0;
    const data = {
      tema: par ? 'claro' : 'escuro', nome: NOME, arroba: ARROBA, quando, fonte: it.fonte,
      texto: `<strong>${esc(it.titulo)}.</strong> ${esc(it.resumo)}`.replace('..</strong>', '.</strong>'),
      cta: urg ? 'seguir' : (it.cta || (par ? 'venda' : 'seguir')), urgente: urg,
    };
    // Foto com licença livre (opcional): it.foto = arquivo local (caminho absoluto ou relativo ao JSON) e
    // it.foto_credito = texto do crédito exibido sobre a foto (ex.: "Foto: Fulano / Wikimedia Commons, CC BY 4.0")
    if (it.foto) {
      const fp = path.resolve(path.dirname(dayPath), it.foto);
      const ext = path.extname(fp).toLowerCase();
      const mime = ext === '.png' ? 'image/png' : ext === '.webp' ? 'image/webp' : 'image/jpeg';
      data.foto = `data:${mime};base64,${fs.readFileSync(fp).toString('base64')}`;
      data.fotoCredito = it.foto_credito || '';
    }
    const frames = fs.mkdtempSync(path.join(os.tmpdir(), 'cnbf-'));
    // Narração: mede a fala e empurra a saída do card / entrada do CTA (tempos >= 6,4 s do template) pelo necessário
    const comVoz = process.env.CNB_SEM_NARRACAO !== '1' && it.narrar !== false;
    let DUR = 10, desloc = 0, vozN, vozC, iniCta;
    if (comVoz) {
      vozN = path.join(frames, 'noticia.wav'); vozC = path.join(frames, 'cta.wav');
      const fala = it.narracao || `${urg ? 'Urgente! ' : ''}${it.titulo.replace(/[.!?]$/, '')}. ${it.resumo}`;
      // Áudios prontos (gerados pelo conector do ElevenLabs): it.audio_noticia e it.audio_cta (mp3/wav; caminho absoluto
      // ou relativo ao JSON da pauta). Se faltar algum, usa narrar.py.
      const pronto = k => it[k] && path.resolve(path.dirname(dayPath), it[k]);
      let n, c;
      if (pronto('audio_noticia') && pronto('audio_cta') && fs.existsSync(pronto('audio_noticia')) && fs.existsSync(pronto('audio_cta'))) {
        const conv = (src, wav) => {
          execFileSync('ffmpeg', ['-y', '-loglevel', 'error', '-i', src, '-ar', '44100', '-ac', '1', wav]);
          return { dur: Number(execFileSync('ffprobe', ['-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', wav]).toString()), voz: 'elevenlabs' };
        };
        n = conv(pronto('audio_noticia'), vozN); c = conv(pronto('audio_cta'), vozC);
      } else {
        n = narrar(vozN, fala);
        c = narrar(vozC, FALA_CTA[data.cta], n.voz === 'gratis' ? { ...process.env, CNB_VOZ: 'gratis' } : process.env);
        if (n.voz !== c.voz) n = narrar(vozN, fala, { ...process.env, CNB_VOZ: 'gratis' });   // nunca 2 vozes no mesmo vídeo
      }
      vozes[c.voz]++;
      const dN = n.dur, dC = c.dur;
      desloc = Math.max(0, 0.6 + dN + 0.4 - 6.55);
      iniCta = 6.55 + desloc + 0.5;
      DUR = Math.ceil(Math.max(10 + desloc, iniCta + dC + 0.8) * 10) / 10;
    }
    fs.writeFileSync(tmpHtml, TEMPLATE.replace(/(\d+\.\d+)s\b/g, (m, v) => Number(v) >= 6.4 ? `${(Number(v) + desloc).toFixed(2)}s` : m));
    const page = await browser.newPage({ viewport: { width: 1080, height: 1920 } });
    await page.goto('file://' + tmpHtml);
    await page.evaluate(async x => { setup(x); const i = document.getElementById('fotoimg'); if (x.foto) await i.decode(); }, data);
    for (let f = 0; f < FPS * DUR; f++) {
      await page.evaluate(ms => seek(ms), f * 1000 / FPS);
      await page.screenshot({ path: `${frames}/${String(f).padStart(4, '0')}.png` });
    }
    await page.close();
    const out = path.join(outDir, urg ? `cnb-${day.data}-urgente-${it.id || it.n}.mp4` : `cnb-${day.data}-${String(it.n).padStart(3, '0')}.mp4`);
    const musica = urg ? path.join(__dirname, 'trilha_urgente.mp3') : trilha;
    const video = ['-c:v', 'libx264', '-preset', 'veryfast', '-crf', '20', '-pix_fmt', 'yuv420p', '-r', String(FPS)];
    const audio = ['-c:a', 'aac', '-b:a', '192k', '-movflags', '+faststart', out];
    if (comVoz) {
      // trilha em loop, baixa por baixo da voz, com fade no fim; voz da notícia aos 0,6 s e do CTA na tela final
      const mix = `[1:a]atrim=0:${DUR},volume=${urg ? 0.25 : 0.18},afade=t=out:st=${(DUR - 1.2).toFixed(2)}:d=1.2[m];` +
        `[2:a]adelay=600|600,volume=1.6[n];[3:a]adelay=${Math.round(iniCta * 1000)}|${Math.round(iniCta * 1000)},volume=1.6[c];` +
        `[m][n][c]amix=inputs=3:normalize=0,alimiter=limit=0.95[a]`;
      execFileSync('ffmpeg', ['-y', '-loglevel', 'error', '-framerate', String(FPS), '-i', `${frames}/%04d.png`,
        '-stream_loop', '-1', '-i', musica, '-i', vozN, '-i', vozC, '-filter_complex', mix, '-map', '0:v', '-map', '[a]',
        '-t', String(DUR), ...video, ...audio]);
    } else {
      execFileSync('ffmpeg', ['-y', '-loglevel', 'error', '-framerate', String(FPS), '-i', `${frames}/%04d.png`,
        '-i', musica, '-shortest', ...video, ...audio]);
    }
    fs.rmSync(frames, { recursive: true });
    console.log('ok', out, comVoz ? `(narrado, ${DUR}s)` : '(sem narração)');
  }
  await browser.close();
  fs.rmSync(tmpHtml, { force: true });
  if (vozes.elevenlabs + vozes.gratis) console.log(`VOZES: ${vozes.elevenlabs} ElevenLabs, ${vozes.gratis} voz grátis` +
    (fs.existsSync(path.join(__dirname, 'voz', '.elevenlabs_sem_creditos')) ? ' (ElevenLabs SEM CRÉDITOS)' : ''));
})();
