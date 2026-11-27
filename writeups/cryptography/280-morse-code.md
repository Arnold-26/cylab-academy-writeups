# morse-code

**Catégorie** : Cryptography · **Challenge** : #280 · **Résolu le** : 2026-11-23

## Énoncé

> —

## Résolution

Méthode : **morse audio (enveloppe d'energie)**.

Le fichier est un WAV de 28,9 s. `multimon-ng -a MORSE_CW` donne un resultat bruite ; un decodeur maison (RMS par fenetre de 5 ms, seuil a 15% du max, durees normalisees) donne `WH47 H47H 90D W20U9H7`, du leetspeak pour "WHAT HATH GOD WROUGHT".

## Flag

```
academy{wh47_h47h_90d_w20u9h7}
```

## Ce qu'il faut retenir

—
