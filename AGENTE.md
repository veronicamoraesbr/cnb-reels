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
| 01/11 e 02/11/2026 | 7 | alterna: n ímpar "seguir", n par "venda" | 08:00, 10:30, 12:30, 15:00, 18:00, 20:00, 22:00 |
| 03/11/2026 | 6 | alterna | 08:00, 10:30, 12:30, 18:00, 20:00, 22:00 |
| a partir de 04/11/2026 | 80 | alterna | das 07:00 a cada 15 min (último 02:45 do dia seguinte) |

### Mistura de assuntos

- Até 31/10/2026: política pode dominar (pós-eleição em alta). Nos dias de 3 posts, escolha as notícias com MAIOR potencial de engajamento.
- A partir de 01/11/2026: **no máximo 5 notícias de política por dia** (só as mais fortes). Nos dias de 6 ou 7 posts, no máximo 1 de política.
- Dias de 80 (a partir de 04/11): 5 política + 12 futebol (1 por time do G12: Flamengo, Fluminense, Vasco, Botafogo, Corinthians, Palmeiras, São Paulo, Santos, Atlético-MG, Cruzeiro, Grêmio, Internacional) + 63 distribuídas pelo que mais engaja. Ponto de partida para as 63:
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

## RODADA 1 – Preparação (04:00)

1. Descubra HOJE e o volume/CTA/horários pelo calendário acima.
2. Pesquise e selecione as notícias. Monte `pautas/HOJE.json`:
   ```json
   {"data":"HOJE","itens":[{"n":1,"horario":"12:00","cat":"politica","tag":"Política","titulo":"…","resumo":"…","fonte":"…","url":"…","cta":"seguir","legenda":"…","video":"https://raw.githubusercontent.com/…/videos/HOJE/cnb-HOJE-001.mp4"}]}
   ```
   Valide com Python (quantidade certa, campos preenchidos, JSON válido).
3. Gere os vídeos (1080x1920, 10 s, com a trilha da CNB):
   `cd /home/claude/cnb-reels/ferramentas && node batch.js ../pautas/HOJE.json ../videos/HOJE`
   (fundo da notícia alterna por n; o CTA vem do campo `cta`; copys dos CTAs estão no template.html — não mude).
   Confira 1 frame de 2 vídeos (ffmpeg) para garantir que o texto coube.
4. Commit e push de `pautas/HOJE.json` e `videos/HOJE/` (git user "CNB Agent", email noreply@anthropic.com). Antes do push: `git fetch origin main && git rebase origin/main`.
5. Grave a pauta na página: `ArtifactData` action `set`, collection `dias`, doc_id HOJE, data = o JSON da pauta + `"criadoEm": <ISO>`.
6. Termine com uma mensagem curta (vai como notificação): "Pauta de DD/MM pronta: N Reels. Aprove até 6h30 na página Pauta CNB: https://claude.ai/artifact/V83YmaokEYY2h33EFJk5KY" + as 3 manchetes mais fortes.

## RODADA 2 – Agendamento (06:30)

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
