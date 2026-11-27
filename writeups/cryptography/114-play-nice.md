# Play Nice

**Catégorie** : Cryptography · **Challenge** : #114 · **Résolu le** : 2026-11-25

## Énoncé

> nc chatelaine.cylabacademy.net <port>

## Résolution

Méthode : **chiffre de Playfair 6x6 : déchiffrement avec la clé publiée en clair**.

Le service imprime en clair l'**alphabet** (36 caractères, carré 6x6) qui sert de clé, puis le **message chiffre**, et demande le clair. Le code `playfair.py` fourni montre l'algorithme exact : carré 6x6 construit dans l'ordre de l'alphabet, et `encrypt_pair` décale de +1 en ligne si même ligne, de +1 en colonne si même colonne, sinon échange les colonnes. Le déchiffrement est donc le même algorithme avec **-1** à la place de +1 (et l'échange de colonnes inchangé). Détail utile : si la longueur du message est impaire, le chiffrement ajoute `{` en fin de texte — il faut donc retirer ce caractère du clair reconstruit avant de répondre. Le service répond « Congratulations! Here's the flag: ... » avec un flag **sans format standard** (une simple chaîne hexadécimale), conformément à l'énoncé.

## Flag

```
8fc275985377ab6a0d9aa40eeaa7dd29
```

## Scripts

- [`solve.py`](../../solve/114/solve.py)
- *1 variantes intermediaires dans `solve/114/archive/`*
