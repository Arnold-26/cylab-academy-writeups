# Rolling My Own

**Catégorie** : Reverse Engineering · **Challenge** : #151 · **Résolu le** : 2026-11-26

## Énoncé

> A password checker that stores no password: the password is hashed and the hash bytes are executed as machine code.

## Résolution

Méthode : **md5 shellcode reversing**.

## Le principe

Le binaire (ELF PIE, 14 472 o) ne compare jamais le mot de passe. Il :

1. lit `Password: ` ;
2. construit un buffer, le decoupe en **chunks de 12 octets**, MD5 chacun ;
3. prend **4 octets a un offset precis de chaque digest** (offsets 8, 2, 7, 1) ;
4. concatene ces 4 tranches -> **16 octets** dans un buffer `mmap` + `mprotect` RWX ;
5. appelle ce buffer comme du code ;
6. si l'appel rend la main, ouvre `flag.txt` et l'affiche.

Un mauvais mot de passe produit des octets aleatoires : le CPU deraille et segfault.

## Le point que les writeups ratent

La description habituelle dit « mot de passe + sel de 8 octets ». C'est faux. En cassant sur
`MD5_Update` et en dumpant les 12 octets hashes :

```
CHUNK0 : 'D' '1' 'v' '1' | G p L a M j E W
CHUNK1 : 'A' 'A' 'A' 'A' | p V O j n n m k
CHUNK2 : 'A' 'A' 'A' 'A' | R G i l e d p 6
CHUNK3 : 'A' 'A' 'A' 'A' | M v c e z l s
```

Le buffer est **4 caracteres du mot de passe + 8 octets constants propres au groupe**, repete :
il y a donc une table de 10 sels de 8 octets, un par groupe de 4 caracteres. Seuls les
**16 premiers caracteres** du mot de passe influencent les 16 octets executes.

Les tranches sont : `chunk0[8:12]`, `chunk1[2:6]`, `chunk2[7:11]`, `chunk3[1:5]`.

## Resolution

Le hint donne le debut du mot de passe (`D1v1`), donc les 4 premiers octets du shellcode sont
fixes :

```
4889fe   mov rsi, rdi
```

Avec `D1v1` + `AAAA`x3, le payload complet est
`48 89 fe 48 74 68 59 ae f3 50 80 4c 58 f8 ee 18`, et le dernier octet `18` precede `ee`
(`out dx, al`, instruction privilegiee) -> crash. Il faut donc chercher les groupes suivants
pour que la concatenation se decode **exactement** jusqu'a l'offset 16 et finisse par un `ret`.

Recherche : 4 caracteres par groupe, alphabet imprimable, avec **capstone** comme oracle
(les instructions peuvent chevaucher les frontieres de groupe : des l'offset 3, `48 xx xx`
consomme deux octets du groupe suivant). Ecarter les instructions privilegiees (`out`, `in`,
`hlt`, `syscall`...) et les sauts, qui quittent le buffer.

Le mot de passe complet est **`D1v1d3AndC0nqu3r`** — 16 caracteres, exactement ce que l'analyse
predisait.

```
$ nc <host> <port>
Password: D1v1d3AndC0nqu3r
academy{r011ing_y0ur_0wn_crypt0_15_h4rd!_13670f39}
```

## A retenir

- Un « sel » n'est pas forcement unique : ici il est **par position**, ce qui fait croire a un
  sel unique quand on ne regarde que le premier chunk.
- Chercher un mot de passe qui rend un hash executable se ramene a un probleme d'**assemblage
  d'instructions**, pas de cryptographie : un desassembleur (capstone) suffit comme oracle.
- Les frontieres de groupe ne sont pas des frontieres d'instruction : le decodage doit etre
  global, depuis l'offset 0.

## Flag

```
academy{r011ing_y0ur_0wn_crypt0_15_h4rd!_13670f39}
```

## Ce qu'il faut retenir

—

## Scripts

- [`_z_151a.py`](../../solve/151/_z_151a.py)
- [`_z_151a.sh`](../../solve/151/_z_151a.sh)
- [`_z_151b.py`](../../solve/151/_z_151b.py)
- [`_z_151b.sh`](../../solve/151/_z_151b.sh)
- [`_z_151c.sh`](../../solve/151/_z_151c.sh)
- [`_z_151d.sh`](../../solve/151/_z_151d.sh)
- [`_z_151e.sh`](../../solve/151/_z_151e.sh)
- [`_z_151f.py`](../../solve/151/_z_151f.py)
- [`_z_151f.sh`](../../solve/151/_z_151f.sh)
- [`_z_151g.sh`](../../solve/151/_z_151g.sh)
- [`_z_151h.sh`](../../solve/151/_z_151h.sh)
- [`_z_151i.sh`](../../solve/151/_z_151i.sh)
- [`_z_151j.sh`](../../solve/151/_z_151j.sh)
- [`_z_151k.sh`](../../solve/151/_z_151k.sh)
- [`_z_151l.py`](../../solve/151/_z_151l.py)
- [`_z_151m.py`](../../solve/151/_z_151m.py)
- [`_z_151n.sh`](../../solve/151/_z_151n.sh)
