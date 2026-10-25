# Trilha original do Plantão CNB (10 s): alarme de duas notas, impacto no carimbo, pulso tenso e virada para o CTA.
# uso: python3 trilha_urgente.py  -> gera trilha_urgente.mp3 (precisa de ffmpeg)
import subprocess
import numpy as np
from scipy.io import wavfile
from scipy.signal import butter, sosfilt

SR = 44100; DUR = 10.0; N = int(SR * DUR)
L = np.zeros(N); R = np.zeros(N)
rng = np.random.default_rng(11)
def hz(m): return 440.0 * 2 ** ((m - 69) / 12)
def add(buf, start, sig, g=1.0):
    i = int(start * SR)
    if i >= N: return
    sig = sig[: N - i]; buf[i:i + len(sig)] += sig * g
def env(n, a=0.005, d=0.2):
    x = np.arange(n) / SR; e = np.exp(-x / d); k = int(a * SR)
    if k: e[:k] *= np.linspace(0, 1, k)
    return e
def beep(f, dur):  # alarme: quase-quadrada filtrada, ataque seco
    n = int(dur * SR); x = np.arange(n) / SR
    s = sum(np.sin(2*np.pi*f*(2*k+1)*x)/(2*k+1) for k in range(5))
    s = sosfilt(butter(2, 4500, fs=SR, output="sos"), s)
    e = np.minimum(1, x/0.004) * np.minimum(1, (dur - x)/0.02)
    return s * e
def boom(dur=1.4):  # impacto do carimbo: queda de grave + estalo
    n = int(dur * SR); x = np.arange(n) / SR
    f = 38 + 90*np.exp(-x/0.05)
    s = np.sin(2*np.pi*np.cumsum(f)/SR) * np.exp(-x/0.45)
    hit = sosfilt(butter(2, [200, 3000], btype="band", fs=SR, output="sos"), rng.standard_normal(n)) * np.exp(-x/0.03)
    return np.tanh(2.2*s) + 0.6*hit
def tick(acc):
    n = int(0.03 * SR)
    s = sosfilt(butter(4, [3000, 9000], btype="band", fs=SR, output="sos"), rng.standard_normal(n))
    return s * env(n, 0.0005, 0.012 if acc else 0.006)
def pulse(f, dur):
    n = int(dur * SR); x = np.arange(n) / SR
    return np.tanh(1.8*(np.sin(2*np.pi*f*x) + 0.3*np.sin(2*np.pi*2*f*x))) * env(n, 0.003, 0.12)
def drone(fs, dur):
    n = int(dur * SR); x = np.arange(n) / SR
    s = sum(np.sin(2*np.pi*f*x + 0.6*np.sin(2*np.pi*0.21*x)) + 0.4*np.sin(2*np.pi*2.004*f*x) for f in fs)
    e = np.minimum(1, x/0.6) * np.minimum(1, (dur - x)/0.4)
    return sosfilt(butter(2, 1400, fs=SR, output="sos"), s * e)
def whoosh(dur=0.7):
    n = int(dur * SR); x = np.arange(n) / SR; nz = rng.standard_normal(n); out = np.zeros(n)
    for k in range(0, n, 512):
        out[k:k+512] = sosfilt(butter(2, 400 + 7000*(k/n)**2, fs=SR, output="sos"), nz[k:k+512])
    return out * np.sin(np.pi * x / dur) ** 2
def bell(f, dur=2.0, d=0.6):
    n = int(dur * SR); x = np.arange(n) / SR
    s = np.sin(2*np.pi*f*x) + 0.5*np.sin(2*np.pi*2*f*x)*np.exp(-x/0.15) + 0.25*np.sin(2*np.pi*3.01*f*x)*np.exp(-x/0.08)
    return s * env(n, 0.002, d)

# alarme: 3 pares agudo-grave (B5-F5, trítono = tensão), abre o vídeo
for k in range(3):
    st = 0.02 + k*0.36
    add(L, st, beep(hz(83), 0.15), 0.20); add(R, st, beep(hz(83), 0.15), 0.17)
    add(L, st+0.17, beep(hz(77), 0.15), 0.17); add(R, st+0.17, beep(hz(77), 0.15), 0.20)
# impacto quando o carimbo bate (0,47 s)
b = boom(); add(L, 0.47, b, 0.55); add(R, 0.47, b, 0.55)
# cama tensa 1,1 s a 6,6 s: pulso em colcheias a 132 BPM + tique + drone menor
BEAT = 60/132
for i in range(int(1.1/(BEAT/2)), int(6.6/(BEAT/2))):
    st = i*BEAT/2; root = 40 if (int(st/(BEAT*4)) % 2 == 0) else 41   # E2 / F2
    p = pulse(hz(root - 12), BEAT/2); add(L, st, p, 0.32); add(R, st, p, 0.32)
for i in range(int(1.1/(BEAT/4)), int(6.6/(BEAT/4))):
    st = i*BEAT/4; acc = i % 4 == 0; t_ = tick(acc)
    add(L, st, t_, 0.18 if acc else 0.08); add(R, st+0.004, t_, 0.08 if acc else 0.18)
d = drone([hz(m) for m in [52, 55, 58]], 5.6)       # E3 G3 Bb3 (diminuto)
add(L, 1.0, d, 0.04); add(R, 1.05, d, 0.04)
for k in range(2):                                   # lembrete do alarme, mais baixo
    st = 3.6 + k*0.36
    add(L, st, beep(hz(83), 0.12), 0.06); add(R, st+0.17, beep(hz(77), 0.12), 0.06)
# virada para o CTA: whoosh + assinatura C-N-B em maior
w = whoosh(); add(L, 6.1, w, 0.25); add(R, 6.15, w, 0.25)
for k, m in enumerate([69, 76, 81]):
    add(L, 6.85 + k*0.18, bell(hz(m), 2.2, 0.7), 0.34); add(R, 6.85 + k*0.18, bell(hz(m), 2.2, 0.7), 0.30)

mix = np.stack([L, R], axis=1)
fn = int(0.5*SR); mix[-fn:] *= np.linspace(1, 0, fn)[:, None]
mix /= np.max(np.abs(mix)) * 1.12
wavfile.write("trilha_urgente_raw.wav", SR, (mix * 32767).astype(np.int16))
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", "trilha_urgente_raw.wav", "-c:a", "libmp3lame", "-b:a", "192k", "trilha_urgente.mp3"], check=True)
print("ok")
