# Surfing the Waves

**Catégorie** : Forensics · **Challenge** : #117 · **Résolu le** : 2026-11-25

## Énoncé

> main.wav (2736 echantillons, 2736 Hz)

## Résolution

Méthode : **hexadécimal encode dans les échantillons audio (2 derniers chiffres = bruit)**.

`main.wav` fait **1 seconde, mono, 2736 Hz, 2736 échantillons**, avec des valeurs comprises entre 1000 et 8509. Le spectrogramme ne montre aucun texte : la donnée n'est pas dans le domaine frequentiel. La clé est dans les **valeurs des échantillons** : en tronquant les **deux derniers chiffres** de chaque valeur (qui sont du bruit aléatoire ajoute), il ne reste que **16 valeurs uniques** — 10, 15, 20, ... 85 — soit exactement un alphabet hexadécimal de 16 symboles. En les triant et en les faisant correspondre à `0123456789abcdef` (10->0, 15->1, ... 85->f), on obtient une longue chaîne hexadécimale qui se decode en ASCII comme un **programme Python générateur** : `hex_stuff[i] = 1000 + int(hex_stuff[i]) * 500 + (10 * random())` — ce qui explique parfaitement les valeurs observees (1000 + 500*n + bruit) et confirme la theorie. Le programme se termine par le drapeau en commentaire. Vérification croisee : 1000 + 500*0 = 1000 et 1000 + 500*15 = 8500, coherents avec min=1000 et max=8509.

## Flag

```
academy{mU21C_1s_1337_63f2299a}
```

## Scripts

- [`solve.py`](../../solve/117/solve.py)
- *5 variantes intermediaires dans `solve/117/archive/`*
