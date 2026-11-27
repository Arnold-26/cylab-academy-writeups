# 767 — Secure Password Database

**Événement** : picoCTF 2026 · **Catégorie** : Reverse Engineering

> Synthèse rédigée à partir des sources publiques listées en fin de fiche : ce challenge a été
> résolu côté CyLab Academy, mais le writeup d'origine n'a pas été conservé.

## Énoncé

> A new password authentication program that even shows you the password you entered in the
> database. Isn't that cool? Download `system.out` and recover what hash value it is actually
> checking.

Le binaire `system.out` (ELF 64 bits PIE, non strippé) et une instance distante sont fournis.

## Analyse

Le programme alloue un buffer de 90 octets (`calloc`), y écrit à l'offset 60 treize octets codés en
dur XORés avec `0xAA`, demande un mot de passe (`fgets`, 50 caractères max), demande sa longueur,
réaffiche ce nombre d'octets en décimal, puis demande la valeur de hash (`strtoul`). La fonction
`make_secret()` redécode les mêmes octets dans un buffer neuf, les termine à l'index 12 et les
hache. Le hash est un **djb2** : `total = 0x1505` (5381) puis `total = total * 33 + octet` pour
chaque octet, en `unsigned long` 64 bits. `main()` compare ce résultat 64 bits à la valeur saisie.
Comme le hash ne dépend que d'octets présents dans le binaire, on peut le lire à l'exécution plutôt
que réimplémenter l'algorithme.

## Solution

1. Décompiler `system.out` (Ghidra) et lire `main()`, `make_secret()` et la fonction de hash.
2. Récupérer la valeur attendue sous GDB en cassant sur la fonction de hash :

```bash
gdb ./system.out
(gdb) break hash
(gdb) run
# répondre n'importe quoi aux deux questions
(gdb) finish
(gdb) print/u $rax     # 15237662580160011234  (0xd3770d6251b31be2)
```

Lire `$eax` au lieu de `$rax` tronque la valeur et fait échouer la vérification.
3. Soumettre cette valeur à l'instance : le programme valide le hash et affiche le flag.

```bash
nc <HOST> <PORT>
# mot de passe : n'importe quoi
# longueur : 1
# hash : 15237662580160011234
```

## Flag

```
picoCTF{d0nt_trust_...}
```

Préfixe publié par picoCTF Solutions, qui indique en plus que le flag est **identique pour toutes
les instances** mais n'en affiche qu'une forme abrégée ; le suffixe n'est donc pas recopié ici, flag
complet non conservé.

## Sources

- [picoCTF Solutions — Secure Password Database (picoCTF 2026)](https://picoctfsolutions.com/picoctf-2026-secure-password-database)
- [far17sya/picoCTF-2026-Writeups — reverse-engineering/secure-password-database](https://github.com/far17sya/picoCTF-2026-Writeups/blob/main/reverse-engineering/secure-password-database/README.md)
- [snwau/picoCTF-2026-Writeup — Reverse Engineering/Secure Password Database](https://github.com/snwau/picoCTF-2026-Writeup/blob/main/Reverse%20Engineering/Secure%20Password%20Database/Secure%20Password%20Database.md)
