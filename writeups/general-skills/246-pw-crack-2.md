# PW Crack 2

**Catégorie** : General Skills · **Difficulté** : Easy · **Épreuve** : picoCTF 2022
**Challenge** : #246

## Résolution

Le mot de passe est construit par concaténation : `chr(0x34)+chr(0x65)+chr(0x63)+chr(0x39)` = `4ec9`.

## Flag

```
academy{tr45h_51ng1ng_d99a9ef4}
```

## Ce qu'il faut retenir

Désobfusquer une expression `chr()` se fait en l'évaluant.
