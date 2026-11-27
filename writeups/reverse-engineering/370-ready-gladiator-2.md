# Ready Gladiator 2

**Catégorie** : Reverse Engineering · **Challenge** : #370 · **Résolu le** : 2026-11-25

## Énoncé

> nc xebec.cylabacademy.net <port>

## Résolution

Méthode : **CoreWars : warrior Gnat qui bat l'Imp 100/100**.

Le service lance un combat **CoreWars** (RedCode) : il faut fournir un warrior qui bat « The Imp » (`mov 0, 1`) sur 100 rounds. Le warrior soumis est lu sur stdin jusqu'a `end`. Apres avoir teste sans succes des strategies naives, le writeup donne la solution fiable : **Gnat** (`gnat  mov -1, <-2` puis `jmp gnat, <-3`), un warrior qui se recopie en decalage et finit par ecraser l'Imp. Resultat verifie : « Rounds: 100 / Warrior 1 wins: 100 / Warrior 2 wins: 0 / Ties: 0 », puis le flag. Envoi : `nc <host> <port> < gnat.red`. Detail : le fichier doit finir par `end`, sinon le service attend encore.

## Flag

```
academy{d3m0n_3xpung3r_36e6efa4}
```

## Ce qu'il faut retenir

—
