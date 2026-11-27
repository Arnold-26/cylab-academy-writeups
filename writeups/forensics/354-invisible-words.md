# Invisible WORDs

**Catégorie** : Forensics · **Challenge** : #354 · **Résolu le** : 2026-11-24

## Énoncé

> Do you recognize this cyberpunk baddie? We don't either. AI art generators are
> all the rage nowadays, which makes it hard to get a reliable known cover image.
> But we know you'll figure it out. The suspect is believed to be trafficking in
> classics. That probably won't help crack the stego, but we hope it will give
> motivation to bring this criminal to justice!
> Download the image [here](https://challenge-files.cylabacademy.net/library/43bb511b308e00a17d1a3e2620926dc364ad802286313809599bc6bb95e178a1/output.bmp)

## Résolution

Méthode : **ZIP cache dans un BMP (2 octets sur 4)**.

Le BMP 960x540 32bpp contient un **ZIP** à l'offset 0x8c, mais chaque groupe de 4 octets n'en garde que 2 (les 2 autres sont du remplissage). On lit `data[i:i+2]` en sautant de 4 en 4 depuis 0x8c jusqu'a tomber sur `\xff\x00`, on écrit le ZIP, on l'ouvre : il contient `ZnJhbmtlbnN0ZWluLXRlc3QudHh0` (= base64 de `frankenstein-test.txt`, le texte de Frankenstein) qui contient le flag.

## Flag

```
academy{w0rd_d4wg_y0u_f0und_5h3113ys_m4573rp13c3_2a058da1}
```

## Scripts

- [`solve.py`](../../solve/354/solve.py)
- *10 variantes intermediaires dans `solve/354/archive/`*
