# Easy as GDB

**Catégorie** : Reverse Engineering · **Challenge** : #122 · **Résolu le** : 2026-11-25

## Énoncé

> The flag has got to be checked somewhere...

## Résolution

Méthode : **static reversing**.

Binaire ELF 32 bits strippe, mais petit (~13 Ko) : la verification se lit entierement
au desassemblage, pas besoin de gdb.

### Les trois briques

| adresse | role |
|---|---|
| `0x1290` | `swap(buf, len, n)` : inverse chaque bloc de `n` octets |
| `0x1302` | `shuffle(buf, len, m)` : `m > 0` -> `swap` pour `i = 1..len-1` croissant ; sinon decroissant |
| `0x11fd` | `xor_func(buf, len, key)` : `buf[j] ^= key.to_bytes(4,'big')[j & 3]` |
| `0x136b` | `transform(input, len)` : 1714 tours de XOR avec des cles derivees de `0x0abcf00d` |
| `0x1404` | `compare(p, len)` : la verification |

### Le controle

```c
p = transform(input, len);      // len = strnlen(ref, 0x200)
shuffle(p, len, +1);
compare(p, len);                // shuffle(p,-1) == shuffle(ref,-1)  ?
```

La reference est le blob de 30 octets a `0x4008` (`.data`) :

```
7a3f64633b5a167c6d436f36666246144361423f58015834623d6a303a17
```

Deux proprietes rendent l'inversion triviale :

1. `shuffle(., +1)` compose avec `shuffle(., -1)` donne l'identite (verifie
   numeriquement sur 5 desordres aleatoires) — les deux `swap` de tailles croissantes puis
   decroissantes s'annulent.
2. `transform` est une involution : il n'applique que des XOR, avec la meme suite de cles
   a chaque appel, donc `transform(transform(x)) == x`.

Donc il suffit de faire `input = transform(shuffle(ref, -1))` :

```python
D    = shuffle(C, -1)          # ce que compare attend
flag = transform(D, len)       # 1714 tours de XOR
```

Le binaire confirme en local : `Correct!`, puis l'API accepte le flag.

Note au passage : `strncpy` copie `n = (len & ~3) + 4` octets, donc 32 ici — les deux
octets de padding (newline + NUL) sont transformes mais jamais compares, ce qui n'a
aucune incidence. Mais oublier que `swap` s'arrete a `len - n + 1` fausse tout le reste :
c'est le genre de detail qu'il faut implementer exactement, pas "a peu pres".

## Flag

```
academy{I_5D3_A11DA7_f73c8ead}
```

## Ce qu'il faut retenir

—

## Scripts

- [`solve.py`](../../solve/122/solve.py)
- *5 variantes intermediaires dans `solve/122/archive/`*
