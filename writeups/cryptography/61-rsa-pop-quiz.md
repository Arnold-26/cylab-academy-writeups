# rsa-pop-quiz

**Catégorie** : Cryptography · **Challenge** : #61 · **Résolu le** : 2026-11-23

## Énoncé

> Class, take your seats! It's PRIME-time for a quiz...

## Résolution

Méthode : **quiz RSA interactif**.

Service nc qui pose 8 questions RSA. Il faut répondre Y/N puis la valeur : `n = p*q`, `totient = (p-1)(q-1)`, `d = e^-1 mod phi`, `c = m^e mod n`, `m = c^d mod n` (factorisation triviale). Réponses N quand l'énoncé ne donne pas assez d'information (ex: p à partir de n et e seuls). A la fin, le service dit de convertir la dernière réponse en hex puis ASCII.

## Flag

```
academy{wA8_th4t$_ill3aGal..oCFc4DC2a}
```
