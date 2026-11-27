# spelling-quiz

**Catégorie** : Cryptography · **Challenge** : #210 · **Résolu le** : 2026-11-23

## Énoncé

> —

## Résolution

Méthode : **substitution + vote majoritaire**.

`public.zip` contient `encrypt.py` (substitution monoalphabetique des a-z), `flag.txt` chiffre et `study-guide.txt` avec 272 543 mots chiffres. Chaque mot chiffre est compare aux mots anglais de meme MOTIF (meme longueur + meme schema de repetitions). On ne garde que les mots a <= 3 candidats, on fait VOTER chaque paire lettre-chiffree -> lettre-claire, et la majorite donne les 26 correspondances.

## Flag

```
picoCTF{perhaps_the_dog_jumped_over_was_just_tired}
```

## Ce qu'il faut retenir

—
