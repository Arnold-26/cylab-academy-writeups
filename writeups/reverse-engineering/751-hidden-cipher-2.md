# 751 — Hidden Cipher 2

**Événement** : picoCTF 2026 · **Catégorie** : Reverse Engineering

> Synthèse rédigée à partir des sources publiques listées en fin de fiche : ce challenge a été
> résolu côté CyLab Academy, mais le writeup d'origine n'a pas été conservé.

## Énoncé

> The flag is right in front of you, kind of. You just need to solve a basic math problem to see it.
> To get the real flag, you'll have to understand how that math answer is used.

L'archive `hiddencipher2.zip` contient le binaire ; le service pose d'abord un calcul.

## Analyse

Le serveur demande de résoudre une opération simple (par exemple « What is 3 - 2? »), puis renvoie
le flag sous forme d'un tableau d'entiers bien plus grands que des valeurs ASCII. La fonction
`encode_flag()` du binaire multiplie chaque valeur ASCII du flag par la réponse au calcul : le
« chiffrement » est donc une simple mise à l'échelle, dont l'inverse est la division entière. Le
secret repose uniquement sur l'ignorance de l'algorithme (sécurité par obscurité) : la
décompilation le révèle en quelques secondes.

## Solution

1. Se connecter et répondre correctement au calcul :

```bash
nc <HOST> <PORT>
```

2. Ouvrir le binaire dans Ghidra et lire `encode_flag()` pour confirmer la multiplication des codes
   ASCII par la réponse.
3. Inverser par division entière :

```python
answer = 3                      # la réponse au calcul posé
encoded = [336, 315, 297, ...]  # le tableau renvoyé par le serveur
print("".join(chr(n // answer) for n in encoded))
```

Si la réponse vaut 1, les nombres sont directement les codes ASCII.

## Flag

```
picoCTF{m4th_b3h1nd_c1ph3r_...}
```

Préfixe publié par picoCTF Solutions (suffixe masqué à la source) : le flag complet n'est pas
recopié ici.

## Sources

- [picoCTF Solutions — Hidden Cipher 2 (picoCTF 2026)](https://picoctfsolutions.com/picoctf-2026-hidden-cipher-2)
- [snwau/picoCTF-2026-Writeup — Reverse Engineering/Hidden Cipher 2](https://github.com/snwau/picoCTF-2026-Writeup/blob/main/Reverse%20Engineering/Hidden%20Cipher%202/Hidden%20Cipher%202.md)
