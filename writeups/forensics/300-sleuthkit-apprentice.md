# Sleuthkit Apprentice

**Catégorie** : Forensics · **Challenge** : #300 · **Résolu le** : 2026-11-23

## Énoncé

> Download this disk image and find the flag.
>
> Note: if you are using the webshell, download and extract the disk image into
> `/tmp` not your home directory.
> - [Download compressed disk image](https://challenge-files.cylabacademy.net/library/699d021acdedf3ce7c6944b6f3e16046a82b3a1f7ee2e79716132292ce4adbbd/disk.flag.img.gz)

## Résolution

Méthode : **icat sur inode UTF-16**.

L'image contient deux partitions Linux. Dans la seconde (offset 360448), `fls -r` révèle `my_folder/flag.uni.txt`. Le fichier est encodé en **UTF-16 LE**, d'ou les octets nuls entre les caractères ; `icat` le restitue directement.

## Flag

```
academy{by73_5urf3r_6395be48}
```

## Scripts

- [`solve.py`](../../solve/300/solve.py)
