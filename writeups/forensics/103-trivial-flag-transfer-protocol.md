# Trivial Flag Transfer Protocol

**Catégorie** : Forensics · **Challenge** : #103 · **Résolu le** : 2026-11-23

## Résolution

Méthode : **export TFTP + ROT13 + steghide**.

Le pcap contient du **TFTP**. `tshark --export-objects tftp` sort `plan`, `program.deb` (steghide) et trois BMP. `plan` est en **ROT13** : "I USED THE PROGRAM AND HID IT WITH-DUEDILIGENCE". `steghide extract -sf picture3.bmp -p DUEDILIGENCE` donne le flag. Piege : le pcap fait 52 Mo, un telechargement tronque a 14 Mo ne contient pas picture2/3.

## Flag

```
academy{h1dd3n_1n_pLa1n_51GHT_18375919}
```
