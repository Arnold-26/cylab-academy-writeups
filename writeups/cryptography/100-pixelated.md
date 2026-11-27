# Pixelated

**Catégorie** : Cryptography · **Challenge** : #100 · **Résolu le** : 2026-11-23

## Énoncé

> I have these 2 images, can you make a flag out of them?
> [scrambled1.png](https://challenge-files.cylabacademy.net/library/fa686cfe375627b0131e670a19ec4775a873562ee3006dae8a40796e3e2b5e3c/scrambled1.png) [scrambled2.png](https://challenge-files.cylabacademy.net/library/fa686cfe375627b0131e670a19ec4775a873562ee3006dae8a40796e3e2b5e3c/scrambled2.png)

## Résolution

Méthode : **addition pixel à pixel**.

Deux PNG 256x256. Le flag apparait en **additionnant** les pixels (`(a+b) % 256`) : le texte est reparti entre les deux images de sorte que la somme reconstitue les caractères noirs sur fond blanc.

## Flag

```
academy{2f16d0c4}
```
