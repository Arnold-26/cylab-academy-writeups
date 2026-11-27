# miniRSA

**Catégorie** : Cryptography · **Challenge** : #73 · **Résolu le** : 2026-11-23

## Énoncé

> Let's decrypt this.
> Can you decrypt this [ciphertext](https://challenge-files.cylabacademy.net/library/eda4bb1f373e93620b8b14221ab1eee5b035609abf646d329514eb7e99f93c03/ciphertext)? Something seems a bit small.

## Résolution

Méthode : **petit exposant + balayage de k**.

`e=3` et le message est court (c fait 788 bits contre N=2048) : `c + k*N` est une puissance cubique parfaite. k=0 suffit ici. Racine cubique entiere par bissection.

## Flag

```
academy{n33d_a_lArg3r_e_1106c382}
```
