#!/usr/bin/env python3
"""Fotos com licença livre para os Reels da CNB (Wikimedia Commons).

Só aceita licenças que permitem uso comercial e adaptação com crédito:
domínio público, CC0, CC BY e CC BY-SA. Recusa NC, ND, GFDL-only, "fair use" e sem licença.

uso:
  python3 fotos.py buscar "Flávio Bolsonaro"          -> lista até 8 candidatas aprovadas (título, licença, autor, descrição)
  python3 fotos.py baixar "File:Nome.jpg" pasta/      -> baixa (1080 px) e imprime JSON {foto, foto_credito, foto_fonte, foto_licenca}

Precisa dos domínios commons.wikimedia.org e upload.wikimedia.org liberados na rede.
"""
import html, json, os, re, sys, urllib.parse, urllib.request

API = 'https://commons.wikimedia.org/w/api.php'
UA = 'CNB-Reels/1.0 (https://github.com/veronicamoraesbr/cnb-reels)'
LIVRES = re.compile(r'^(public domain|pd|cc0|cc[ -]by(-sa)?([ -]\d(\.\d)?)?( [a-z-]+)?)$', re.I)


def api(**p):
    p.update(format='json', formatversion='2')
    req = urllib.request.Request(API + '?' + urllib.parse.urlencode(p), headers={'User-Agent': UA})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


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
        'thumb': ii.get('thumburl'), 'pagina': ii.get('descriptionurl'),
        'mime': ii.get('mime', ''), 'largura': ii.get('width', 0),
    }


def buscar(termo):
    d = api(action='query', generator='search', gsrnamespace=6, gsrlimit=30,
            gsrsearch=f'{termo} filetype:bitmap', prop='imageinfo',
            iiprop='url|extmetadata|mime|size', iiurlwidth=1080)
    fotos = [info(p) for p in d.get('query', {}).get('pages', [])]
    boas = [f for f in fotos if f['livre'] and f['mime'] in ('image/jpeg', 'image/png') and f['largura'] >= 800]
    for f in boas[:8]:
        print(f"{f['titulo']}\n   licença: {f['licenca']} | autor: {f['autor'][:60]} | data: {f['data']}\n   {f['descricao']}")
    if not boas:
        print('NENHUMA foto livre encontrada — faça o Reel sem foto.')


def baixar(titulo, pasta):
    d = api(action='query', titles=titulo, prop='imageinfo', iiprop='url|extmetadata|mime|size', iiurlwidth=1080)
    f = info(d['query']['pages'][0])
    if not f['livre']:
        sys.exit(f'RECUSADA: licença "{f["licenca"]}" não é livre para uso comercial.')
    os.makedirs(pasta, exist_ok=True)
    nome = re.sub(r'[^A-Za-z0-9._-]+', '_', f['titulo'].split(':', 1)[1])[:80]
    destino = os.path.join(pasta, nome if nome.lower().endswith(('.jpg', '.jpeg', '.png')) else nome + '.jpg')
    req = urllib.request.Request(f['thumb'], headers={'User-Agent': UA})
    with urllib.request.urlopen(req, timeout=60) as r, open(destino, 'wb') as out:
        out.write(r.read())
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
