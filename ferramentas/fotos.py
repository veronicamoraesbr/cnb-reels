#!/usr/bin/env python3
"""Fotos com licença livre para os Reels da CNB (Wikimedia Commons).

Só aceita licenças que permitem uso comercial e adaptação com crédito:
domínio público, CC0, CC BY e CC BY-SA. Recusa NC, ND, GFDL-only, "fair use" e sem licença.

uso:
  python3 fotos.py buscar "Flávio Bolsonaro"          -> lista até 8 candidatas aprovadas (título, licença, autor, descrição)
  python3 fotos.py baixar "File:Nome.jpg" pasta/      -> baixa (miniatura de 1280 px) e imprime JSON {foto, foto_credito, foto_fonte, foto_licenca}

Precisa dos domínios commons.wikimedia.org e upload.wikimedia.org liberados na rede (as miniaturas vêm de upload.wikimedia.org).
"""
import html, json, os, re, subprocess, sys, time, urllib.error, urllib.parse, urllib.request

API = 'https://commons.wikimedia.org/w/api.php'
UA = 'CNB-Reels/1.0 (https://github.com/veronicamoraesbr/cnb-reels)'
LIVRES = re.compile(r'^(public domain|pd|cc0|cc[ -]by(-sa)?([ -]\d(\.\d)?)?( [a-z-]+)?)$', re.I)


def pegar(url, tentativas=4):
    """GET com espera e nova tentativa quando o Wikimedia responde 429/503 (limite de acessos)."""
    for i in range(tentativas):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': UA}), timeout=60) as r:
                return r.read()
        except urllib.error.HTTPError as e:
            if e.code not in (429, 503) or i == tentativas - 1:
                raise
            time.sleep(min(int(e.headers.get('Retry-After') or 0) or 5 * 2 ** i, 60))


def api(**p):
    p.update(format='json', formatversion='2', maxlag='5')
    return json.loads(pegar(API + '?' + urllib.parse.urlencode(p)))


def limpa(v):
    return re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', '', v or ''))).strip()


def info(pagina):
    ii = (pagina.get('imageinfo') or [{}])[0]
    m = ii.get('extmetadata', {})
    lic = limpa(m.get('LicenseShortName', {}).get('value'))
    livre = bool(LIVRES.match(lic)) and 'nc' not in lic.lower() and 'nd' not in lic.lower().split('-')
    return {
        'titulo': pagina['title'], 'licenca': lic, 'livre': livre,
        'autor': limpa(m.get('Artist', {}).get('value')) or 'autor desconhecido',
        'descricao': limpa(m.get('ImageDescription', {}).get('value'))[:160],
        'data': limpa(m.get('DateTimeOriginal', {}).get('value'))[:20],
        'thumb': ii.get('thumburl'), 'original': ii.get('url'), 'pagina': ii.get('descriptionurl'),
        'mime': ii.get('mime', ''), 'largura': ii.get('width', 0),
    }


def buscar(termo):
    d = api(action='query', generator='search', gsrnamespace=6, gsrlimit=30,
            gsrsearch=f'{termo} filetype:bitmap', prop='imageinfo',
            iiprop='url|extmetadata|mime|size', iiurlwidth=1280)
    fotos = [info(p) for p in d.get('query', {}).get('pages', [])]
    boas = [f for f in fotos if f['livre'] and f['mime'] in ('image/jpeg', 'image/png') and f['largura'] >= 800]
    for f in boas[:8]:
        print(f"{f['titulo']}\n   licença: {f['licenca']} | autor: {f['autor'][:60]} | data: {f['data']}\n   {f['descricao']}")
    if not boas:
        print('NENHUMA foto livre encontrada — faça o Reel sem foto.')


def baixar(titulo, pasta):
    d = api(action='query', titles=titulo, prop='imageinfo', iiprop='url|extmetadata|mime|size', iiurlwidth=1280)
    f = info(d['query']['pages'][0])
    if not f['livre']:
        sys.exit(f'RECUSADA: licença "{f["licenca"]}" não é livre para uso comercial.')
    os.makedirs(pasta, exist_ok=True)
    nome = re.sub(r'[^A-Za-z0-9._-]+', '_', f['titulo'].split(':', 1)[1])[:80]
    destino = os.path.join(pasta, nome if nome.lower().endswith(('.jpg', '.jpeg', '.png')) else nome + '.jpg')
    # miniatura em tamanho padrão do Wikimedia (1280 px). O Wikimedia limita o download de originais, então só
    # usamos miniaturas; o endereço thumb.wikimedia.org é trocado pelo equivalente em upload.wikimedia.org.
    url = re.sub(r'\?.*$', '', f['thumb'] or '').replace('https://thumb.wikimedia.org/', 'https://upload.wikimedia.org/')
    if '/thumb/' not in url:      # foto menor que 1280 px: o "thumb" já é o próprio arquivo
        url = re.sub(r'\?.*$', '', f['original'])
    with open(destino, 'wb') as out:
        out.write(pegar(url))
    autor = f['autor'] if len(f['autor']) <= 40 else f['autor'][:37] + '…'
    print(json.dumps({'foto': os.path.abspath(destino),
                      'foto_credito': f'Foto: {autor} / Wikimedia Commons, {f["licenca"]}',
                      'foto_fonte': f['pagina'], 'foto_licenca': f['licenca']}, ensure_ascii=False))


if __name__ == '__main__':
    if len(sys.argv) >= 3 and sys.argv[1] == 'buscar':
        buscar(sys.argv[2])
    elif len(sys.argv) >= 4 and sys.argv[1] == 'baixar':
        baixar(sys.argv[2], sys.argv[3])
    else:
        sys.exit(__doc__)
