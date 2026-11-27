# Hidden in plainsight

**Catégorie** : Forensics · **Challenge** : #524

## Résolution

Le commentaire EXIF contient `c3RlZ2hpZGU6…` → base64 → `steghide:cEF6endvcmQ=` → base64 → mot de passe `pAzzword` → `steghide extract` donne le flag.

## Flag

```
academy{h1dd3n_1n_1m4g3_a2158aa5}
```

## Ce qu'il faut retenir

Les métadonnées peuvent porter le *mot de passe* du stégo, pas le flag.
