# riscy business

**Catégorie** : Reverse Engineering · **Challenge** : #219 · **Résolu le** : 2026-11-24

## Énoncé

> Try not to take too many riscs when finding the flag.

## Résolution

Méthode : **RC4 avec clé = les 8 premiers octets de l'entrée**.

Binaire **RISC-V** statique stripped, exécute avec `qemu-riscv64`. Le desassemblage montre une implementation **RC4** : KSA a 0x10086 (table de 256 octets, `remu`, swaps) puis PRGA a 0x100d2. Le `main` appelle la KSA avec `a1 = entree`, `a2 = 8` : **la clé RC4 est les 8 premiers octets de l'entrée**, donc `picoCTF{` puisque le flag commence par la. Le chiffre attendu est en `.rodata` a 0x10210 (52 octets, compare jusqu'a 0x10244). Déchiffrer avec la clé `picoCTF{` donne directement le flag.

## Flag

```
picoCTF{4ny0n3_g0t_r1scv_h4rdw4r3?_LGUfwl8xyMUlpgvz}
```

## Scripts

- [`solve.py`](../../solve/219/solve.py)
