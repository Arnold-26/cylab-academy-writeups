# Flag in Flame

**Catégorie** : Forensics · **Challenge** : #523

## Énoncé

> The SOC team discovered a suspiciously large log file after a recent breach. When they opened it, they found an enormous block of encoded text instead of typical logs. Could there be something hidden within? Your mission is to inspect the resulting file and reveal the real purpose of it. The team is relying on your skills to uncover any concealed information within this unusual log.
> Download the encoded data here: [Logs Data](https://challenge-files.cylabacademy.net/library/8389f7eb8ae95fd4453f1e2d27498905b415efec5fc738bfd0983d56c09959bf/logs.txt). Be prepared—the file is large, and examining it thoroughly is crucial .

## Résolution

`logs.txt` = un PNG en base64. Décodé (896×1152) puis OCR : l'image contient une chaîne **hexadécimale** → `bytes.fromhex()`.

## Flag

```
academy{forensics_analysis_is_amazing_dfc2b4b9}
```

## Ce qu'il faut retenir

Les logs « encodés » cachent souvent une image, et l'image du texte.
