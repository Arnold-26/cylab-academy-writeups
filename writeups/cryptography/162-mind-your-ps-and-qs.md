# Mind your Ps and Qs

**Catégorie** : Cryptography · **Challenge** : #162 · **Résolu le** : 2026-11-23

## Résolution

Méthode : **RSA + factordb + inversion**.

RSA a petit N : factoriser n donne p et q, puis `d = e^-1 mod phi`, `m = c^d mod n`. Le clair obtenu est **inverse** (`ymedaca` -> `academy`) : toujours tester le reverse. Pollard rho/Fermat echouent ici, factordb.com donne la factorisation.

## Flag

```
academy{sma11_N_n0_g0od_a3ac7152}
```
