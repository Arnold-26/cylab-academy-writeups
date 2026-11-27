# It is my Birthday 2

**Catégorie** : Cryptography · **Challenge** : #169 · **Résolu le** : 2026-11-25

## Énoncé

> invite.pdf + shattered-1/2.pdf (shattered.io)

## Résolution

Méthode : **collision SHA-1 a préfixe fixe + suffixe impose de 1000 octets**.

L'énoncé demande d'uploader **deux PDF valides, differents, mais de même SHA-1**, dont les **1000 derniers octets** sont identiques a ceux d'un `invite.pdf` fourni. Premier faux diagnostic : j'ai d'abord tente une collision **MD5** (paire `poeMD5_A/B.pdf` de corkami/collisions, vérifiée : même MD5 `b347b04f...`, contenus differents) — le service a repondu « You are not invited! ». Le writeup precise qu'il s'agit de **SHA-1** : le challenge repose sur SHAttered (Stevens et al.), première collision SHA-1 pratique entre deux PDF. Méthode : (1) récupérer `shattered-1.pdf` et `shattered-2.pdf` sur shattered.io (422 435 octets chacun, SHA-1 identique `38762cf7f55934b3...`, contenus differents — collision a préfixe fixe, donc tout suffixe commun conserve l'égalité des hashes) ; (2) récupérer l'`invite.pdf` (2 247 830 octets) ; (3) **concaténer a chacun des deux shattered les 1000 derniers octets de l'invite**. Resultat vérifie : SHA-1 `133f99dc4ac356ad...` identique pour les deux fichiers, contenus differents, et les 1000 derniers octets correspondent bien à l'invite (SHA-1 de la queue : `9bc110fe8b6b5561...`). L'upload renvoie alors le flag. Points clés : ne pas confondre MD5 et SHA-1 (le nom « Birthday » evoque la collision, pas l'algorithme) ; et la propriété de collision a préfixe fixe est ce qui permet d'ajouter un suffixe impose sans casser la collision.

## Flag

```
academy{h4ppy_b1rthd4y_2_m3_8248ffdd}
```

## Scripts

- [`solve.py`](../../solve/169/solve.py)
- *10 variantes intermediaires dans `solve/169/archive/`*
