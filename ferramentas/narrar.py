#!/usr/bin/env python3
"""Narração dos Reels da CNB.

uso: python3 narrar.py saida.wav "texto a ser falado"
Imprime a duração do áudio em segundos.

Voz principal: ElevenLabs, quando a variável ELEVENLABS_API_KEY existir (a chave NUNCA vai para o repositório;
ela fica nas instruções das tarefas agendadas). Voz: ELEVENLABS_VOICE_ID (padrão abaixo).
Reserva automática (sem chave ou se o ElevenLabs falhar): voz brasileira Piper "faber", grátis e offline.
Na primeira vez instala o piper-tts (pip) e baixa a voz para ferramentas/voz/ (fora do git).
Quando cair na reserva, avisa no stderr com "AVISO: ElevenLabs falhou".
"""
import json, os, re, subprocess, sys, tarfile, urllib.error, urllib.request, wave

EL_VOZ_PADRAO = 'onwK4e9ZLuTAKqWW03F9'   # troque pelo Voice ID escolhido pela VECA (ou use ELEVENLABS_VOICE_ID)
EL_MODELO = 'eleven_multilingual_v2'

AQUI = os.path.dirname(os.path.abspath(__file__))
VOZ_DIR = os.path.join(AQUI, 'voz')
NOME = 'pt_BR-faber-medium'
MODELO = os.path.join(VOZ_DIR, f'vits-piper-{NOME}', f'{NOME}.onnx')
URL = f'https://github.com/k2-fsa/sherpa-onnx/releases/download/tts-models/vits-piper-{NOME}.tar.bz2'
VELOCIDADE = '0.88'   # <1 = mais rápido (ritmo de telejornal)

ORDINAIS = {'1': 'primeiro', '2': 'segundo', '3': 'terceiro', '4': 'quarto', '5': 'quinto'}


def preparar():
    try:
        import piper  # noqa: F401
    except ImportError:
        subprocess.run([sys.executable, '-m', 'pip', 'install', '-q', 'piper-tts', '--break-system-packages'], check=True)
    if not os.path.exists(MODELO):
        os.makedirs(VOZ_DIR, exist_ok=True)
        tar = os.path.join(VOZ_DIR, 'voz.tar.bz2')
        urllib.request.urlretrieve(URL, tar)
        with tarfile.open(tar) as t:
            t.extractall(VOZ_DIR, **({'filter': 'data'} if hasattr(tarfile, 'data_filter') else {}))
        os.remove(tar)


def normalizar(txt):
    """Ajustes básicos para a voz ler direito (o campo `narracao` da pauta tem prioridade)."""
    txt = re.sub(r'\b(\d)º', lambda m: ORDINAIS.get(m.group(1), m.group(1) + 'º'), txt)
    txt = re.sub(r'\b(\d)ª', lambda m: ORDINAIS.get(m.group(1), m.group(1))[:-1] + 'a', txt)
    txt = re.sub(r'R\$\s?(\d[\d.,]*\d|\d)(?:\s+(milhões|milhão|bilhões|bilhão|mil)\b)?',
                 lambda m: m.group(1) + (f' {m.group(2)}' if m.group(2) else '') + (' de reais' if m.group(2) and m.group(2) != 'mil' else ' reais'), txt)
    txt = re.sub(r'(\d)\.(\d{3})\b', r'\1\2', txt)          # 3.076 -> 3076
    txt = txt.replace('%', ' por cento').replace(';', ',')
    txt = re.sub(r'\(([A-Z]{2,3})-([A-Z]{2})\)', r'(\1, \2)', txt)  # (PL-RJ) -> (PL, RJ)
    return re.sub(r'\s+', ' ', txt).strip()


def elevenlabs(saida, texto, chave):
    voz = os.environ.get('ELEVENLABS_VOICE_ID') or EL_VOZ_PADRAO
    corpo = json.dumps({'text': texto, 'model_id': EL_MODELO, 'language_code': 'pt',
                        'voice_settings': {'stability': 0.5, 'similarity_boost': 0.75, 'speed': 1.08}}).encode()
    req = urllib.request.Request(f'https://api.elevenlabs.io/v1/text-to-speech/{voz}?output_format=mp3_44100_128',
                                 data=corpo, headers={'xi-api-key': chave, 'Content-Type': 'application/json'})
    mp3 = saida + '.mp3'
    with urllib.request.urlopen(req, timeout=90) as r, open(mp3, 'wb') as f:
        f.write(r.read())
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', mp3, '-ar', '44100', '-ac', '1', saida], check=True)
    os.remove(mp3)


def main():
    saida, texto = sys.argv[1], sys.argv[2]
    chave = os.environ.get('ELEVENLABS_API_KEY', '').strip()
    if chave:
        try:
            elevenlabs(saida, texto, chave)
            return duracao(saida)
        except Exception as e:  # cai na voz grátis para não parar o dia
            det = e.read().decode(errors='ignore')[:200] if isinstance(e, urllib.error.HTTPError) else str(e)
            print(f'AVISO: ElevenLabs falhou ({det}); usando voz grátis', file=sys.stderr)
    preparar()
    subprocess.run([sys.executable, '-m', 'piper', '-m', MODELO, '-c', MODELO + '.json',
                    '--length-scale', VELOCIDADE, '-f', saida],
                   input=normalizar(texto).encode(), check=True, capture_output=True)
    duracao(saida)


def duracao(wav):
    with wave.open(wav) as w:
        print(round(w.getnframes() / w.getframerate(), 3))


if __name__ == '__main__':
    main()
