# Trilha original da CNB (10 s, 120 BPM): tique de redação + baixo pulsante + pad, com a assinatura de 3 notas "C-N-B".
import numpy as np
from scipy.io import wavfile
from scipy.signal import butter, sosfilt

SR = 44100
DUR = 10.0
N = int(SR * DUR)
t = np.arange(N) / SR
L = np.zeros(N); R = np.zeros(N)
BEAT = 0.5           # 120 BPM
S16 = BEAT / 4

def hz(midi): return 440.0 * 2 ** ((midi - 69) / 12)

def add(buf, start, sig, gain=1.0):
    i = int(start * SR)
    if i >= N: return
    sig = sig[: N - i]
    buf[i:i + len(sig)] += sig * gain

def env(n, a=0.005, d=0.2):
    x = np.arange(n) / SR
    e = np.exp(-x / d)
    att = int(a * SR)
    if att: e[:att] *= np.linspace(0, 1, att)
    return e

def bell(f, dur=1.6, d=0.45):
    n = int(dur * SR); x = np.arange(n) / SR
    s = (np.sin(2*np.pi*f*x) + 0.5*np.sin(2*np.pi*2.0*f*x)*np.exp(-x/0.15)
         + 0.25*np.sin(2*np.pi*3.01*f*x)*np.exp(-x/0.08))
    return s * env(n, 0.002, d)

def tick(accent):
    n = int(0.03 * SR)
    noise = np.random.default_rng(int(accent*7)+1).standard_normal(n)
    sos = butter(4, [3000, 9000], btype="band", fs=SR, output="sos")
    return sosfilt(sos, noise) * env(n, 0.0005, 0.006 if not accent else 0.012)

def bass(f, dur):
    n = int(dur * SR); x = np.arange(n) / SR
    s = np.sin(2*np.pi*f*x) + 0.3*np.sin(2*np.pi*2*f*x)
    return np.tanh(1.5*s) * env(n, 0.004, 0.18)

def pad(freqs, dur):
    n = int(dur * SR); x = np.arange(n) / SR
    s = sum(np.sin(2*np.pi*f*x + np.sin(2*np.pi*0.3*x)) + 0.4*np.sin(2*np.pi*2.003*f*x) for f in freqs)
    e = np.minimum(1, x/0.8) * np.minimum(1, (dur - x)/0.6)
    sos = butter(2, 1800, fs=SR, output="sos")
    return sosfilt(sos, s * e)

def whoosh(dur=0.7):
    n = int(dur * SR); x = np.arange(n) / SR
    noise = np.random.default_rng(3).standard_normal(n)
    out = np.zeros(n)
    for k in range(0, n, 512):           # varredura de filtro subindo
        fc = 400 + 7000 * (k / n) ** 2
        sos = butter(2, fc, fs=SR, output="sos")
        out[k:k+512] = sosfilt(sos, noise[k:k+512])
    return out * np.sin(np.pi * x / dur) ** 2

# --- assinatura C-N-B: três notas subindo (lá menor), abre o vídeo
for k, m in enumerate([69, 72, 76]):          # A4 C5 E5
    add(L, 0.05 + k*0.18, bell(hz(m)), 0.32); add(R, 0.05 + k*0.18, bell(hz(m)), 0.28)

# --- cama de notícia 0,6 s a 6,6 s: tique em semicolcheias + baixo em colcheias + pad
for i in range(int(0.6 / S16), int(6.6 / S16)):
    st = i * S16; acc = (i % 4 == 0)
    tk = tick(acc)
    add(L, st, tk, 0.22 if acc else 0.11); add(R, st + 0.004, tk, 0.11 if acc else 0.22)
prog = [45, 45, 41, 43]                       # A2 A2 F2 G2 (um compasso cada)
for i in range(int(0.5 / (BEAT/2)), int(6.5 / (BEAT/2))):
    st = i * BEAT/2; root = prog[int(st / 2.0) % 4]
    b = bass(hz(root - 12), BEAT/2)
    add(L, st, b, 0.30); add(R, st, b, 0.30)
for c, chord in enumerate([[57, 60, 64], [57, 60, 64], [53, 57, 60], [55, 59, 62]]):
    p = pad([hz(m) for m in chord], 2.1)
    add(L, 0.5 + c*2.0, p, 0.035); add(R, 0.55 + c*2.0, p, 0.035)

# --- virada para o CTA: whoosh e assinatura resolvida em maior, mais aguda
w = whoosh(); add(L, 6.1, w, 0.25); add(R, 6.15, w, 0.25)
for k, m in enumerate([69, 76, 81]):          # A4 E5 A5
    add(L, 6.85 + k*0.18, bell(hz(m), 2.2, 0.7), 0.34); add(R, 6.85 + k*0.18, bell(hz(m), 2.2, 0.7), 0.30)
p = pad([hz(m) for m in [57, 61, 64, 69]], 3.1)   # A maior
add(L, 6.9, p, 0.05); add(R, 6.95, p, 0.05)
for i in range(int(7.0 / S16), int(9.5 / S16), 2):   # tique mais leve no fim
    add(L, i*S16, tick(False), 0.07); add(R, i*S16+0.004, tick(False), 0.07)

mix = np.stack([L, R], axis=1)
fade = np.ones(N); fn = int(0.5*SR); fade[-fn:] = np.linspace(1, 0, fn)
mix *= fade[:, None]
mix /= np.max(np.abs(mix)) * 1.12
wavfile.write("trilha_cnb_raw.wav", SR, (mix * 32767).astype(np.int16))
print("ok")
