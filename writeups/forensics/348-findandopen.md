# FindAndOpen

**Catégorie** : Forensics · **Challenge** : #348 · **Résolu le** : 2026-11-23

## Énoncé

> Someone might have hidden the password in the trace file.
> Find the key to unlock [this file](https://challenge-files.cylabacademy.net/library/db0ed8ae315a98a99df76de2bc96c527f6cb36c0ab7497bf10e951576343d560/flag.zip). [This tracefile](https://challenge-files.cylabacademy.net/library/db0ed8ae315a98a99df76de2bc96c527f6cb36c0ab7497bf10e951576343d560/dump.pcap) might be good to analyze.

## Résolution

Méthode : **pcap -> base64 partiel -> mot de passe zip**.

Le pcap contient des paquets UDP avec du texte et un fragment **base64** : `VGhpcyBpcyB0aGUgc2VjcmV0OiBhY2FkZW15e1IzNERJTkdfTE9LZF8=` qui decode en `This is the secret: academy{R34DING_LOKd_`. Un autre paquet dit "try checking the other file". Ce secret partiel est le **mot de passe** de `flag.zip`, qui contient le flag complet.

## Flag

```
academy{R34DING_LOKd_fil56_succ3ss_48035188}
```

## Ce qu'il faut retenir

Un pcap se lit par flux (`-z follow,tcp,ascii`), pas paquet par paquet.
