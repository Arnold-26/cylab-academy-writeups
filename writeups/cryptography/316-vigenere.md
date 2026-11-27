# Vigenere

**Catégorie** : Cryptography · **Challenge** : #316 · **Résolu le** : 2026-11-23

## Énoncé

> Can you decrypt this message?
> Decrypt this [message](https://challenge-files.cylabacademy.net/library/848831bc0df5e68fe8f320c91c47f635bce35a7c8236c696f9478bfaf39cfd10/cipher.txt) using this key "CYLAB".

## Résolution

Méthode : **vigenere clé CYLAB**.

Le fichier `cipher.txt` contient `caldfow{...}` et l'énoncé donne la clé **CYLAB**. Déchiffrement de Vigenere : `p = (c - k) mod 26` sur les lettres seulement, la clé se répète en ignorant la ponctuation.

## Flag

```
academy{D0NT_US3_V1G3N3R3_C1PH3R_42ccuf9c}
```
