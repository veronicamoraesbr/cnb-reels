#!/usr/bin/env python3
"""Narração dos Reels da CNB (voz brasileira Piper "faber", grátis e offline).

uso: python3 narrar.py saida.wav "texto a ser falado"
Na primeira vez instala o piper-tts (pip) e baixa a voz para ferramentas/voz/ (fora do git).
Imprime a duração do áudio em segundos.
"""
import os, re, subprocess, sys, tarfile, urllib.request, wave

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


def main():
    saida, texto = sys.argv[1], sys.argv[2]
    preparar()
    subprocess.run([sys.executable, '-m', 'piper', '-m', MODELO, '-c', MODELO + '.json',
                    '--length-scale', VELOCIDADE, '-f', saida],
                   input=normalizar(texto).encode(), check=True, capture_output=True)
    with wave.open(saida) as w:
        print(round(w.getnframes() / w.getframerate(), 3))


if __name__ == '__main__':
    main()
