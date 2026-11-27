# Chronohack

**Catégorie** : Reverse Engineering · **Challenge** : #468 · **Résolu le** : 2026-11-24

## Énoncé

> nc xebec.cylabacademy.net <port>

## Résolution

Méthode : **seed de PRNG base sur time.time()*1000 : brute force temporel**.

Le générateur fourni (`token_generator.py`, 45 lignes) fait `random.seed(int(time.time() * 1000))` puis 20 fois `random.choice(alphabet)` : le token est **entierement determine par l'horodatage en millisecondes** au demarrage du programme. Le service accepte 50 tentatives par connexion, donc chaque connexion permet de tester 50 seeds consecutifs. Deux points mesures par l'experience : (1) le token est regenere à chaque connexion (un nouveau processus est lance) — vérifie en consommant 50 tentatives puis en rouvrant une connexion, qui redemarre bien a zero ; (2) le décalage entre l'horloge locale et la date de demarrage du programme est de l'ordre de la centaine de millisecondes (trouve a **+100 ms**). Le facteur decisif a été le **pipelining** : envoyer les 50 candidats d'un seul coup et lire la réponse en bloc, au lieu d'attendre le prompt entre chaque essai — le scan complet de +/-10 s est passé de plusieurs heures a 2,5 minutes. Une fois le bon seed trouve, la réponse « Congratulations! » est suivie du contenu de /flag.txt.

## Flag

```
academy{UseSecure#$_Random@j3n3r@T0rs02d049c1}
```

## Scripts

- [`solve.py`](../../solve/468/solve.py)
- *6 variantes intermediaires dans `solve/468/archive/`*
