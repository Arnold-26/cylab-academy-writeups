# rotation

**Catégorie** : Cryptography · **Challenge** : #373 · **Résolu le** : 2026-11-23

## Énoncé

> You will find the flag after decrypting this file
> Download the encrypted flag [here](https://challenge-files.cylabacademy.net/library/87b38d23d72ad6f1aa572b3fb1ba217ddb7476a432e8810b51a3ff40caad8ac1/encrypted.txt).

## Résolution

Méthode : **rot13**.

Le fichier contient `ikilmug{z0bib1wv_l3kzgxb3l_69m10560}` : un ROT13. `tr 'A-Za-z' 'N-ZA-Mn-za-m'` ou `codecs.decode(s,'rot13')`.

## Flag

```
academy{r0tat1on_d3crypt3d_69e10560}
```
