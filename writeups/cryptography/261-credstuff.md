# credstuff

**Catégorie** : Cryptography · **Challenge** : #261 · **Résolu le** : 2026-11-23

## Énoncé

> —

## Résolution

Méthode : **index parallele + ROT13**.

`leak.tar` contient `usernames.txt` et `passwords.txt` (505 lignes chacun, listes paralleles). On cherche `cultiris` a l'index i et on prend le mot de passe au meme index : `npnqrzl{P7e1S_54I35_71Z3}`, qui est du **ROT13** -> `academy{C7r1F_54V35_71M3}`.

## Flag

```
academy{C7r1F_54V35_71M3}
```

## Ce qu'il faut retenir

—
