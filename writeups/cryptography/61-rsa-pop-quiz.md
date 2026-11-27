# rsa-pop-quiz

**Catégorie** : Cryptography · **Challenge** : #61 · **Résolu le** : 2026-11-23

## Résolution

Méthode : **quiz RSA interactif**.

Service nc qui pose 8 questions RSA. Il faut repondre Y/N puis la valeur : `n = p*q`, `totient = (p-1)(q-1)`, `d = e^-1 mod phi`, `c = m^e mod n`, `m = c^d mod n` (factorisation triviale). Reponses N quand l'enonce ne donne pas assez d'information (ex: p a partir de n et e seuls). A la fin, le service dit de convertir la derniere reponse en hex puis ASCII.

## Flag

```
academy{wA8_th4t$_ill3aGal..oCFc4DC2a}
```
