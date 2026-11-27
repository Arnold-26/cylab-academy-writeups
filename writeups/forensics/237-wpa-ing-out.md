# WPA-ing Out

**Catégorie** : Forensics · **Challenge** : #237

## Résolution

`aircrack-ng -w rockyou.txt wpa-ing_out.pcap` : le handshake craque avec `mickeymouse`.

## Flag

```
academy{mickeymouse}
```

## Ce qu'il faut retenir

Un pcap 802.11 + rockyou se craque en quelques secondes si le mot de passe est faible.
