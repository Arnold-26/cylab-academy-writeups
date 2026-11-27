# Flag Hunters

**Catégorie** : Reverse Engineering · **Challenge** : #472 · **Résolu le** : 2026-11-23

## Résolution

Méthode : **injection au prompt Crowd**.

Le lecteur de paroles remplace la ligne CROWD par `'Crowd: ' + input` puis la re-decode avec `split(';')`. En envoyant `;RETURN 0` (sans espace apres le point-virgule), on injecte une commande `RETURN 0` qui remonte au debut du morceau, ou se trouve le flag.

## Flag

```
academy{70637h3r_f0r3v3r_697ad4d5}
```
