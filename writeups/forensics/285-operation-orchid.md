# Opération Orchid

**Catégorie** : Forensics · **Challenge** : #285 · **Résolu le** : 2026-11-23

## Énoncé

> Download this disk image and find the flag.
>
> Note: if you are using the webshell, download and extract the disk image into
> `/tmp` not your home directory.
> - [Download compressed disk image](https://challenge-files.cylabacademy.net/library/bb0cb9b59f754a578fdcff72400d49394fe4399b5bf0d34f650c5baffbad8575/disk.flag.img.gz)

## Résolution

Méthode : **sleuthkit + openssl aes256**.

Image disque avec 3 partitions. Dans la 3e (offset 411648), `/root/.ash_history` (inode 1875) révèle la commande : `openssl aes256 -salt -in flag.txt -out flag.txt.enc -k unbreakablepassword1234567`. `icat` extrait `flag.txt.enc` (inode 1782) et openssl le déchiffre avec cette clé.

## Flag

```
academy{h4un71ng_p457_0b36d810}
```
