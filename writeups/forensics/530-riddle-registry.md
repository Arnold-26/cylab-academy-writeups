# Riddle Registry

**Catégorie** : Forensics · **Challenge** : #530 · **Résolu le** : 2026-11-24

## Énoncé

> Hi, intrepid investigator! 📄🔍 You've stumbled upon a peculiar PDF filled with what seems like nothing more than garbled nonsense. But beware! Not everything is as it appears. Amidst the chaos lies a hidden treasure—an elusive flag waiting to be uncovered.
> Find the PDF file here [Hidden Confidential Document](https://challenge-files.cylabacademy.net/library/f1a59c8fe4c030bdcdce963b06148196c62afa61f1e959134cd5b547347fddaf/confidential.pdf) and uncover the flag within the metadata.

## Résolution

Méthode : **metadonnees PDF en base64**.

Le PDF contient des metadonnees dont le champ **Author** est en base64 : `YWNhZGVteXtwdXp6bDNkX20zdGFkYXRhX2YwdW5kIV8zY2M3Y2VhOX0=`. Un decodage donne le flag.

## Flag

```
academy{puzzl3d_m3tadata_f0und!_3cc7cea9}
```

## Scripts

- [`solve.py`](../../solve/530/solve.py)
