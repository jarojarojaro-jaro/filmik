# Pure-code soundtrack synced to index.html timeline -> audio.wav
import math, random, wave, struct
SR, D = 44100, 7
N, TAU, rnd = SR * D, 2 * math.pi, random.Random(7).random
S = lambda a, b, x: (lambda k: k * k * (3 - 2 * k))(min(max((x - a) / (b - a), 0), 1))
chord = [73.42, 110, 146.83, 220, 293.66, 369.99, 440, 659.25]   # D major add9, spread
bell = [880, 1174.66, 1760]
ch = ([], [])
for c, det in enumerate((-.0025, .0025)):
    p0 = p1 = p2 = l1 = l2 = l3 = 0.
    for i in range(N):
        t = i / SR; e = t - 1; E = max(e, 0); w = rnd() * 2 - 1; s = 0.
        l1 += (w - l1) * .05; l2 += (w - l2) * .008
        l3 += (w - l3) * (.015 + .06 * (.5 + .5 * math.sin(E * 2.3 + c)))
        if e < 0:   # singularity: accelerating heartbeat, rising drone, choked swell
            g = 1 - S(.9, .97, t)
            p0 += (38 + 30 * t * t) / SR
            s += math.sin(TAU * 48 * t) * max(math.sin(t * t * 30), 0) ** 16 * .9 * g
            s += (math.sin(TAU * p0) + .3 * math.sin(TAU * 2 * p0)) * .3 * t * t * g
            s += (w - l1) * t ** 5 * .35 * g
        else:       # big bang: crack, sub drop, rumble
            p1 += (26 + 90 * math.exp(-E * 5)) / SR
            s += math.sin(TAU * p1) * math.exp(-E * 1.1) * 1.1
            s += w * math.exp(-E * 30) + l2 * 9 * math.exp(-E * .8)
            s += l3 * 3 * S(.2, 1, E) * (1 - S(2.6, 3.6, E))                         # nebula wind
            s += (w - l1) * S(3.1, 4.3, E) ** 3 * (1 - S(4.3, 4.4, E)) * .45          # riser into the core
            s += math.sin(TAU * p2) * .12 * S(2.4, 3.2, E) * (1 - S(4.1, 4.4, E)) * (.6 + .4 * math.sin(E * 25))
            p2 += (180 + 260 * S(2.5, 4.3, E)) / SR                                    # swirl gliss
            if E > 4.3:
                q = E - 4.3
                s += math.sin(TAU * 42 * q) * math.exp(-q * 3) * .7                    # arrival thump
                s += sum(math.sin(TAU * f * (1 + det) * t) for f in chord) * .09 * S(0, 1.1, q)
                s += sum(math.sin(TAU * f * (1 - det) * t) * math.exp(-(q - .8) * 1.5 * (k + 1))
                         for k, f in enumerate(bell)) * .1 * S(.75, .85, q)            # sunrise shimmer
        ch[c].append(s * (1 - S(6.75, 7, t)))

def reverb(x, o):  # Schroeder: 4 combs + 2 allpasses
    y = [0.] * len(x)
    for d in (1557 + o, 1617 + o, 1491 + o, 1422 + o):
        b = [0.] * d
        for i, v in enumerate(x):
            j = i % d; r = b[j]; b[j] = v + r * .84; y[i] += r * .25
    for d in (225, 556):
        b = [0.] * d
        for i, v in enumerate(y):
            j = i % d; r = b[j]; b[j] = v + r * .5; y[i] = r - v * .5
    return [a + .3 * b for a, b in zip(x, y)]

L, R = reverb(ch[0], 0), reverb(ch[1], 23)
pk = max(map(abs, L + R))
with wave.open('audio.wav', 'wb') as f:
    f.setnchannels(2); f.setsampwidth(2); f.setframerate(SR)
    f.writeframes(b''.join(struct.pack('<hh', int(32767 * math.tanh(1.3 * a / pk) * .95),
                                       int(32767 * math.tanh(1.3 * b / pk) * .95)) for a, b in zip(L, R)))
