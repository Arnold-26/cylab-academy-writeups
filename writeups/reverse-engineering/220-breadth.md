# breadth

**Catégorie** : Reverse Engineering · **Challenge** : #220 · **Résolu le** : 2026-11-24

## Énoncé

> Surely this is what people mean when they say "horizontal scaling," right?
> TOP SECRET INFO:
> Our operatives managed to exfiltrate an in-development version of this
> challenge, where the function with the real flag had a mistake in it. Can
> you help us get the flag?

## Résolution

Méthode : **diff de deux binaires (v1/v2)**.

`breadth.v1` et `breadth.v2` font 2605312 octets et ne different que de **36 octets**. Un build-id, un octet dans une chaîne de version, et surtout 14 octets de code dans `fcnkKTQpF` (0x95040) : v1 fait `mov eax,0xd037803a; cmp rdx,rax` (comparaison toujours fausse) alors que v2 fait `cmp rax,0x41bc73e`, la valeur qu'il vient de stocker. La version `v2` passe donc le test et `puts` affiche le flag. Le binaire contient des centaines de faux flags `picoCTF{...}` : il faut lire celui référence par le `puts` de la fonction corrigee (offset fichier 0x155ef8), pas chercher avec `strings`.

## Flag

```
picoCTF{VnDB2LUf1VFJkdfDJtdYtFlMexPxXS6X}
```

## Scripts

- [`solve.py`](../../solve/220/solve.py)
