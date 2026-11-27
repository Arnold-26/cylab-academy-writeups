# Chronohack

**Catégorie** : Reverse Engineering · **Challenge** : #468 · **Résolu le** : 2026-11-24

## Énoncé

> nc xebec.cylabacademy.net <port>

## Résolution

Méthode : **seed de PRNG base sur time.time()*1000 : brute force temporel**.

Le generateur fourni (`token_generator.py`, 45 lignes) fait `random.seed(int(time.time() * 1000))` puis 20 fois `random.choice(alphabet)` : le token est **entierement determine par l'horodatage en millisecondes** au demarrage du programme. Le service accepte 50 tentatives par connexion, donc chaque connexion permet de tester 50 seeds consecutifs. Deux points mesures par l'experience : (1) le token est regenere a chaque connexion (un nouveau processus est lance) — verifie en consommant 50 tentatives puis en rouvrant une connexion, qui redemarre bien a zero ; (2) le decalage entre l'horloge locale et la date de demarrage du programme est de l'ordre de la centaine de millisecondes (trouve a **+100 ms**). Le facteur decisif a ete le **pipelining** : envoyer les 50 candidats d'un seul coup et lire la reponse en bloc, au lieu d'attendre le prompt entre chaque essai — le scan complet de +/-10 s est passe de plusieurs heures a 2,5 minutes. Une fois le bon seed trouve, la reponse « Congratulations! » est suivie du contenu de /flag.txt.

## Flag

```
academy{UseSecure#$_Random@j3n3r@T0rs02d049c1}
```

## Ce qu'il faut retenir

—
