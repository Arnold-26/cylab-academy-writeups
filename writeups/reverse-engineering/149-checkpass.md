# Checkpass

**Catégorie** : Reverse Engineering · **Challenge** : #149 · **Résolu le** : 2026-11-25

## Énoncé

> What is the password? Flag format: academy{...}

## Résolution

Méthode : **spn inversion**.

Binaire **Rust** strippe (358 Ko, imports `_Unwind*`, `pthread_*`). Le `main` est
retrouvable par la chaine `Invalid password` : le point d'entree `_start` passe le vrai `main`
a `lang_start`, et le code utile est juste a cote du message d'erreur.

### Ce que fait la verification

```asm
cmp qword [rax+0x28], 0x29      ; longueur == 41
movabs rax, 0x7b796d6564616361  ; "academy{"
cmp [rbx], rax                  ; 8 premiers octets
cmp byte [rbx+0x28], 0x7d       ; dernier octet == '}'
```

puis les 32 octets intermediaires passent par **4 tours d'un reseau substitution-permutation**
(`0x168c0` appelle 4 fois `0x16940`), et le resultat est compare octet par octet a une table
de 32 octets en `.rodata` a `0x9f70` :

```
1f9950d7b8223acbcf12aecbd9209948057b7b22cd0d46f9cfe6120105cbf97b
```

### Le GPU du probleme : ce n'etait pas un `std::sort`

Les notes precedentes parlaient d'un comparateur via `std::sort` : c'est faux, et c'est ce qui
bloquait. Le comparateur est lineaire, chaque octet de sortie ne depend que d'**un** octet
d'entree. Chaque tour est exactement :

```
Rr(x)[i] = S_r( x[ P_r[i] ] )
```

- `S_r` : la r-box du tour, 256 octets a `0x8470 + 256*r` (4 tables, toutes bijectives) ;
- `P_r` : une permutation de 32 indices, 32 `u64` a `0x9fb0 + 256*r`.

Le controle final compare `R3(R2(R1(R0(x))))[i]` a `TABLE[i]`. On inverse en une passe, de la
sortie vers l'entree :

```python
y2[P3[i]] = invS3(TABLE[i])
y1[P2[k]] = invS2(y2[k])
y0[P1[k]] = invS1(y1[k])
x [P0[k]] = invS0(y0[k])
flag = b"academy{" + bytes(x) + b"}"
```

Le binaire repond `Success`. 30 lignes de Python contre une session de debugger.

### A retenir

- Un binaire Rust strippe se retrouve **par ses chaines** : `Invalid password` donne le `main`.
- Quand une table de 32 octets « random » traine en `.rodata` a cote d'une assertion, c'est la
  cible de la comparaison : chercher la fonction qui la consomme.
- Verifier qu'une S-box est **bijective** (`len(set(s)) == 256`) valide le modele en une ligne.
- Une permutation + substitution se defait analytiquement. Avant de sortir gdb, lire la
  structure des tables : 1024 octets de S-box + 4 x 256 octets de permutation, c'est un
  chiffre par blocs jouet, pas un puzzle opaque.

## Flag

```
academy{t1mingS1deChann3l_c55b1a90e29d2f}
```

## Ce qu'il faut retenir

—
