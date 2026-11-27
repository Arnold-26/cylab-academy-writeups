# riscy business

**Catégorie** : Reverse Engineering · **Challenge** : #219 · **Résolu le** : 2026-11-24

## Énoncé

> —

## Résolution

Méthode : **RC4 avec cle = les 8 premiers octets de l'entree**.

Binaire **RISC-V** statique stripped, execute avec `qemu-riscv64`. Le desassemblage montre une implementation **RC4** : KSA a 0x10086 (table de 256 octets, `remu`, swaps) puis PRGA a 0x100d2. Le `main` appelle la KSA avec `a1 = entree`, `a2 = 8` : **la cle RC4 est les 8 premiers octets de l'entree**, donc `picoCTF{` puisque le flag commence par la. Le chiffre attendu est en `.rodata` a 0x10210 (52 octets, compare jusqu'a 0x10244). Dechiffrer avec la cle `picoCTF{` donne directement le flag.

## Flag

```
picoCTF{4ny0n3_g0t_r1scv_h4rdw4r3?_LGUfwl8xyMUlpgvz}
```

## Ce qu'il faut retenir

—
