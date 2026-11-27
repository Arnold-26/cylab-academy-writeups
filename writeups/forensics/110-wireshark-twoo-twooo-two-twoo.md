# Wireshark twoo twooo two twoo...

**Catégorie** : Forensics · **Challenge** : #110 · **Résolu le** : 2026-11-23

## Résolution

Méthode : **exfiltration DNS base64**.

Le pcap contient une **exfiltration DNS** : chaque requete vers `<base64>.reddshrimpandherring.com` transporte un fragment du flag. En ne gardant que les fragments dont le decodage est du texte propre et en les remettant dans l'ordre des frames, on obtient le flag. Les reponses HTTP `/flag` sont des leurres.

## Flag

```
academy{dns_3xf1l_ftw_deadbeef}
```
