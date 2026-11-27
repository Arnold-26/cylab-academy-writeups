# SansAlpha

**Catégorie** : General Skills · **Challenge** : #436 · **Résolu le** : 2026-11-24

## Énoncé

> —

## Résolution

Méthode : **shell sans lettres : globbing + expansion**.

Le shell n'accepte que les symboles. Techniques : `*` execute le premier fichier avec les autres en arguments (ce qui renseigne `$_`, le dernier argument = `on-calastran.txt`) ; `$-` donne les options du shell (lettres disponibles) ; l'expansion `${_:3:2}${_:8:1}` extrait `ca` + `t` de `on-calastran.txt` -> commande `cat`. Payload final : `*` puis `*; ${_:3:2}${_:8:1} */????.???` qui fait `cat blargh/flag.txt`.

## Flag

```
academy{7h15_mu171v3r53_15_m4dn355_0abcd64b}
```

## Ce qu'il faut retenir

—

## Scripts

- [`_z_436a.py`](../../solve/436/_z_436a.py)
- [`_z_436b.py`](../../solve/436/_z_436b.py)
- [`_z_436c.sh`](../../solve/436/_z_436c.sh)
- [`_z_436d.sh`](../../solve/436/_z_436d.sh)
- [`_z_436e.py`](../../solve/436/_z_436e.py)
