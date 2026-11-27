# Bases

**Catégorie** : Général Skills · **Difficulté** : Easy · **Épreuve** : picoCTF 2019
**Challenge** : #67

## Énoncé

> What does this `bDNhcm5fdGgzX3IwcDM1` mean? I think it has something to do with bases.

**Entrée** : —

## Résolution

Chaîne en base64 (alphabet `A-Za-z0-9+/`, longueur multiple de 4 attendue). `base64.b64decode('bDNhcm5fdGgzX3IwcDM1')` → `l3arn_th3_r0p35`.

## Flag

```
academy{l3arn_th3_r0p35}
```

## Ce qu'il faut retenir

« bases » dans l'énoncé = base64/base32/hex. Reconnaître l'alphabet avant de décoder.
