# FindAndOpen

**Catégorie** : Forensics · **Challenge** : #348 · **Résolu le** : 2026-11-23

## Énoncé

> —

## Résolution

Méthode : **pcap -> base64 partiel -> mot de passe zip**.

Le pcap contient des paquets UDP avec du texte et un fragment **base64** : `VGhpcyBpcyB0aGUgc2VjcmV0OiBhY2FkZW15e1IzNERJTkdfTE9LZF8=` qui decode en `This is the secret: academy{R34DING_LOKd_`. Un autre paquet dit "try checking the other file". Ce secret partiel est le **mot de passe** de `flag.zip`, qui contient le flag complet.

## Flag

```
academy{R34DING_LOKd_fil56_succ3ss_48035188}
```

## Ce qu'il faut retenir

Un pcap se lit par flux (`-z follow,tcp,ascii`), pas paquet par paquet.
