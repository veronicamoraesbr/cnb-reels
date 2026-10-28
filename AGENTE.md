# Agente CNB – Canal de News do Brasil

Instruções das duas rodadas diárias do perfil @canalnewsdobrasil (dona: VECA).
Fuso de tudo: America/Sao_Paulo. "HOJE" = data de hoje nesse fuso (AAAA-MM-DD).

## Referências fixas

- Repositório (ferramentas, pautas e vídeos): `veronicamoraesbr/cnb-reels` (público, branch `main`).
  Se o repositório não estiver na sessão, use a ferramenta `add_repo` (owner `veronicamoraesbr`, repo `cnb-reels`, access `push`) e clone com `git clone --depth 1 https://github.com/veronicamoraesbr/cnb-reels /home/claude/cnb-reels`.
- Página de aprovação (Artifact com db): `https://claude.ai/artifact/V83YmaokEYY2h33EFJk5KY`.
  Use a ferramenta `ArtifactData` (carregue com ToolSearch) com esse `url`.
  Toda escrita num documento que já existe precisa de `if_version` (pegue o `version` com um `get` antes).
  - Pauta do dia: documento `dias/HOJE` (coleção `dias`, doc id = HOJE).
  - Aprovação: documento `aprovacoes/HOJE` → `{status: "aprovado"|"rejeitado", excluidos: [n...], em}`.
- Metricool: brand `blogId` = `7648862`, rede `instagram`, Instagram `canalnewsdobrasil`.
- Link público de um vídeo: `https://raw.githubusercontent.com/veronicamoraesbr/cnb-reels/main/videos/HOJE/<arquivo>.mp4`

## Calendário de volume

| Período | Posts/dia | CTA | Horários |
|---|---|---|---|
| 26/10 a 31/10/2026 | 3 | todos "seguir" | 12:00, 18:30, 21:00 |
| 01/11 a 30/11/2026 | 8 | alterna: n ímpar "seguir", n par "venda" | 08:00, 10:30, 12:00, 13:00, 15:30, 18:30, 20:00, 21:30 |
| a partir de 01/12/2026 | continua 8 até a VECA definir o próximo degrau | alterna | os mesmos de novembro |

**Aumento gradual (decisão da VECA, 28/10/2026):** o volume sobe aos poucos para o Instagram não bloquear o perfil. Os 80/dia (plano antigo) ficaram suspensos; só mude o volume quando a VECA pedir e registre aqui.

### Mistura de assuntos

- Até 31/10/2026: política pode dominar (pós-eleição em alta). Nos dias de 3 posts, escolha as notícias com MAIOR potencial de engajamento.
- A partir de 01/11/2026: **no máximo 5 notícias de política por dia** (só as mais fortes). Nos dias de até 8 posts, no máximo 1 de política; as outras 7 vão para as editorias que mais engajam (lista abaixo), sem repetir editoria mais de 2 vezes.
- Dias de 80 (se a VECA voltar a esse volume): 5 política + 12 futebol (1 por time do G12: Flamengo, Fluminense, Vasco, Botafogo, Corinthians, Palmeiras, São Paulo, Santos, Atlético-MG, Cruzeiro, Grêmio, Internacional) + 63 distribuídas pelo que mais engaja. Ponto de partida para as 63:
  - 14 bolso e economia do dia a dia (salário, INSS, Pix, preços, gasolina, concursos, loterias, golpes)
  - 12 famosos, TV, reality, música e redes sociais
  - 10 curiosidades, "inacreditável", histórias que viralizam
  - 8 esporte além do G12 (seleção, F1, UFC, vôlei, outros clubes)
  - 7 mundo
  - 6 tecnologia e IA
  - 6 saúde, bem-estar e serviço (clima, feriados, documentos)
- **Ajuste pelo engajamento (toda segunda-feira, na Rodada 1):** use as ferramentas de analytics do Metricool (getAnalyticsAvailableMetrics / getAnalyticsDataByMetrics, blogId 7648862, Instagram Reels dos últimos 7 dias) e compare alcance, curtidas, comentários, compartilhamentos e salvamentos por editoria (cruze com `tag` das pautas em `pautas/`). Mova até 6 vagas por semana das editorias mais fracas para as mais fortes, sem mexer nos 12 do G12 e sem passar de 5 de política. Registre a nova distribuição e o motivo na seção "Histórico de ajustes" (logo abaixo), atualize a lista "Ponto de partida" e faça commit.
- Ordem do dia: espalhe as editorias (nunca 3 seguidas iguais) e ponha as mais fortes nos horários de pico (12h–13h e 18h–22h).

### Histórico de ajustes

- 25/10/2026: distribuição inicial definida (VECA pediu política no máximo 5/dia a partir de novembro).
- 26/10/2026: sem mudança. Metricool (19–26/10) só tem 2 Reels, ambos de política (111 e 17 de alcance); não há dados para comparar editorias.

## Regras editoriais (sempre)

- Só notícias das últimas 24–36 h, de veículos jornalísticos confiáveis (ex.: https://www.poder360.com.br/poder-hoje/, https://agenciabrasil.ebc.com.br/ultimas, g1, Folha, Estadão, ge, Lance).
- Nada inventado: todo fato e número precisa estar na fonte. Sem duplicatas.
- Política equilibrada entre campos; acusações sempre atribuídas ("X diz que…").
- `titulo`: manchete curta (até ~55 caracteres), sem ponto final.
- `resumo`: UMA frase, com palavras próprias (nunca copiar a fonte).

## Legenda

CTA "seguir":
```
<resumo>

Fonte: <fonte>

Siga @canalnewsdobrasil e fique por dentro de tudo que acontece no mundo.

#noticias #brasil #cnb <2 hashtags do assunto>
```
CTA "venda":
```
<resumo>

Fonte: <fonte>

Desafio R$ 3.000 em 21 dias: faça um Caixa Rápido e saia do aperto financeiro. Mais de 100 formas de ganhar dinheiro rápido. De R$ 47 por R$ 17. Clique no link da bio e saiba mais.

#noticias #brasil #cnb <2 hashtags do assunto>
```

---

## RODADA 1 – Preparação (06:00)

1. Descubra HOJE e o volume/CTA/horários pelo calendário acima. Se `plantao/registro.json` tiver item com `compensar_em` = HOJE e sem `compensado`, faça 1 post a menos (tire o de menor potencial) e marque `"compensado": true`.
2. Pesquise e selecione as notícias. Monte `pautas/HOJE.json`:
   ```json
   {"data":"HOJE","itens":[{"n":1,"horario":"12:00","cat":"politica","tag":"Política","titulo":"…","resumo":"…","fonte":"…","url":"…","cta":"seguir","legenda":"…","video":"https://raw.githubusercontent.com/…/videos/HOJE/cnb-HOJE-001.mp4"}]}
   ```
   Valide com Python (quantidade certa, campos preenchidos, JSON válido).
3. Gere os vídeos (1080x1920, NARRADOS, com a trilha da CNB baixa por baixo da voz):
   `cd /home/claude/cnb-reels/ferramentas && node batch.js ../pautas/HOJE.json ../videos/HOJE`
   (fundo da notícia alterna por n; o CTA vem do campo `cta`; copys dos CTAs estão no template.html — não mude).
   - **Narração (padrão desde 28/10/2026, pedido da VECA):** `batch.js` chama `narrar.py`. Voz principal: **ElevenLabs**, usada quando a variável `ELEVENLABS_API_KEY` existir (a chave vem nas instruções da tarefa agendada; exporte-a antes de rodar o batch e NUNCA grave a chave em arquivo do repositório nem em commit). **Quando os créditos do ElevenLabs acabarem** (ou ele falhar), a narração continua sozinha com a voz grátis "faber" (Piper; na 1ª vez instala o `piper-tts` e baixa a voz do GitHub para `ferramentas/voz/`, fora do git). Um vídeo nunca mistura as duas vozes. O batch termina com a linha `VOZES: X ElevenLabs, Y voz grátis`; se aparecer "SEM CRÉDITOS", acrescente na mensagem final "ElevenLabs sem créditos: Y vídeos com a voz grátis". A voz lê "título. resumo" e depois a copy do CTA; o vídeo passa a ter 10–30 s (a notícia fica na tela o tempo da leitura). Cada linha de saída deve dizer `(narrado, XXs)`.
   - Campo opcional `narracao` no item: texto falado no lugar de "título. resumo". Use quando a leitura automática puder sair errada: siglas que devem ser soletradas (ex.: "P F", "S T F"), números grandes ou com ponto, nomes estrangeiros. `narrar.py` já converte sozinho º/ª, R$, %, "3.076" e "(PL-RJ)".
   - Se a narração falhar (pip, download da voz ou piper), NÃO pare o dia: gere sem voz com `CNB_SEM_NARRACAO=1 node batch.js …` e avise na mensagem final "vídeos sem narração: <erro>".
   - Tempo: ~40 s por vídeo narrado. Com 8 posts, gere em 2 lotes de 4 itens (JSONs temporários com os mesmos `n`) para não estourar o tempo de cada comando.
   Confira 1 frame de 2 vídeos (ffmpeg, aos 3 s) para garantir que o texto coube.
4. Commit e push de `pautas/HOJE.json` e `videos/HOJE/` (git user "CNB Agent", email noreply@anthropic.com). Antes do push: `git fetch origin main && git rebase origin/main`.
5. Grave a pauta na página: `ArtifactData` action `set`, collection `dias`, doc_id HOJE, data = o JSON da pauta + `"criadoEm": <ISO>`.
6. Termine com uma mensagem curta (vai como notificação): "Pauta de DD/MM pronta: N Reels. Aprove até 7h30 na página Pauta CNB: https://claude.ai/artifact/V83YmaokEYY2h33EFJk5KY" + as 3 manchetes mais fortes.

## RODADA 2 – Agendamento (07:30)

1. Leia `aprovacoes/HOJE` (ArtifactData `get`).
   - Não existe ou `status` = "rejeitado": não agende nada. Termine com "Pauta de DD/MM não foi aprovada; nada foi agendado."
2. Leia `dias/HOJE`. Para cada item cujo `n` NÃO está em `excluidos`, agende no Metricool com `createScheduledPost`:
   - `blogId` "7648862"; `date` = HOJE + horario com -03:00 (horários depois da meia-noite caem no dia seguinte); horário já passado → pule e registre.
   - `info`: `{"autoPublish":true,"draft":false,"descendants":[],"firstCommentText":"","hasNotReadNotes":false,"media":[<video>],"videoCoverMilliseconds":3000,"mediaAltText":[],"providers":[{"network":"instagram"}],"publicationDate":{"dateTime":"AAAA-MM-DDTHH:MM:00","timezone":"America/Sao_Paulo"},"shortener":false,"smartLinkData":{"ids":[]},"text":<legenda>,"instagramData":{"type":"REEL","showReelOnFeed":true,"isAiGenerated":false}}`
   - `videoCoverMilliseconds: 3000` é a capa do Reel no feed: o 1º frame do vídeo é preto (a notícia ainda está entrando), e aos 3 s o card está completo. Não remova.
   - Se o Metricool recusar por limite do plano, PARE e informe quantos foram agendados.
3. Atualize a página: `ArtifactData` `update` em `dias/HOJE` com `{"agendado":{"em":<ISO>,"total":<qtd>}}`.
4. O Metricool guarda cópia dos vídeos: apague `videos/HOJE/` do repositório (e pastas de dias anteriores que tenham sobrado), commit e push.
5. Termine com: "DD/MM: X Reels agendados (Y seguir, Z venda). Primeiro às HH:MM." + qualquer erro.

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
   (sai `cnb-HOJE-urgente-<id>.mp4`, com carimbo URGENTE, trilha de alerta e narração que começa com "Urgente!"; se a narração falhar, use `CNB_SEM_NARRACAO=1`). Confira o frame de 3 s com ffmpeg.
7. Commit e push do vídeo (mesmo processo da Rodada 1). Espere ~1 min e confira que o link raw responde 200.
8. Agende no Metricool com `createScheduledPost` para AGORA + 10 min, mesmo `info` da Rodada 2 (com `"videoCoverMilliseconds":3000`), legenda no modelo "seguir" com "🚨 URGENTE: " antes do resumo e 2 hashtags do assunto.
   **Até 03/11/2026 (plano gratuito do Metricool: 20 posts em outubro e 20 em 01–03/11, todos já reservados): o plantão NÃO soma post no dia, ele substitui um post normal.** Escolha a vítima entre os posts normais de HOJE ainda não publicados e com pelo menos 20 min de folga: a notícia de menor potencial de engajamento (empate → a de horário mais tarde). Então:
   - Se a Rodada 2 de hoje ainda não rodou (antes das 7h30): faça o post do plantão com `createScheduledPost` normalmente e acrescente o `n` da vítima em `excluidos` de `aprovacoes/HOJE` (ArtifactData `update` com `if_version`; se o doc não existir, não precisa — sem aprovação nada normal é postado mesmo).
   - Se já rodou: NÃO use `createScheduledPost`. Ache o post da vítima com `getScheduledPosts` (brandId 7648862, timezone America/Sao_Paulo, intervalo de hoje) e transforme-o no plantão com `updateScheduledPost` (mesmos `id` e `uuid`): troque `media`, `text` e `publicationDate` (AGORA + 10 min), mantendo o resto do `info`. Assim o total de posts do dia não muda.
   - Se não sobrar nenhum post normal pendente hoje: poste o plantão e anote em `plantao/registro.json` `"compensar_em": "<amanhã>"`; a Rodada 1 do dia seguinte faz 1 post a menos (o de menor potencial) e marca a compensação como feita (`"compensado": true`).
   - Registre a vítima no registro (`"substituiu": {"n":…, "titulo":…}`) e cite na notificação: "(substituiu o post das HH:MM)".
   A partir de 04/11/2026 (plano Starter) o plantão é post extra (vale o passo 8 normal). Se a compensação cair em 01/11, vale normalmente; se cair em 04/11 ou depois, ignore-a.
9. Acrescente em `plantao/registro.json` → `{"data","hora","titulo","fontes":[url1,url2,url3],"agendado_para"}`; apague o vídeo de `videos/HOJE/` só se a Rodada 2 de hoje já tiver rodado (senão ela apaga junto); commit e push.
10. Termine com notificação curta: "🚨 Plantão postado às HH:MM: <título>. Fontes: <veículo 1>, <veículo 2>, <veículo 3>."
