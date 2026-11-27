# 767 — Secure Password Database

**Événement** : picoCTF 2026 · **Catégorie** : Reverse Engineering

## Énoncé

> A new password authentication program that even shows you the password you entered in the
> database. Isn't that cool? Download `system.out` and recover what hash value it is actually
> checking.

Le binaire `system.out` est fourni avec une instance distante qui exécute le même programme.

## Analyse

Premier réflexe sur un binaire inconnu :

```bash
file system.out
# ELF 64-bit LSB pie executable, x86-64, dynamically linked, not stripped
checksec --file=system.out
strings -n 6 system.out | head -40
```

Le binaire est PIE et **non strippé** : les noms de fonctions sont dans la table des symboles, ce
qui rend la lecture directe.

La décompilation de `main()` donne la séquence suivante :

1. `calloc(1, 90)` — un buffer de 90 octets, remis à zéro ;
2. écriture à l'offset 60 de **treize octets codés en dur, XORés avec `0xAA`** ;
3. `fgets` d'un mot de passe, 50 caractères au maximum ;
4. demande d'une longueur, puis réaffichage de ce nombre d'octets **en décimal** ;
5. demande d'une valeur de hash, lue avec `strtoul` ;
6. comparaison du hash calculé et de la valeur saisie.

Le hash est produit par `make_secret()` : la fonction redécode les mêmes treize octets (même XOR
`0xAA`) dans un buffer neuf, écrit un octet nul à l'index 12, puis hache les douze octets ainsi
obtenus.

L'algorithme est un **djb2** :

```c
unsigned long total = 0x1505;          /* 5381 */
for (i = 0; i < 12; i++)
    total = total * 33 + secret[i];    /* unsigned long 64 bits */
return total;
```

`main()` compare cette valeur 64 bits à celle saisie. Deux conséquences pratiques :

- le secret ne dépend que d'octets présents dans le binaire : on peut donc le lire à l'exécution,
  sans réimplémenter l'algorithme ;
- la longueur demandée à l'étape 4 pilote un `printf` sur le buffer : en demandant plus que la
  longueur du mot de passe, on fait afficher la zone où sont stockés les treize octets obfusqués,
  et un XOR `0xAA` suffit à les retrouver. C'est le « password shown in the database » de l'énoncé.

## Solution

1. Ouvrir le binaire dans Ghidra (ou `objdump -d -M intel system.out`) et lire `main()`,
   `make_secret()` et la fonction de hash. Noter l'offset 60 et la constante `0xAA`.

2. Récupérer la valeur attendue à l'exécution plutôt que la recalculer. On casse sur la fonction de
   hash et on lit la valeur de retour :

```bash
gdb ./system.out
(gdb) break hash
(gdb) run
# répondre n'importe quoi aux deux premières questions
# longueur : 1
(gdb) finish
(gdb) print/u $rax
# 15237662580160011234
(gdb) print/x $rax
# 0xd3770d6251b31be2
```

3. Variante sans GDB : demander une longueur supérieure au mot de passe, récupérer la suite de
   valeurs décimales affichée, puis appliquer le XOR :

```python
vals = [ ... ]                 # octets affichés par le programme
secret = bytes(v ^ 0xAA for v in vals)
print(secret[:12])
```

4. Soumettre la valeur à l'instance distante :

```bash
nc <HOST> <PORT>
# mot de passe : n'importe quoi
# longueur : 1
# hash : 15237662580160011234
```

Le programme valide alors le hash et affiche le flag.

## Pièges

- **`$eax` au lieu de `$rax`.** Le hash est un `unsigned long` 64 bits ; lire le registre 32 bits
  tronque la valeur et la vérification échoue. On lit `$rax` avec `print/u` (non signé) pour
  comparer à la valeur décimale demandée par le programme.
- **`finish` dans la mauvaise fonction.** Si le point d'arrêt tombe dans une fonction utilitaire,
  `finish` rend une autre valeur. On vérifie le nom de la fonction avant de poser le `break`.
- **Saisie du hash.** Le programme lit avec `strtoul` : la valeur doit être décimale, sans `0x`, et
  tenir dans un `unsigned long`.
- **Longueur trop grande.** Demander une longueur supérieure à la taille du buffer provoque un
  affichage hors zone ou un plantage : on reste dans les 90 octets alloués.
- **Terminateur.** Le secret haché fait douze octets, l'octet 12 étant forcé à zéro : inclure le
  treizième octet dans un recalcul manuel donne un hash différent.

**Pourquoi ça marche.** Le binaire embarque à la fois le secret obfusqué et l'algorithme de hachage,
et il affiche lui-même une partie de son buffer. Le XOR `0xAA` n'est pas un chiffrement : c'est un
masquage qui tombe dès qu'on lit les octets. La vérification côté client d'un hash calculé à partir
d'une constante du binaire n'apporte aucune sécurité.
