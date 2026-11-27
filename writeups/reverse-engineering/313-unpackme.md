# unpackme

**Catégorie** : Reverse Engineering · **Challenge** : #313 · **Résolu le** : 2026-11-23

## Énoncé

> Can you get the flag?
> Reverse engineer this [binary](https://challenge-files.cylabacademy.net/library/1866752fd42f8e5c56036336e3260fc55ecc5a7e2b64539dd0bf48889eb9b03c/unpackme-upx).

## Résolution

Méthode : **UPX + cmp immediat**.

Binaire **UPX** : `upx -d unpackme-upx -o unpacked`. Il demande un nombre ; on trouve `cmp eax,0xb83cb` (754635) dans le desassemblage. Le lancer avec ce nombre donne le flag.

## Flag

```
academy{up><_m3_f7w_266036d7}
```
