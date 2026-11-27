# Mind your Ps and Qs

**Catégorie** : Cryptography · **Challenge** : #162 · **Résolu le** : 2026-11-23

## Énoncé

> In RSA, a small $$e$$ value can be problematic, but what about $$N$$? Can you decrypt this?
> [values](https://challenge-files.cylabacademy.net/library/4a3b1aca528881eece43ed483e527d3700c5e388eb5ab2291015dbd67a809f31/values)

## Résolution

Méthode : **RSA + factordb + inversion**.

RSA a petit N : factoriser n donne p et q, puis `d = e^-1 mod phi`, `m = c^d mod n`. Le clair obtenu est **inverse** (`ymedaca` -> `academy`) : toujours tester le reverse. Pollard rho/Fermat echouent ici, factordb.com donne la factorisation.

## Flag

```
academy{sma11_N_n0_g0od_a3ac7152}
```
