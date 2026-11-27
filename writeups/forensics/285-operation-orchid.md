# Operation Orchid

**Catégorie** : Forensics · **Challenge** : #285 · **Résolu le** : 2026-11-23

## Énoncé

> —

## Résolution

Méthode : **sleuthkit + openssl aes256**.

Image disque avec 3 partitions. Dans la 3e (offset 411648), `/root/.ash_history` (inode 1875) revele la commande : `openssl aes256 -salt -in flag.txt -out flag.txt.enc -k unbreakablepassword1234567`. `icat` extrait `flag.txt.enc` (inode 1782) et openssl le dechiffre avec cette cle.

## Flag

```
academy{h4un71ng_p457_0b36d810}
```

## Ce qu'il faut retenir

—
