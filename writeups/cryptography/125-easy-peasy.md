# Easy Peasy

**Catégorie** : Cryptography · **Challenge** : #125 · **Résolu le** : 2026-11-23

## Énoncé

> A one-time pad is unbreakable, but can you manage to recover the flag? (Wrap with academy{})

## Résolution

Méthode : **OTP a compteur : retour a zero du keystream**.

`otp.py` utilise une clé de 50000 octets et un compteur `key_location`. Après le flag (32 octets), le compteur demarre a 32. En envoyant **49968 octets** on force `stop = 50000` -> `stop % KEY_LEN = 0` : le compteur revient a zero. La requête suivante réutilise donc `kf[0:32]`, la portion qui a chiffre le flag. On chiffre un texte connu et on XOR. Vérification par ancrage : envoyer 8 octets, retrouver ce keystream dans une fenetre de 50000 octets confirme le décalage exact.

## Flag

```
academy{5d2ed61216151a1c485ee5b4651c64cf}
```
