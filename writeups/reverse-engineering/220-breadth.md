# breadth

**Catégorie** : Reverse Engineering · **Challenge** : #220 · **Résolu le** : 2026-11-24

## Énoncé

> —

## Résolution

Méthode : **diff de deux binaires (v1/v2)**.

`breadth.v1` et `breadth.v2` font 2605312 octets et ne different que de **36 octets**. Un build-id, un octet dans une chaine de version, et surtout 14 octets de code dans `fcnkKTQpF` (0x95040) : v1 fait `mov eax,0xd037803a; cmp rdx,rax` (comparaison toujours fausse) alors que v2 fait `cmp rax,0x41bc73e`, la valeur qu'il vient de stocker. La version `v2` passe donc le test et `puts` affiche le flag. Le binaire contient des centaines de faux flags `picoCTF{...}` : il faut lire celui reference par le `puts` de la fonction corrigee (offset fichier 0x155ef8), pas chercher avec `strings`.

## Flag

```
picoCTF{VnDB2LUf1VFJkdfDJtdYtFlMexPxXS6X}
```

## Ce qu'il faut retenir

—

## Scripts

- [`_z_220a.sh`](../../solve/220/_z_220a.sh)
- [`_z_220b.py`](../../solve/220/_z_220b.py)
- [`_z_220c.py`](../../solve/220/_z_220c.py)
- [`_z_220d.py`](../../solve/220/_z_220d.py)
- [`_z_220e.py`](../../solve/220/_z_220e.py)
- [`_z_220f.py`](../../solve/220/_z_220f.py)
