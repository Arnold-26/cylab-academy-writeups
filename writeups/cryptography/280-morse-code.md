# morse-code

**Catégorie** : Cryptography · **Challenge** : #280 · **Résolu le** : 2026-11-23

## Énoncé

> Morse code is well known. Can you decrypt this?
> Download the file [here](https://challenge-files.cylabacademy.net/library/3728bfa4e8314fddd6b7e9f3fae9cb453b459a0bd4b3a29a9224701152f0cd89/morse_chal.wav).
>
> Wrap your answer with academy{}, put underscores in place of pauses, and use all uppercase.

## Résolution

Méthode : **morse audio (enveloppe d'energie)**.

Le fichier est un WAV de 28,9 s. `multimon-ng -a MORSE_CW` donne un resultat bruite ; un decodeur maison (RMS par fenetre de 5 ms, seuil a 15% du max, durees normalisees) donne `WH47 H47H 90D W20U9H7`, du leetspeak pour "WHAT HATH GOD WROUGHT".

## Flag

```
academy{wh47_h47h_90d_w20u9h7}
```
