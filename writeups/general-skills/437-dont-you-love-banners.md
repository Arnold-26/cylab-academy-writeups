# dont-you-love-banners

**Catégorie** : General Skills · **Challenge** : #437 · **Résolu le** : 2026-11-23

## Énoncé

> —

## Résolution

Méthode : **symlink sur le banner root**.

Le port SSH fuit le mot de passe dans sa banniere (`My_Passw@rd_@1234`). Le port applicatif demande ce mot de passe puis deux questions de culture hacker (DEF CON, John Draper) et donne un shell `player`. `ps aux` revele : `socat TCP4-LISTEN:4221 system:'python3 /root/script.py'` execute en **root** et lit `~/banner`. On remplace `~/banner` par un lien symbolique vers `/root/flag.txt` : a la connexion suivante, root affiche le flag.

## Flag

```
academy{b4nn3r_gr4bb1n9_su((3sfu11y_5f2334f1}
```

## Ce qu'il faut retenir

—
