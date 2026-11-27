# convertme.py

**Catégorie** : General Skills · **Difficulté** : Easy · **Épreuve** : picoCTF 2022
**Challenge** : #239

## Résolution

Script exécuté en interactif : il demande la conversion d'un nombre aléatoire en binaire, réponse calculée avec `bin(n)[2:]`.

## Flag

```
academy{4ll_y0ur_b4535_fff0af3d}
```

## Ce qu'il faut retenir

Automatiser l'interactif : tubes binaires, sans quoi Windows traduit `\n` en `\r\n` et casse la saisie.
