# Keygenme

**Catégorie** : Reverse Engineering · **Challenge** : #276 · **Résolu le** : 2026-11-24

## Énoncé

> —

## Résolution

Méthode : **extraction de la chaine attendue par gdb**.

`keygenme` (ELF 64 PIE stripped) demande une licence. La fonction de verification (0x1209) construit **le flag attendu sur la pile** : une serie de `movabs` partiellement chevauchants ecrit `academy{H` a [rbp-0x90], `br1ng_y0H` a +8, `g_y0ur_0H` a +12 (ce qui ecrase et recolle en `br1ng_y0ur_0`), puis `wn_k3y_` a +20, donnant `academy{br1ng_y0ur_0wn_k3y_`. Ensuite l'entree est hashee en MD5, convertie en hexa par `sprintf("%02x")`, et une partie de cet hexadecimal complete le flag. La comparaison finale (0x1442) est INLINE (boucle sur 36 caracteres), donc les hooks LD_PRELOAD sur strcmp/memcmp ne declenchent rien. Il faut un **breakpoint gdb a 0x1442** (base PIE 0x555555554000 avec ASLR desactive, et entree de 36 caracteres sinon la fonction sort avant par un controle de longueur) puis `x/s $rbp-0x30` : la chaine complete y est en clair.

## Flag

```
academy{br1ng_y0ur_0wn_k3y_bb724f88}
```

## Ce qu'il faut retenir

—
