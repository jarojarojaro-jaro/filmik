# GENESIS — 7 sekund powstania świata, wyłącznie kodem

`genesis.mp4` (1080p60, stereo) — zero assetów: obraz to jeden fragment shader, dźwięk to syntezator w czystym Pythonie.

| czas | scena |
|---|---|
| 0–1 s | osobliwość: materia spada do środka, puls przyspiesza, cisza |
| 1 s | Wielki Wybuch: błysk, chromatyczna fala uderzeniowa, drżenie kamery |
| 1.2–4.5 s | lot przez pierwotną mgławicę, w gazie zapalają się gwiazdy |
| 3.5–5.6 s | rotacja różnicowa zwija gaz w galaktykę spiralną, nurkujemy w jądro |
| 5.2–7 s | stygnąca, lawowa planeta i jej pierwszy wschód słońca — GENESIS |

- `index.html` — shader WebGL2 (otwórz w przeglądarce, gra na żywo w pętli)
- `audio.py` — ścieżka dźwiękowa → `audio.wav`
- `render.mjs` — render klatka po klatce (Playwright) → ffmpeg → `genesis.mp4`

```sh
python3 audio.py && FFMPEG=ffmpeg node render.mjs
```
