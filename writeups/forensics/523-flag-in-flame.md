# Flag in Flame

**Catégorie** : Forensics · **Challenge** : #523

## Résolution

`logs.txt` = un PNG en base64. Décodé (896×1152) puis OCR : l'image contient une chaîne **hexadécimale** → `bytes.fromhex()`.

## Flag

```
academy{forensics_analysis_is_amazing_dfc2b4b9}
```

## Ce qu'il faut retenir

Les logs « encodés » cachent souvent une image, et l'image du texte.
