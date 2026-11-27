# DISKO 1

**Catégorie** : Forensics · **Challenge** : #505

## Énoncé

> Can you find the flag in this disk image?
>
> Download the disk image [here](https://challenge-files.cylabacademy.net/library/dccdae2c264a78f31f0eb8d86c0f8fcbaccf0b0d9e775e97b08da044c05b2277/disko-1.dd.gz).

## Résolution

Image disque gzip : `gunzip` puis `strings` sur le `.dd` — le flag est une chaîne en clair.

## Flag

```
academy{1t5_ju5t_4_5tr1n9_3f5388a2}
```

## Ce qu'il faut retenir

Sur une image disque, `strings` avant tout outil lourd.
