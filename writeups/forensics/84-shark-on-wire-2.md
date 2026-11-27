# shark on wire 2

**Catégorie** : Forensics · **Challenge** : #84 · **Résolu le** : 2026-11-25

## Énoncé

> shark-on-wire-2-capture.pcap

## Résolution

Méthode : **flag encode dans les ports source UDP (5000 + code ASCII)**.

La capture contient 614 paquets UDP. Le piege est de chercher le flag dans les **payloads** : ils contiennent bien des caractères un par paquet (port 8888) mais dans un ordre melange et avec des leurres (`kfdsalkfsalk`, des series de `f` et de `z` sur le port 8990) — j'ai perdu du temps a trier ces payloads par numéro de paquet, par `ip.id`, par TTL, par longueurs et par port, tous donnant la même chaîne incoherente `cccaaddemyemy{N0t_{StaTa_fLa31355g}_36f6e6e}`. La vraie cachette, donnée par le writeup, est le **port source UDP** : un hote (**10.0.0.66**) envoie ses paquets avec `srcport = 5000 + code ASCII du caractere`. En triant les paquets de cet hote par ordre d'arrivee et en calculant `srcport - 5000`, on obtient directement le drapeau. Les autres hotes (10.0.0.100, .75, .67, .79, .78, .77, .110) n'emettent qu'un ou deux caractères `a` — des leurres. Lecon : quand une valeur varie d'un paquet à l'autre (port, ID, TTL), c'est souvent ELLE qui porte la donnée.

## Flag

```
academy{p1LLf3r3d_data_v1a_st3g0}
```

## Scripts

- [`solve.py`](../../solve/84/solve.py)
- *15 variantes intermediaires dans `solve/84/archive/`*
