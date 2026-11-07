# Agente CNB – Canal de News do Brasil

Instruções das duas rodadas diárias do perfil @canalnewsdobrasil (dona: VECA).
Fuso de tudo: America/Sao_Paulo. "HOJE" = data do DIA DOS POSTS nesse fuso (AAAA-MM-DD).
**Desde 03/11/2026 (VECA): a Rodada 1 roda às 23h da VÉSPERA, então nela HOJE = AMANHÃ (a data do dia seguinte).** Nas Rodadas 2 (00h30) e 3 (plantão), HOJE = a data corrente.

## Referências fixas

- Repositório (ferramentas, pautas e vídeos): `veronicamoraesbr/cnb-reels` (público, branch `main`).
  Se o repositório não estiver na sessão, use a ferramenta `add_repo` (owner `veronicamoraesbr`, repo `cnb-reels`, access `push`) e clone com `git clone --depth 1 https://github.com/veronicamoraesbr/cnb-reels /home/claude/cnb-reels`.
- Página de aprovação (Artifact com db): `https://claude.ai/artifact/V83YmaokEYY2h33EFJk5KY`.
  Use a ferramenta `ArtifactData` (carregue com ToolSearch) com esse `url`.
  Toda escrita num documento que já existe precisa de `if_version` (pegue o `version` com um `get` antes).
  - Pauta do dia: documento `dias/HOJE` (coleção `dias`, doc id = HOJE).
  - Aprovação: documento `aprovacoes/HOJE` → `{status: "aprovado"|"rejeitado", excluidos: [n...], em}`.
- Metricool: brand `blogId` = `7648862`. **Plano Starter (5 marcas), pago pela VECA em 03/11/2026.** **Desde 03/11/2026 cada vídeo vai para 3 redes no mesmo post: Instagram (Reel), TikTok e YouTube (Short)** — pedido da VECA. Todas têm o link de venda no perfil.
- Link público de um vídeo: `https://raw.githubusercontent.com/veronicamoraesbr/cnb-reels/main/videos/HOJE/<arquivo>.mp4`
- Link público das imagens de um carrossel: `https://raw.githubusercontent.com/veronicamoraesbr/cnb-reels/main/videos/HOJE/cnb-HOJE-<NNN>-1.png` e `…-2.png` (ficam na mesma pasta dos vídeos).

## Formato: metade Reels, metade carrossel (VECA, 07/11/2026 — vale a partir de 08/11/2026)

- Cada item da pauta tem `"formato": "reels"` ou `"formato": "carrossel"`. Padrão para testar engajamento: **n com resto 1 ou 2 na divisão por 4 → reels; resto 3 ou 0 → carrossel** (n1 reels, n2 reels, n3 carrossel, n4 carrossel, n5 reels…). Assim os dois formatos têm fundo azul e fundo claro. 16 posts = 8 + 8; 17 = 9 reels + 8 carrosséis. Plantão é sempre Reels e fica fora da conta.
- **Visual dos dois formatos (VECA, 07/11/2026; não mude sem ela):** logo CNB no alto, foto com cantos arredondados, título grande, resumo, "FONTE: …" e botão amarelo "SIGA O NOSSO PERFIL". Fundo azul (n ímpar) ou claro #ebebeb (n par); a tela/página de CTA sempre com o fundo oposto. CTA seguir: logo grande + "Siga a CNB e fique por dentro de tudo que acontece no mundo." + botão "SEGUIR @CANALNEWSDOBRASIL". CTA venda: selo PUBLICIDADE no lugar da logo, imagem do Caixa Rápido, título "Caixa Rápido", texto "Mais de 100 opções de serviço para sair do aperto financeiro, encontrar uma fonte de renda honesta ou dar o primeiro passo para mudar de carreira." + botão "CLIQUE NO LINK DA BIO", tudo centralizado. Arquivos em `ferramentas/visual/` (fontes, logos, fundo azul, imagem de venda).
  - Reels (`template.html`, 1080x1920): mesmo layout, fundo azul em cor lisa, conteúdo entre y 250 e 1520; mantém a barra de tempo enquanto a notícia é falada, a narração, a trilha e o carimbo URGENTE do plantão.
  - Carrossel (`carrossel.html` + `carrossel.js`, 1080x1350): página 1 = notícia (fundo azul com textura ou claro); página 2 = CTA. Sem narração (não gasta ElevenLabs).
- Redes do carrossel: `"redes": ["instagram","tiktok"]` (o YouTube não aceita post de imagens). Reels continuam nas 3 redes.
- A regra "Qual CTA usar" vale igual para os dois formatos; tente equilibrar seguir/venda dentro de cada formato.


## Calendário de volume

| Período | Posts/dia | CTA | Horários |
|---|---|---|---|
| 26/10 a 31/10/2026 | 3 | todos "seguir" | 12:00, 18:30, 21:00 |
| 01/11/2026 | 8 | pela regra "Qual CTA usar" (~metade venda) | 08:00, 10:30, 12:00, 13:00, 15:30, 18:30, 20:00, 21:30 |
| 02/11/2026 | 7 | pela regra "Qual CTA usar" | 08:00, 10:30, 12:00, 13:00, 18:30, 20:00, 21:30 |
| 03/11/2026 | 2 | n2 "venda" só se o assunto não for pessoa específica (senão "seguir") | n1 12:00 → `"redes":["instagram"]`; n2 18:30 → `"redes":["instagram","tiktok","youtube"]` |
| 04/11/2026 | 8 | pela regra "Qual CTA usar" (~metade venda) | 05:00, 07:00, 09:00, 12:00, 13:00, 18:30, 20:00, 21:30 — as 3 redes |
| 05/11/2026 | 10 | idem | 05:00, 07:00, 09:00, 11:00, 12:00, 13:00, 15:00, 18:30, 20:00, 21:30 — as 3 redes |
| 06/11/2026 | 12 | idem | 05:00, 07:00, 08:00, 09:00, 11:00, 12:00, 13:00, 15:00, 17:00, 18:30, 20:00, 21:30 — as 3 redes |
| 07/11/2026 | 14 | idem | 05:00, 06:00, 07:00, 08:00, 09:00, 10:00, 11:00, 12:00, 13:00, 15:00, 17:00, 18:30, 20:00, 21:30 — as 3 redes |
| 08/11/2026 | 16 | idem | 05:00, 06:00, 07:00, 08:00, 09:00, 10:00, 11:00, 12:00, 13:00, 14:00, 15:00, 17:00, 18:00, 19:00, 20:00, 21:30 — as 3 redes |
| a partir de 09/11/2026 | 17 | idem | 05:00, 06:00, 07:00, 08:00, 09:00, 10:00, 11:00, 12:00, 12:30, 13:00, 14:00, 15:00, 17:00, 18:00, 19:00, 20:00, 21:30 — as 3 redes |

**Aumento de 2 por dia até 17 (VECA, 03/11/2026):** 8 em 04/11 e +2 por dia até chegar a 17/dia (a partir de 09/11). Primeiro post às 05:00. O plano antigo (1 post em 04/11 e 17 já em 05/11 no Pro) foi substituído.
**Metricool Starter (pago em 03/11/2026):** o limite de 20 publicações/mês do plano grátis não vale mais. Se o Metricool recusar por limite do plano, pare e avise quantos foram agendados.
**Campo `redes` no item da pauta:** lista das redes daquele vídeo. Sem o campo = as 3 redes.
**Aumento gradual (decisão da VECA, 28/10/2026):** o volume sobe aos poucos para o Instagram não bloquear o perfil. Os 80/dia (plano antigo) ficaram suspensos; só mude o volume quando a VECA pedir e registre aqui.

### Mistura de assuntos

- Até 31/10/2026: política pode dominar (pós-eleição em alta). Nos dias de 3 posts, escolha as notícias com MAIOR potencial de engajamento.
- **Política: no máximo 1 por dia, em qualquer volume** (decisão da VECA, 02/11/2026) — só a mais forte do dia.
- **Nenhum tema passa de 3 posts por dia.** Os temas com mais posts (3) são os que mais engajam nas métricas.
- **Dias de 17 (desde 09/11), distribuição atual** (definida pelas métricas de 25/10–02/11, ver Histórico):
  - 3 esporte além do G12 (F1, seleção, UFC, vôlei, tênis, outros clubes) — melhor alcance médio (F1: 125 e 124)
  - 3 futebol do G12 (um time diferente em cada: Flamengo, Fluminense, Vasco, Botafogo, Corinthians, Palmeiras, São Paulo, Santos, Atlético-MG, Cruzeiro, Grêmio, Internacional) — 2º melhor (Fla 4x1 Vasco: 45; tabela do Brasileirão: 25)
  - 3 bolso e economia (conta de luz, salário, INSS, Pix, preços, gasolina, concursos, loterias, golpes) — 3º (conta de luz: 14; Mega-Sena: 9–13)
  - 2 serviço e saúde (Enem, feriados, documentos, clima, vacinas)
  - 2 famosos, TV, reality e música
  - 1 política
  - 1 mundo
  - 1 curiosidades
  - 1 tecnologia e IA
  - Se num dia não houver notícia forte o bastante de um tema de 3, complete com o próximo tema da lista (nunca com política).
- **Dias de 8 a 16 (rampa de 04 a 08/11):** use a mesma lista, cortando vagas de baixo para cima (primeiro tecnologia/IA, curiosidades, mundo; depois os temas de 2; os 3 temas fortes ficam com pelo menos 2 cada). Política no máximo 1, só se for forte.
- Dias de 80 (se a VECA voltar a esse volume): mesma lógica — política 1, nenhum tema com mais que a proporção dos temas fortes; redefinir com a VECA antes.
- **Ajuste pelo engajamento (na Rodada 1 em que HOJE for segunda-feira, ou seja, a de domingo às 23h):** use as ferramentas de analytics do Metricool (getAnalyticsAvailableMetrics / getAnalyticsDataByMetrics, blogId 7648862, Instagram Reels dos últimos 7 dias) e compare alcance, curtidas, comentários, compartilhamentos e salvamentos por editoria (cruze com `tag` das pautas em `pautas/`). Reordene a distribuição dos dias de 17: os 3 temas com maior alcance médio (e, no empate, mais compartilhamentos/salvamentos) ficam com 3 posts cada, os seguintes com 2 ou 1; política sempre 1; nenhum tema acima de 3; total 17. Use também TikTok e YouTube quando houver dados. **Desde 08/11 compare também Reels × carrossel** (alcance, curtidas, comentários, compartilhamentos e salvamentos médios de cada formato no Instagram) e registre no Histórico; NÃO mude a proporção 50/50 sozinho: só informe o resultado na mensagem final para a VECA decidir. Com menos de 3 vídeos de um tema na semana, não tire conclusão sobre ele (mantenha a vaga). Registre a nova distribuição e o motivo na seção "Histórico de ajustes" (logo abaixo), atualize a lista "Dias de 17" e faça commit.
- Ordem do dia: espalhe as editorias (nunca 3 seguidas iguais) e ponha as mais fortes nos horários de pico (12h–13h e 18h–22h).

### Histórico de ajustes

- 25/10/2026: distribuição inicial definida (VECA pediu política no máximo 5/dia a partir de novembro).
- 26/10/2026: sem mudança. Metricool (19–26/10) só tem 2 Reels, ambos de política (111 e 17 de alcance); não há dados para comparar editorias.
- 02/11/2026 (pedido da VECA): política no máximo 1/dia; temas fortes com até 3 posts escolhidos pelas métricas do Instagram (25/10–02/11, 31 Reels). Alcance médio: esporte além do G12 124,5 (2 Reels de F1); futebol G12 ~27 (Cruzeiro feminino, que não é G12, teve 3); política 18,6 no total, mas só ~9 fora do dia da eleição; bolso/economia 9,2; serviço 9; famosos 8; mundo 6,5; curiosidades 0. Amostra pequena (temas com 1–2 Reels) e Reels de 02/11 ainda acumulando — rever na segunda 09/11.
- 02/11/2026 (análise anterior do dia): sem mudança. Metricool (26/10–01/11): 22 Reels, quase todos de política; fora dela, os melhores alcances foram futebol (Flamengo 4x1 Vasco: 44) e conta de luz (14). Os 4 Reels de 01/11 ainda estão com alcance 0–3, amostra pequena demais para mover vagas. Reavaliar na próxima segunda, já com a mistura nova.

## Regras editoriais (sempre)

- Só notícias das últimas 24–36 h, de veículos jornalísticos confiáveis (ex.: https://www.poder360.com.br/poder-hoje/, https://agenciabrasil.ebc.com.br/ultimas, g1, Folha, Estadão, ge, Lance).
- Nada inventado: todo fato e número precisa estar na fonte. Sem duplicatas.
- Política equilibrada entre campos; acusações sempre atribuídas ("X diz que…").
- `titulo`: manchete curta (até ~55 caracteres), sem ponto final.
- `resumo`: UMA frase, com palavras próprias (nunca copiar a fonte).

## Fotos (licença livre, decisão da VECA em 28/10/2026)

- Use SÓ fotos com licença livre do Wikimedia Commons, via `ferramentas/fotos.py` (aceita domínio público, CC0, CC BY e CC BY-SA; recusa sozinho NC, ND e o resto). NUNCA use fotos tiradas dos sites de notícia, de agências (Reuters, AFP, Folhapress, Estadão Conteúdo…), do Google ou de redes sociais, mesmo com crédito.
  1. `python3 ferramentas/fotos.py buscar "<pessoa, lugar ou instituição da notícia>"`
  2. Escolha a candidata que mostra claramente o assunto (pela descrição) e baixe: `python3 ferramentas/fotos.py baixar "File:…" /tmp/fotos-HOJE` → devolve `foto`, `foto_credito`, `foto_fonte` e `foto_licenca`; copie os 4 campos para o item da pauta.
- É foto de arquivo/ilustrativa: tem de mostrar a pessoa, o lugar ou a instituição citada, nunca fingir ser do fato (nada de foto de outro acidente, outra enchente, outro jogo). Proibido: fotos de vítimas, feridos, crianças e cenas de tragédia; montagens; fotos que deixem alguém em situação vexatória.
- Confira o frame de 3 s: a foto NÃO pode mostrar faixas, placas ou números que contradigam a notícia (ex.: cartaz "Mega vai pagar 72 milhões" numa notícia de R$ 320 milhões). Se mostrar, troque a foto.
- Se a busca não achar nada, tente variações (sem hífen, nome da instituição, do lugar ou do cargo: "Mega Sena", "Loteria", "Caixa Econômica Federal").
- Sem foto boa → Reel sem foto (o card normal). Não force.
- Se o `fotos.py` der erro de rede (403/bloqueio ou 429 "too many requests" do Wikimedia que não passa após as tentativas automáticas), siga sem foto nos Reels que faltarem e avise na mensagem final: "fotos: Wikimedia bloqueado".
- As fotos ficam fora do repositório (`/tmp/fotos-HOJE`); só o vídeo vai para o git.
- O crédito aparece sobre a foto no vídeo e TAMBÉM na legenda (linha "Foto:" abaixo).
- O recorte padrão mira o rosto no alto do retrato. Ao conferir o frame de 3 s, se o rosto/assunto estiver cortado, ajuste `foto_posicao` no item (ex.: "50% 40%") e gere de novo.
- Prefira fotos com autor identificado (ex.: "Isac Nóbrega/PR", "U.S. Consulate"); evite as marcadas como "arquivo pessoal" ou com autor desconhecido.

## Qual CTA usar (regra da VECA, 02/11/2026)

- **Notícia sobre uma pessoa específica (ou com foto de pessoa identificável) → SEMPRE CTA "seguir".** Nunca associar a imagem ou o nome de alguém à propaganda (uso comercial de imagem).
- **CTA "venda" só em assuntos sem pessoa específica:** economia e bolso, serviços, loterias, clima, tecnologia, curiosidades sobre lugares/objetos, resultados de campeonato sem foco em um jogador, etc. A foto desses posts também não pode mostrar pessoa em destaque.
- Busque metade "venda" e metade "seguir" no dia, mas a regra acima vence a proporção. A alternância por horário (ímpar/par) deixa de ser obrigatória: distribua os "venda" pelo dia sem deixar 2 seguidos quando der.
- A propaganda (vídeo, imagem, narração e legenda) não cita valores nem promessas de ganho: só "Caixa Rápido" e o texto aprovado ("mais de 100 opções de serviço para sair do aperto financeiro, encontrar uma fonte de renda honesta ou dar o primeiro passo para mudar de carreira").

## Legenda

A MESMA legenda vai para Instagram, TikTok e YouTube: "link da bio" (a VECA quer essa forma nas 3 redes, inclusive no YouTube) e "Siga a CNB" (sem @, porque o @ do YouTube pode ser diferente). **Aviso de IA só na legenda** (decisão da VECA, 02/11/2026): a linha "🤖 Narração gerada por IA." vai em toda legenda, antes das hashtags; NUNCA entra na narração nem no vídeo, e as marcações de IA das plataformas (`isAiGenerated`, `isAigc`, `isAiGeneratedContent`) ficam false. Não ponha outras URLs na legenda (nas três redes elas não são clicáveis); a única exceção é o link da foto na linha "Foto:", exigido pelo crédito da licença. Até 5 hashtags (o YouTube mostra as 3 primeiras acima do título; mais de 15 ele ignora todas).

CTA "seguir":
```
<resumo>

Fonte: <fonte>
[se tiver foto] Foto: <autor> / Wikimedia Commons (<licença>) <foto_fonte>

Siga a CNB e fique por dentro de tudo que acontece no mundo.

🤖 Narração gerada por IA.

#noticias #brasil #cnb <2 hashtags do assunto>
```
CTA "venda" (a partir de 03/11/2026: selo de publicidade NA PRIMEIRA LINHA e propaganda sem valores):
```
📢 Publicidade

<resumo>

Fonte: <fonte>
[se tiver foto] Foto: <autor> / Wikimedia Commons (<licença>) <foto_fonte>

Caixa Rápido: mais de 100 opções de serviço para sair do aperto financeiro, encontrar uma fonte de renda honesta ou dar o primeiro passo para mudar de carreira. Clique no link da bio e saiba mais.

🤖 Narração gerada por IA.

#noticias #brasil #cnb <2 hashtags do assunto>
```
**Carrossel:** mesmos modelos, mas SEM a linha "🤖 Narração gerada por IA." (não tem narração) e, no "seguir", acrescente "Arraste para o lado 👉" logo depois do resumo, numa linha própria.

---

## RODADA 1 – Preparação (23:00 da véspera)

Roda às 23h e prepara os posts do DIA SEGUINTE: aqui HOJE = amanhã (ex.: rodando em 03/11 às 23h, HOJE = 2026-11-04). Use essa data em `pautas/HOJE.json`, `videos/HOJE/`, `/tmp/fotos-HOJE`, `/tmp/audios-HOJE` e `dias/HOJE`. As notícias valem se forem das últimas 24–36 h contadas a partir de agora.

1. Descubra HOJE e o volume/CTA/horários pelo calendário acima. (Compensações de plantão não existem mais desde o Metricool Starter.)
2. Pesquise e selecione as notícias. Monte `pautas/HOJE.json`:
   ```json
   {"data":"HOJE","itens":[{"n":1,"horario":"12:00","cat":"politica","tag":"Política","formato":"reels","titulo":"…","resumo":"…","fonte":"…","url":"…","cta":"seguir","legenda":"…","video":"https://raw.githubusercontent.com/…/videos/HOJE/cnb-HOJE-001.mp4"},
    {"n":3,"horario":"…","formato":"carrossel","redes":["instagram","tiktok"],"…":"…","video":"https://raw.githubusercontent.com/…/videos/HOJE/cnb-HOJE-003-1.png","imagens":["…/cnb-HOJE-003-1.png","…/cnb-HOJE-003-2.png"]}]}
   ```
   Para cada item, tente uma foto livre (seção "Fotos"); com foto, inclua no item `foto`, `foto_credito`, `foto_fonte`, `foto_licenca` e a linha "Foto:" na legenda.
   Valide com Python (quantidade certa, campos preenchidos, JSON válido, e todo item com `foto` tem `foto_credito` e a linha "Foto:" na legenda; legenda sem URL (exceto o link da foto na linha "Foto:"), com a linha "🤖 Narração gerada por IA.", legendas "venda" começando com "📢 Publicidade", `formato` em todo item pela regra da seção Formato, carrossel sem a linha de narração por IA e com `redes` ["instagram","tiktok"], nenhum "venda" sobre pessoa específica, no máximo 5 hashtags, e `redes` conforme o calendário, no modelo da seção Legenda).
3. Gere os vídeos dos itens `"formato": "reels"` (o batch pula os carrosséis sozinho; 1080x1920, NARRADOS, com a trilha da CNB baixa por baixo da voz). Narração do ElevenLabs só para os itens reels:
   `cd /home/claude/cnb-reels/ferramentas && node batch.js ../pautas/HOJE.json ../videos/HOJE`
   (fundo da notícia alterna por n; o CTA vem do campo `cta`; copys dos CTAs estão no template.html — não mude).
   - **Narração (padrão desde 28/10/2026, pedido da VECA): voz "Dyego Notícias" do ElevenLabs, pelo CONECTOR do ElevenLabs** (sem chave). Para cada item, ANTES de rodar o batch:
     1. `creative_generate_speech` com `voice_id` "eUAnqvLQWNX29twcYLUM", `model_id` "eleven_multilingual_v2", `generations_count` 1 e `prompt` = `narracao` do item (se houver) ou "<titulo>. <resumo>" (no plantão, comece com "Urgente! "). Pode disparar vários itens seguidos e depois consultar.
     2. `creative_get_flow_run_status` (flow_id + session_ids) até `all_completed`; baixe o `content_url` com `curl -sSf -o /tmp/audios-HOJE/n-<NNN>.mp3 '<url>'` (o link expira em 2 h; o ElevenLabs entrega por `storage.googleapis.com` ou `elevenlabsusercontent.com` — se o download for bloqueado, siga com a voz grátis e avise "ElevenLabs: download bloqueado (<domínio>)") e ponha `"audio_noticia": "/tmp/audios-HOJE/n-<NNN>.mp3"` no item.
     3. NÃO gere a fala do CTA: ela é fixa e fica em `ferramentas/cta_seguir_dyego.mp3` e `cta_venda_dyego.mp3` (o batch usa sozinho). Se `cta_venda_dyego.mp3` não existir, os vídeos "venda" saem inteiros com a voz grátis (nunca 2 vozes) — não gere a fala do CTA por conta própria.
     4. Nunca repita uma geração para "tentar de novo" (cobra de novo). Se o conector não estiver disponível, recusar por **créditos esgotados**/limite, ou falhar, NÃO ponha `audio_noticia` nesse item nem nos seguintes: o batch narra com a voz grátis "faber" (Piper; `narrar.py`, que na 1ª vez instala o `piper-tts` e baixa a voz para `ferramentas/voz/`, fora do git). Um vídeo nunca mistura as duas vozes.
     5. O batch termina com `VOZES: X ElevenLabs, Y voz grátis`. Se Y > 0, diga na mensagem final o motivo (ex.: "ElevenLabs sem créditos: Y vídeos com a voz grátis").
     - Os áudios ficam fora do git (`/tmp/audios-HOJE`); a chave antiga de API não é usada.
     - **Créditos do ElevenLabs só para vídeos que vão ao ar** (regra da VECA, 03/11/2026): qualquer teste, amostra, modelo ou vídeo refeito por ajuste visual usa a voz grátis (sem `audio_noticia`) ou reaproveita um áudio do Dyego já baixado. Nunca gere áudio novo para testar.
   - Campo opcional `narracao` no item: texto falado no lugar de "título. resumo". Use quando a leitura automática puder sair errada: siglas que devem ser soletradas (ex.: "P F", "S T F"), números grandes ou com ponto, nomes estrangeiros. `narrar.py` já converte sozinho º/ª, R$, %, "3.076" e "(PL-RJ)".
   - Se a narração falhar (pip, download da voz ou piper), NÃO pare o dia: gere sem voz com `CNB_SEM_NARRACAO=1 node batch.js …` e avise na mensagem final "vídeos sem narração: <erro>".
   - Tempo: ~40 s por vídeo narrado. Gere em lotes de até 4 itens (conte só os reels: 8 = 4+4; 9 = 3+3+3) (JSONs temporários com os mesmos `n`) para não estourar o tempo de cada comando.
   Confira 1 frame de 2 vídeos (ffmpeg, aos 3 s) para garantir que o texto coube.
3b. Gere os carrosséis: `cd /home/claude/cnb-reels/ferramentas && node carrossel.js ../pautas/HOJE.json ../videos/HOJE` (sai `cnb-HOJE-<NNN>-1.png` e `-2.png` para cada item carrossel). Abra 2 páginas 1 com Read para conferir texto e foto. Se aparecer "texto apertado", encurte o resumo daquele item e gere de novo.
4. Commit e push de `pautas/HOJE.json` e `videos/HOJE/` (vídeos e imagens dos carrosséis) (git user "CNB Agent", email noreply@anthropic.com). Antes do push: `git fetch origin main && git rebase origin/main`.
5. Grave a pauta na página: `ArtifactData` action `set`, collection `dias`, doc_id HOJE, data = o JSON da pauta + `"criadoEm": <ISO>`.
6. Termine com uma mensagem curta (vai como notificação): "Pauta de DD/MM pronta: R Reels e C carrosséis (1º às 05:00). Aprove até meia-noite (no máximo 00h30) na página Pauta CNB: https://claude.ai/artifact/V83YmaokEYY2h33EFJk5KY" + as 3 manchetes mais fortes.

## RODADA 2 – Agendamento (00:30)

Roda logo depois da meia-noite: HOJE = a data corrente (o dia que acabou de começar), a mesma que a Rodada 1 da véspera preparou.

1. Leia `aprovacoes/HOJE` (ArtifactData `get`).
   - Não existe ou `status` = "rejeitado": não agende nada. Termine com "Pauta de DD/MM não foi aprovada; nada foi agendado."
2. Leia `dias/HOJE`. Para cada item cujo `n` NÃO está em `excluidos`, agende no Metricool com `createScheduledPost` — UM post por item, com as redes do campo `redes` (sem o campo: as 3). Inclua `tiktokData`/`youtubeData` só se a rede estiver na lista.
   **Item carrossel** (`formato` = "carrossel"): `media` = as 2 imagens na ordem (`imagens` do item: -1.png, -2.png), SEM `videoCoverMilliseconds`, `"instagramData":{"type":"POST","isAiGenerated":false}`, `"tiktokData":{"privacyOption":"PUBLIC_TO_EVERYONE","disableComment":false,"autoAddMusic":true,"commercialContentThirdParty":false,"commercialContentOwnBrand":<true se venda>,"title":<titulo>,"photoCoverIndex":0}`, providers instagram e tiktok, sem youtubeData. Se o TikTok recusar o post de fotos, repita só com Instagram e registre. O resto do `info` é igual ao dos Reels.
   **Item reels:**
   - `blogId` "7648862"; `date` = HOJE + horario com -03:00 (horários depois da meia-noite caem no dia seguinte); horário já passado → pule e registre.
   - `info`: `{"autoPublish":true,"draft":false,"descendants":[],"firstCommentText":"","hasNotReadNotes":false,"media":[<video>],"videoCoverMilliseconds":3000,"mediaAltText":[],"providers":<um {"network":…} para cada rede em `redes` do item (sem o campo: instagram, tiktok e youtube)>,"publicationDate":{"dateTime":"AAAA-MM-DDTHH:MM:00","timezone":"America/Sao_Paulo"},"shortener":false,"smartLinkData":{"ids":[]},"text":<legenda>,"instagramData":{"type":"REEL","showReelOnFeed":true,"isAiGenerated":false},"tiktokData":{"privacyOption":"PUBLIC_TO_EVERYONE","disableComment":false,"disableDuet":false,"disableStitch":false,"autoAddMusic":false,"commercialContentThirdParty":false,"commercialContentOwnBrand":<true se cta = "venda", senão false>,"isAigc":false,"title":<titulo>},"youtubeData":{"title":<titulo>,"type":"short","privacy":"public","madeForKids":false,"isAiGeneratedContent":false,"category":<"SPORTS" se cat for futebol/esporte, senão "NEWS_POLITICS">,"tags":["noticias","brasil","cnb",<as 2 hashtags do assunto, sem #>]}}`
   - YouTube: `title` = o `titulo` do item (até 100 caracteres, sem `<` nem `>`); a legenda vira a descrição do Short.
   - TikTok: `tiktokData.title` = o `titulo` do item é OBRIGATÓRIO (sem ele o Metricool recusa com "TikTok title is required" — visto em 04/11/2026).
   - TikTok: posts com CTA "venda" divulgam produto da própria VECA → `commercialContentOwnBrand: true` (o TikTok exige essa marcação de conteúdo comercial).
   - `videoCoverMilliseconds: 3000` é a capa (Reel, TikTok e Short): o 1º frame do vídeo é preto (a notícia ainda está entrando), e aos 3 s o card está completo. Se o Metricool recusar com `VIDEO_THUMBNAIL_NOT_APPLICABLE`, repita esse item uma vez sem `videoCoverMilliseconds` e registre.
   - Se o Metricool recusar uma rede específica (conta desconectada, limite da rede), repita o item uma vez só com as redes que funcionam e registre qual rede falhou.
   - Se recusar por limite do PLANO do Metricool, PARE e informe quantos foram agendados.
3. Atualize a página: `ArtifactData` `update` em `dias/HOJE` com `{"agendado":{"em":<ISO>,"total":<qtd>}}`.
4. O Metricool guarda cópia dos vídeos: apague `videos/HOJE/` do repositório (e pastas de dias anteriores que tenham sobrado), commit e push.
5. Termine com: "DD/MM: X Reels (Instagram, TikTok e YouTube) e C carrosséis (Instagram e TikTok) agendados (Y seguir, Z venda). Primeiro às HH:MM." + qualquer erro ou rede que falhou.

## RODADA 3 – Plantão (de hora em hora, o dia todo)

Objetivo: pegar notícia BOMBÁSTICA, nível "plantão interrompe a programação", e postar sozinho na hora (a VECA autorizou postar sem aprovação, desde que confirmado por 3 veículos grandes).

1. Pesquise as notícias da última ~1h30 SOMENTE com WebSearch "extended" (várias buscas no mesmo turno, com termos de plantão + a data de hoje). NÃO use WebFetch nem abra páginas: abrir página pede aprovação manual e trava a rodada (decisão da VECA, 25/10/2026).
2. Só vale como plantão se for de um destes tipos:
   - morte de pessoa MUITO famosa no Brasil (ex-presidente, ídolo nacional do esporte, da música ou da TV);
   - acidente aéreo, desabamento ou tragédia com vítimas no Brasil; desastre natural de grande porte no Brasil;
   - ataque, guerra ou catástrofe no mundo de repercussão enorme;
   - renúncia, afastamento, prisão ou morte de alguém do topo do poder (presidente, ministro do STF, presidente da Câmara/Senado, governador).
   Não é plantão: resultado esperado (eleição, sorteio, jogo), boato, "estado de saúde", "segundo redes sociais", notícia que só um veículo deu.
3. CONFIRMAÇÃO OBRIGATÓRIA: o fato precisa estar publicado HOJE por pelo menos 3 veículos grandes e confiáveis diferentes (g1, Folha, Estadão, UOL, CNN Brasil, Agência Brasil, Poder360, ge, BBC Brasil, Reuters, AFP), com confirmação oficial ou de família/órgão responsável. Confira a data de cada resultado (notícia antiga não vale); blogs, portais pequenos e redes sociais não contam. Morte só com confirmação oficial. Na dúvida, NÃO poste.
4. Não repita: leia `plantao/registro.json` e `pautas/HOJE.json`. Se a CNB já postou ou agendou esse assunto, pare. Máximo de 3 plantões por dia.
5. Se não houver plantão: termine em silêncio, SEM notificação e sem commit.
6. Se houver: monte um JSON temporário `{"data":"HOJE","itens":[{"n":1,"id":"<slug-curto>","urgente":true,"titulo":"…","resumo":"…","fonte":"<veículo 1>, <veículo 2> e <veículo 3>","cta":"seguir"}]}` (regras editoriais valem: título curto, resumo de 1 frase com palavras próprias, nada além do que as fontes dizem) e gere o vídeo:
   `cd /home/claude/cnb-reels/ferramentas && node batch.js /tmp/plantao.json ../videos/HOJE`
   Narração: igual à Rodada 1 (conector do ElevenLabs, voz Dyego, 1 geração, prompt começando com "Urgente! "; ponha `audio_noticia` no JSON temporário; se falhar, voz grátis).
   (pode ter foto livre como na Rodada 1, se achar uma em até 2 buscas — não atrase o plantão por isso; sai `cnb-HOJE-urgente-<id>.mp4`, com carimbo URGENTE, trilha de alerta e narração que começa com "Urgente!"; se a narração falhar, use `CNB_SEM_NARRACAO=1`). Confira o frame de 3 s com ffmpeg.
7. Commit e push do vídeo (mesmo processo da Rodada 1). Espere ~1 min e confira que o link raw responde 200.
8. Agende no Metricool com `createScheduledPost` para AGORA + 10 min, mesmo `info` da Rodada 2 (as 3 redes, com `"videoCoverMilliseconds":3000`; `youtubeData.title` = "URGENTE: <titulo>"; `commercialContentOwnBrand` false), legenda no modelo "seguir" com "🚨 URGENTE: " antes do resumo e 2 hashtags do assunto.
   Desde 03/11/2026 (Metricool Starter pago) o plantão é post EXTRA nas 3 redes: não substitui post normal nem gera compensação (`compensar_em` antigos são ignorados).
9. Acrescente em `plantao/registro.json` → `{"data","hora","titulo","fontes":[url1,url2,url3],"agendado_para"}`; apague o vídeo de `videos/HOJE/` só se a Rodada 2 de hoje já tiver rodado (senão ela apaga junto); commit e push.
10. Termine com notificação curta: "🚨 Plantão postado às HH:MM: <título>. Fontes: <veículo 1>, <veículo 2>, <veículo 3>."
