# Play Nice

**Catégorie** : Cryptography · **Challenge** : #114 · **Résolu le** : 2026-11-25

## Énoncé

> nc chatelaine.cylabacademy.net <port>

## Résolution

Méthode : **chiffre de Playfair 6x6 : dechiffrement avec la cle publiee en clair**.

Le service imprime en clair l'**alphabet** (36 caracteres, carre 6x6) qui sert de cle, puis le **message chiffre**, et demande le clair. Le code `playfair.py` fourni montre l'algorithme exact : carre 6x6 construit dans l'ordre de l'alphabet, et `encrypt_pair` decale de +1 en ligne si meme ligne, de +1 en colonne si meme colonne, sinon echange les colonnes. Le dechiffrement est donc le meme algorithme avec **-1** a la place de +1 (et l'echange de colonnes inchange). Detail utile : si la longueur du message est impaire, le chiffrement ajoute `{` en fin de texte — il faut donc retirer ce caractere du clair reconstruit avant de repondre. Le service repond « Congratulations! Here's the flag: ... » avec un flag **sans format standard** (une simple chaine hexadecimale), conformement a l'enonce.

## Flag

```
8fc275985377ab6a0d9aa40eeaa7dd29
```

## Ce qu'il faut retenir

—
