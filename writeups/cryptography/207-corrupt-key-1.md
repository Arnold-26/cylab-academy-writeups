# corrupt-key-1

**Catégorie** : Cryptography · **Challenge** : #207 · **Résolu le** : 2026-11-25

## Énoncé

> fichiers picoMini (endpoints de l'instance)

## Résolution

Méthode : **recuperation de cle RSA : n et e intacts, d nul, p partiellement efface -> FactorDB / Coppersmith**.

`openssl asn1parse` sur private.key revele n (1024 bits) et e=65537 intacts, d entierement a zero et p dont la moitie basse est effacee. En extrayant n on peut le factoriser (FactorDB) ou retrouver p par Coppersmith sur les bits connus, puis reconstruire d et dechiffrer msg.enc (128 octets).

## Flag

```
picoCTF{d741543f172970457e6a9aaa890935b8}
```

## Ce qu'il faut retenir

—

## Scripts

- [`solve.py`](../../solve/207/solve.py)
- *3 variantes intermediaires dans `solve/207/archive/`*
