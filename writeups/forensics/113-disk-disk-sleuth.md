# Disk, disk, sleuth!

**Catégorie** : Forensics · **Challenge** : #113 · **Résolu le** : 2026-11-23

## Énoncé

> Use `srch_strings` from the sleuthkit and some terminal-fu to find a flag in this disk image.
<a href='https://challenge-files.cylabacademy.net/library/4d6e776c4f09366b282fa45c00b74c0e348309a34f636fd6a9e4e0ee50e7345b/dds1-alpine.flag.img.gz' download>dds1-alpine.flag.img.gz</a>

## Résolution

Méthode : **strings**.

## Flag

```
academy{f0r3ns1c4t0r_n30phyt3_6502313d}
```

## Ce qu'il faut retenir

`strings` est souvent suffisant : le flag est en clair dans le binaire.
