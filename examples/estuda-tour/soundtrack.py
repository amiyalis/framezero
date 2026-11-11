# Copyright 2026 Matheus Patricio Pessoa Santana — trilha LO-FI do vídeo "Tour do app" (39 s; mesmos instrumentos de som-desafio-lofi.py)
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / 'kit'))
from sound import *
DUR = 39.0
mus = Mix(DUR); fx = Mix(DUR); bat = Mix(DUR)
r2 = np.random.default_rng(11)

def erro(d=0.38):
    t = t_(d)
    x = saw(140, t) + saw(147, t) * 0.8
    return lp(x, 1600) * np.exp(-t * 5) * np.minimum(1, t / 0.005) * 0.22

def tique(alto=True):
    x = pop(2600 if alto else 1900, 0.035) * 0.9; c = clique(0.02) * 0.5
    x[:len(c)] += c
    return x

# ---------------- instrumentos lo-fi
def rhodes(f, d):
    t = t_(d + 0.25)
    vib = 1 + 0.0025 * np.sin(2 * np.pi * 0.7 * t)                     # leve "fita velha"
    ph = 2 * np.pi * f * np.cumsum(vib) / SR
    x = np.sin(ph) + 0.32 * np.sin(2 * ph) * np.exp(-t * 2.5) + 0.07 * np.sin(3 * ph) * np.exp(-t * 6)
    x += 0.12 * np.sin(2 * np.pi * f * 7.02 * t) * np.exp(-t * 28)       # "tine" do piano elétrico
    env = np.minimum(1, t / 0.01) * np.exp(-t * 0.9)
    rel = np.ones_like(t); n = int(0.25 * SR); rel[-n:] = np.linspace(1, 0, n) ** 2
    trem = 1 + 0.12 * np.sin(2 * np.pi * 3.0 * t)
    return x * env * rel * trem * 0.16

def acorde(notas, d, g=1.0):
    out = np.zeros(int((d + 0.4) * SR))
    for i, n in enumerate(notas):
        y = rhodes(nota(n), d); o = int(i * 0.022 * SR)                  # dedilhado suave
        m = min(len(y), len(out) - o); out[o:o + m] += y[:m]
    return lp(out, 3200) * g

def sub(f, d):
    t = t_(d)
    env = np.minimum(1, t / 0.03) * np.exp(-t * 1.2)
    rel = np.ones_like(t); n = int(0.08 * SR); rel[-n:] = np.linspace(1, 0, n)
    return (np.sin(2 * np.pi * f * t) + 0.15 * np.sin(4 * np.pi * f * t)) * env * rel * 0.42

def sino(f, d=1.2):
    t = t_(d)
    x = np.sin(2 * np.pi * f * t) + 0.25 * np.sin(2 * np.pi * f * 2.01 * t) * np.exp(-t * 4)
    return lp(x * np.exp(-t * 2.6) * np.minimum(1, t / 0.004), 4000) * 0.11

def kick_lofi():
    return lp(kick(0.38, 115, 44, 0.25), 1100) * 0.85

def caixa():
    t = t_(0.28)
    n = bp(r2.standard_normal(len(t)), 300, 3800) * np.exp(-t * 20) * 0.32
    corpo = np.sin(2 * np.pi * 185 * t) * np.exp(-t * 28) * 0.28
    return lp(n + corpo, 5200)

def chimbal(g=1.0):
    t = t_(0.06)
    return lp(hp(r2.standard_normal(len(t)), 6000, 2), 9500) * np.exp(-t * 85) * 0.11 * g

def vinil(d):
    n = int(d * SR)
    x = lp(hp(r2.standard_normal(n), 900), 5500) * 0.010
    for _ in range(int(d * 7)):                                         # estalos
        i = r2.integers(0, n - 200); a = r2.uniform(0.04, 0.22) * (1 if r2.random() < .5 else -1)
        x[i:i + 40] += a * np.exp(-np.arange(40) / 6)
    return x

# Em9  Cmaj9  Am9  Bm7 — um acorde a cada 2 s
ACORDES = [[-14, -10, -7, -3], [-14, -10, -7, -5], [-14, -10, -9, -5], [-12, -10, -7, -3]]
BAIXO = [-29, -33, -24, -26]
def acorde_em(t): return int(t // 2.0) % 4

def teclas(a, b, g=1.0):
    t = a
    while t < b - 1e-6:
        c = acorde_em(t); fimc = min(b, (int(t // 2.0) + 1) * 2.0)
        mus.add(acorde(ACORDES[c], fimc - t, g), t, 1.0)
        mus.add(sub(nota(BAIXO[c]), fimc - t), t, 0.9 * g)
        t = fimc

def batida(a, b, g=1.0):
    t = a
    while t < b - 1e-6:
        pos = round((t % 2.0) / 0.25)            # 8 semicolcheias por compasso de 2 s (meio-tempo)
        sw = 0.055 if pos % 2 == 1 else 0.0      # swing
        if pos in (0, 3): bat.add(kick_lofi(), t + sw, 1.0 * g)
        if pos == 4: bat.add(caixa(), t, 0.95 * g)
        if pos == 7: bat.add(caixa(), t + sw, 0.22 * g)        # nota fantasma
        bat.add(chimbal(1.0 if pos % 2 == 0 else 0.6), t + sw, 0.9 * g, pan=0.2)
        t += 0.25

def melodia(a, b):
    """frases curtas na pentatônica de Mi menor, a cada 4 s"""
    FR = [[(0.0, 7), (0.5, 10), (1.0, 14), (1.75, 12)], [(0.0, 10), (0.75, 7), (1.25, 5), (2.0, 7)]]
    t = a; i = 0
    while t < b - 1e-6:
        for dt, n in FR[i % 2]:
            if t + dt < b: mus.add(sino(nota(n)), t + dt, 0.9, pan=(0.25 if i % 2 else -0.25))
        t += 4.0; i += 1

# ---------------- arranjo (música)
teclas(0.0, 39.0)
for a, b in [(0.0, 26.5), (27.3, 38.5)]: batida(a, b)
for a, b in [(0.0, 26.5), (27.3, 38.5)]: melodia(a, b)
mus.add(vinil(DUR), 0.0, 1.0)
CHEIAS = [(0.0, 26.5), (27.3, 38.5)]

# ---------------- efeitos (sincronizados com tour-app.html)
fx.add(impacto(1.1, .9), 0.0)                                     # POV
fx.add(pop(620, .12), 0.5, 0.6)
fx.add(impacto(.9, .8), 1.0); fx.add(pop(520, .12), 1.0, 0.5)     # ESTUDA COMIGO
fx.add(pop(900, .14), 1.5, 0.7); fx.add(ding(1318.5, .8), 1.52, 0.5)   # 100% grátis
for k, a in enumerate([.5, .75, 1.0, 1.25, 1.5]): fx.add(pop(1000 + k * 120, .1), a + .02, 0.55, pan=(-0.4 if k % 2 == 0 else 0.4))   # selos saindo do celular
for a in [.75, 1.25, 1.75]: fx.add(whoosh(.18, True, .45), a - .02, pan=0.2)                                                      # telas trocando (deslize)
fx.add(pop(560, .1), 2.0, 0.4)
fx.add(whoosh(.3, True, 1.0), 2.24)                                                                                                 # celular voa pra câmera
fx.add(impacto(1.3, 1.0), 2.5)                                    # 5
fx.add(impacto(.6, .55), 2.75)
for i in range(7): fx.add(clique(.02), 2.9 + i * .04, 0.45)
for i in range(5): fx.add(pop(660 * 2 ** ([0, 2, 4, 7, 9][i] / 12), .1), 3.25 + i * .12, 0.65, pan=(i - 2) * 0.15)
fx.add(ding(1567.98, 1.0), 4.0, 0.7)                              # a última é a melhor
fx.add(whoosh(.3, True, .9), 4.28)
ITENS = [(4.5, 10.0, 0), (10.0, 15.5, 1), (15.5, 21.0, 2), (21.0, 26.5, 3), (27.3, 33.3, 4)]
ZOOMS = {0: [1.0, 2.9, 4.8], 1: [0.95, 4.9], 2: [1.0, 2.9, 4.8], 3: [1.0, 2.9, 4.8], 4: [1.9]}
ETQ = {0: [1.65, 3.55], 1: [1.6, 3.3], 2: [1.65, 3.55], 3: [1.65, 3.65], 4: [0.6, 3.0, 4.75]}
for S, E_, k in ITENS:
    fx.add(whoosh(.3, True, .8), S - .1)
    fx.add(impacto(.9, .7), S)
    fx.add(pop(780, .12), S + .05, 0.7)                           # número
    for j in range(3): fx.add(clique(.02), S + .12 + j * .06, 0.4)  # palavras
    if k in (1, 2, 3): fx.add(whoosh(.35, False, .6), S + .02)     # celular gira
    else: fx.add(whoosh(.5, True, .6), S + .02)                    # celular sobe
    for z in ZOOMS[k]: fx.add(whoosh(.45, True, .35), S + z)       # câmera aproxima
    for e in ETQ[k]: fx.add(pop(1040, .12), S + e, 0.65); fx.add(clique(.02), S + e + .02, 0.4)   # etiqueta
T0, T1, T2, T3, T4 = 4.5, 10.0, 15.5, 21.0, 27.3
fx.add(clique(), T0 + 2.2, 0.9); fx.add(pop(1200, .1), T0 + 2.3, 0.7); fx.add(ding(1760.0, .6), T0 + 2.35, 0.35)   # marcou a atividade
fx.add(whoosh(.4, True, .55), T1 + .45)                                                                           # folha do desafio
for i in range(4): fx.add(pop(900 + i * 120, .09), T1 + .9 + i * .07, 0.5, pan=(-0.3 if i % 2 == 0 else 0.3))
fx.add(clique(), T1 + 2.8, 1.0); fx.add(ding(1567.98, 1.1), T1 + 2.95, 0.8); fx.add(moeda(), T1 + 3.2, 0.75)    # acertou + XP
fx.add(clique(), T2 + 2.25, 0.9); fx.add(pop(700, .12), T2 + 2.3, 0.6)                                            # abre o livro
fx.add(clique(), T3 + 3.45, 0.9); fx.add(pop(1100, .14), T3 + 3.5, 0.8); fx.add(ding(2093.0, .5), T3 + 3.6, 0.4)  # curtiu
PERG = 'Como eu calculo 20% de 150?'
for i in range(1, len(PERG) + 1):
    tt = T4 + .5 + 1.1 * (i - .5) / len(PERG)
    fx.add(clique(.018), tt, 0.3 + 0.1 * ((i * 7) % 3) / 2, pan=((i * 13) % 5 - 2) * 0.08)
fx.add(whoosh(.22, True, .7), T4 + 1.68); fx.add(pop(880, .1), T4 + 1.72, 0.8)                                   # enviar
fx.add(pop(700, .1), T4 + 2.6, 0.8)
for i in range(5): fx.add(pop(660 * 2 ** ([0, 3, 7, 10, 12][i] / 12), .08), T4 + 2.65 + i * .38, 0.5)
fx.add(ding(1567.98, 1.0), T4 + 4.4, 0.7)                                                                        # marca-texto
for i in range(3): fx.add(pop(900 + i * 150, .1), T4 + 4.7 + i * .2, 0.6)
# E A MELHOR
fx.add(impacto(1.0, .85), 26.5); fx.add(riser(.8), 26.5, 0.85)
for i in range(6): fx.add(clique(.02), 26.62 + i * .035, 0.45)
fx.add(impacto(1.6, 1.1), 27.3); fx.add(ding(1318.5, 1.2), 27.32, 0.7)
# TUDO NUM APP SÓ
fx.add(whoosh(.3, True), 33.2); fx.add(impacto(1.0, .8), 33.35)
fx.add(pop(620, .18), 33.4, 0.8)
for i in range(9): fx.add(clique(.02), 33.55 + i * .035, 0.4)
for k in range(5): fx.add(pop(760 * 2 ** ([0, 2, 4, 7, 12][k] / 12), .12), 33.7 + k * .18, 0.7, pan=(k - 2) * 0.2)
fx.add(ding(1760.0, 1.0), 34.75, 0.6)
# CTA
fx.add(impacto(1.6, 1.1), 35.35); fx.add(impacto(1.0, .8), 35.8)
fx.add(pop(900, .16), 36.3, 0.8); fx.add(ding(1567.98, 1.4), 36.32, 0.9)    # EM BREVE DISPONÍVEL
fx.add(pop(1040, .12), 36.8, 0.6); fx.add(pop(820, .12), 37.2, 0.5)
fx.add(whoosh(.45, True, .9), 38.43)                                          # loop

# ---------------- mixagem (sidechain leve, clima lo-fi)
duck = np.ones(mus.buf.shape[1])
for a, b in CHEIAS:
    tk = a
    while tk < b - 1e-6:
        for off in (0.0, 0.75 + 0.055):
            i = int((tk + off) * SR); n = int(0.18 * SR)
            if i + n < len(duck): duck[i:i + n] = np.minimum(duck[i:i + n], 0.72 + 0.28 * np.linspace(0, 1, n))
        tk += 2.0
mus.buf *= duck
final = Mix(DUR)
final.buf = mus.buf * 1.0 + bat.buf * 0.85 + fx.buf * 0.9
y = final.master(DUR, 0.70)
Mix.salvar(y, sys.argv[1] if len(sys.argv) > 1 else 'soundtrack.wav')
print('trilha ok', y.shape, 'pico', float(np.max(np.abs(y))))
