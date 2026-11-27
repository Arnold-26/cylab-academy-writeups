# Timestamped Secrets

**Catégorie** : Cryptography · **Challenge** : #722 · **Résolu le** : 2026-11-23

## Énoncé

> Someone encrypted a message using AES in ECB mode but they weren’t very careful with their key. Turns out it’s derived from something as simple as the current time!
> Can you uncover the key and decrypt the flag?
> Download the encrypted message: [message](https://challenge-files.cylabacademy.net/library/19f6ce60f219eddc3613ac4b301bea75a863ddca9e9230c50c8d72fe36ce2a21/message.txt)
> You may also find the encryption script helpful: [code](https://challenge-files.cylabacademy.net/library/19f6ce60f219eddc3613ac4b301bea75a863ddca9e9230c50c8d72fe36ce2a21/encryption.py)

## Résolution

Méthode : **bruteforce du timestamp**.

La clé AES est `sha256(str(int(time.time())))[:16]` et l'énoncé donne un timestamp approximatif. En balayant les timestamps autour de la valeur indiquee, celui qui donne un clair commencant par `academy{` est le bon (ici delta = 0).

## Flag

```
academy{sa3S_sEc9t_99162e4b}
```
