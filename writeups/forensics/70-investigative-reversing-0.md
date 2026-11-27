# Investigative Reversing 0

**Catégorie** : Forensics · **Challenge** : #70 · **Résolu le** : 2026-11-25

## Énoncé

> We recovered a binary and an image. There should be a flag somewhere.

## Résolution

Méthode : **append transform**.

Le binaire n'est **pas strippe** : `main` se lit directement. Il ouvre `flag.txt` en
lecture et `mystery.png` en **mode `a` (append)** — attention au piege : le fichier ouvert
« en image » est en fait ouvert en ajout, donc le flag est ecrit **a la fin du PNG**.

Transformation appliquee avant ecriture (26 octets) :

| indices | operation |
|---|---|
| 0..5 | tel quel |
| 6..14 | `+5` |
| 15 | `-3` |
| 16..25 | tel quel |

Il suffit donc de lire les 26 derniers octets du PNG et d'inverser :

```
tail   = 61636164656d7e806b357a73696436715f3932346166333064 7d
decode = academy{f0und_1t_924af30d}
```

### Le vrai enseignement

Les notes des sessions precedentes disaient ce challenge « refuse par le serveur » : c'etait
faux. Le serveur refuse les flags **publics** (ceux des writeups), parce que CyLab a
**regenere** le suffixe (`f0und_1t_<8 hex>`). L'artefact distribue contient le flag de
l'instance : il faut le decoder soi-meme, jamais recopier un writeup.

## Flag

```
academy{f0und_1t_924af30d}
```

## Ce qu'il faut retenir

—

## Scripts

- [`solve.py`](../../solve/70/solve.py)
- *12 variantes intermediaires dans `solve/70/archive/`*
