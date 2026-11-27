# MATRIX

**Catégorie** : Reverse Engineering · **Challenge** : #221 · **Résolu le** : 2026-11-24

## Énoncé

> nc mars.cylabacademy.net 31259

## Résolution

Méthode : **VM custom + BFS labyrinthe**.

Le binaire est une **VM a pile** faite main : un dispatch sur un octet d'opcode, avec deux piles (principale + alt), des sauts conditionnels, et GETCHAR/PUTCHAR. Le bytecode embarque un **labyrinthe** : `#` murs, `^` gagne de la vie, `v` en perd, `$` sortie, et 5 checkpoints verifient que le compteur de vie >= 5. Le chemin le plus court geometriquement echoue car il saute les `^`. Chemin valide de 63 coups : `rrrrrlrlrlrlrllddddddlddrrddrrrrdddrruuuruuuuuuurrddddddddlddrd`. Le flag n'est pas dans le binaire : il est lu depuis `flag.txt` sur le serveur, donc il faut l'envoyer a l'instance nc.

## Flag

```
picoCTF{y0uv3_3sc4p3d_th3_m4ze...f0r_n0w-hYkq2D9PmrA5GpEq}
```

## Ce qu'il faut retenir

—
