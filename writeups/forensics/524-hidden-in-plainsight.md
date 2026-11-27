# Hidden in plainsight

**Catégorie** : Forensics · **Challenge** : #524

## Énoncé

> You’re given a seemingly ordinary JPG image. Something is tucked away out of sight inside the file. Your task is to discover the hidden payload and extract the flag.
> Download the jpg image [here](https://challenge-files.cylabacademy.net/library/714093cf55b6f82d117c53a2a1d44f4956e0ccc7655b1fe2efee99e12b314f53/img.jpg).

## Résolution

Le commentaire EXIF contient `c3RlZ2hpZGU6…` → base64 → `steghide:cEF6endvcmQ=` → base64 → mot de passe `pAzzword` → `steghide extract` donne le flag.

## Flag

```
academy{h1dd3n_1n_1m4g3_a2158aa5}
```

## Ce qu'il faut retenir

Les métadonnées peuvent porter le *mot de passe* du stégo, pas le flag.
