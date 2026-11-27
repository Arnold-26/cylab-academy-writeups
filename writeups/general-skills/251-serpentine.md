# Serpentine

**Catégorie** : Général Skills · **Challenge** : #251 · **Résolu le** : 2026-11-23

## Énoncé

> Find the flag in the Python script!
> [Download Python script](https://challenge-files.cylabacademy.net/library/5cb6e7ec1292ddc3129e08a71c9e79b3cf1aac310ad9656a27b904aac92651cf/serpentine.py)

## Résolution

Méthode : **str_xor avec clé enkidu**.

Le script definit `flag_enc` comme une concaténation de `chr(0x..)`. La fonction `print_flag()` fait `str_xor(flag_enc, 'enkidu')` : XOR caractère par caractère avec la clé répétée. On peut l'evaluer et déchiffrer sans lancer le menu interactif.

## Flag

```
academy{7h3_r04d_l355_7r4v3l3d_f2de26d4}
```
