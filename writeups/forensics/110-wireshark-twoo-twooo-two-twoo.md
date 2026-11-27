# Wireshark twoo twooo two twoo...

**Catégorie** : Forensics · **Challenge** : #110 · **Résolu le** : 2026-11-23

## Énoncé

> Can you find the flag?
> [shark2.pcapng](https://challenge-files.cylabacademy.net/library/539e234c40631ade42eca2ae91c7a24a8f1b7165b6f6ef60d2dc8c15415ae096/shark2.pcapng)

## Résolution

Méthode : **exfiltration DNS base64**.

Le pcap contient une **exfiltration DNS** : chaque requête vers `<base64>.reddshrimpandherring.com` transporte un fragment du flag. En ne gardant que les fragments dont le decodage est du texte propre et en les remettant dans l'ordre des frames, on obtient le flag. Les réponses HTTP `/flag` sont des leurres.

## Flag

```
academy{dns_3xf1l_ftw_deadbeef}
```
