# Shop

**Catégorie** : Reverse Engineering · **Challenge** : #134 · **Résolu le** : 2026-11-23

## Énoncé

> Best Stuff - Cheap Stuff, Buy Buy Buy...

## Résolution

Méthode : **quantite negative**.

Boutique : on a 40 coins, le flag coute 100. En achetant une **quantite negative** d'un item a 10 coins, l'argent augmente au lieu de diminuer (40 - 10*(-10) = 140). On peut alors acheter le flag, affiche en liste d'octets ASCII.

## Flag

```
academy{b4d_brogrammer_0ca0fc368}
```
