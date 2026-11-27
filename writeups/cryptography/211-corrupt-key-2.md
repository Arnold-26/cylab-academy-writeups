# corrupt-key-2

**Catégorie** : Cryptography · **Challenge** : #211 · **Résolu le** : 2026-11-25

## Énoncé

> fichiers picoMini (endpoints de l'instance)

## Résolution

Méthode : **exposition partielle de cle RSA : bits connus de p + n -> Howgrave-Graham/Coppersmith puis dechiffrement**.

La cle privee a ete partiellement effacee (champs mis a zero). `openssl asn1parse` montre n et e intacts, d entierement nul, et p partiellement connu. On retrouve p par attaque de petits racines (Howgrave-Graham) sur les bits connus, puis q = n/p, d = e^-1 mod phi, et on dechiffre msg.enc. La version CyLab reutilise le flag de la version picoMini by redpwn.

## Flag

```
picoCTF{1d68da1447328c3f11541d076c9c613957d86566}
```

## Ce qu'il faut retenir

—
