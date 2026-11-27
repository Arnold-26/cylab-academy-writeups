# tunn3l v1s10n

**Catégorie** : Forensics · **Challenge** : #112 · **Résolu le** : 2026-11-23

## Énoncé

> —

## Résolution

Méthode : **reparation d'entete BMP (hauteur)**.

`file` voit le fichier comme `data`. L'entete BMP est corrompu : `bfOffBits=0xd0ba` (53434) et `biSize=53434` au lieu de 54 et 40. Apres correction, l'image s'affiche mais en 1134x**306** avec le texte `notaflag(sorry)` : c'est un leurre. Les donnees du fichier couvrent en realite **850 lignes** ((taille-54)/(1134*3)). Corriger `biHeight` a 850 revele le haut de l'image, ou est ecrit `academy{qu1t3_a_v13w_2020}`.

## Flag

```
academy{qu1t3_a_v13w_2020}
```

## Ce qu'il faut retenir

—
