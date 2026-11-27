# unpackme

**Catégorie** : Reverse Engineering · **Challenge** : #313 · **Résolu le** : 2026-11-23

## Énoncé

> —

## Résolution

Méthode : **UPX + cmp immediat**.

Binaire **UPX** : `upx -d unpackme-upx -o unpacked`. Il demande un nombre ; on trouve `cmp eax,0xb83cb` (754635) dans le desassemblage. Le lancer avec ce nombre donne le flag.

## Flag

```
academy{up><_m3_f7w_266036d7}
```

## Ce qu'il faut retenir

—
