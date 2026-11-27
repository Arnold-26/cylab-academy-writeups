# WPA-ing Out

**Catégorie** : Forensics · **Challenge** : #237

## Énoncé

> I thought that my password was super-secret, but it turns out that passwords passed over the AIR can be CRACKED, especially if I used the same wireless network password as one in the rockyou.txt credential dump.
> Use this '[pcap file](https://challenge-files.cylabacademy.net/library/14d2e2f2da78ce901cceaff734ed2bca4555097ceb52f486e7836a799b411adc/wpa-ing_out.pcap)' and the rockyou wordlist. The flag should be entered in the academy{XXXXXX} format.

## Résolution

`aircrack-ng -w rockyou.txt wpa-ing_out.pcap` : le handshake craque avec `mickeymouse`.

## Flag

```
academy{mickeymouse}
```

## Ce qu'il faut retenir

Un pcap 802.11 + rockyou se craque en quelques secondes si le mot de passe est faible.
