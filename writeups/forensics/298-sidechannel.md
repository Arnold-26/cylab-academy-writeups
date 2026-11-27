# SideChannel

**Catégorie** : Forensics · **Challenge** : #298 · **Résolu le** : 2026-11-24

## Énoncé

> nc xebec.cylabacademy.net 48223

## Résolution

Méthode : **attaque temporelle sur un PIN a 8 chiffres**.

`pin_checker` (ELF 32 bits) verifie un PIN a 8 chiffres et **compare caractere par caractere avec un delai**, ce qui cree un oracle temporel. En local (pas de bruit reseau), on determine le PIN position par position : pour chacun des 8 chiffres, on essaie les 10 possibilites en gardant le prefixe deja trouve et en completant par des zeros, on mesure le temps median de 3 executions, et on garde le chiffre le plus lent (le plus de caracteres corrects = le plus de delais accumules). Temps mesures : 385 ms -> 523 -> 743 -> 1177 -> 1079 -> 1279 -> 1351 -> 1451 ms, PIN = **48390513**, que le binaire accepte (« Access granted »). Le PIN se rentre ensuite sur le serveur maitre, qui renvoie le flag.

## Flag

```
academy{t1m1ng_4tt4ck_55dcfc0f}
```

## Ce qu'il faut retenir

—

## Scripts

- [`solve.py`](../../solve/298/solve.py)
- *5 variantes intermediaires dans `solve/298/archive/`*
