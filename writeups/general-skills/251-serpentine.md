# Serpentine

**Catégorie** : General Skills · **Challenge** : #251 · **Résolu le** : 2026-11-23

## Résolution

Méthode : **str_xor avec cle enkidu**.

Le script definit `flag_enc` comme une concatenation de `chr(0x..)`. La fonction `print_flag()` fait `str_xor(flag_enc, 'enkidu')` : XOR caractere par caractere avec la cle repetee. On peut l'evaluer et dechiffrer sans lancer le menu interactif.

## Flag

```
academy{7h3_r04d_l355_7r4v3l3d_f2de26d4}
```
