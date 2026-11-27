# Disk, disk, sleuth! II

**Catégorie** : Forensics · **Challenge** : #137 · **Résolu le** : 2026-11-23

## Énoncé

> All we know is the file with the flag is named `down-at-the-bottom.txt`...
> [dds2-alpine.flag.img.gz](https://challenge-files.cylabacademy.net/library/37cc81e16bbabfa27473e55596d81db602310fb47340473d9e94d74cd3dc1761/dds2-alpine.flag.img.gz)

## Résolution

Méthode : **fls + icat**.

Image disque (134 Mo) avec une table MBR, partition à l'offset **2048**. `fls -r -o 2048` liste les fichiers, dont `root/down-at-the-bottom.txt` (inode 18291). `icat -o 2048 img 18291` l'affiche : le flag y est dessine en ASCII art.

## Flag

```
academy{f0r3ns1c4t0r_n0v1c3_95c645ad}
```

## Ce qu'il faut retenir

Sur une image disque, `mmls` puis `fls` listent les fichiers sans monter l'image.
