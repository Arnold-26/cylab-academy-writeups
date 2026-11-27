# Static ain't always noise

**Catégorie** : Général Skills · **Difficulté** : Easy · **Épreuve** : picoCTF 2021

## Énoncé

> Can you look at the data in this binary? The bash script might help!
> [static](https://challenge-files.cylabacademy.net/library/62b13fdfc80476be04e35a972b82367cf77538d9327931635d3bb6283a40f86c/static), [ltdis.sh](https://challenge-files.cylabacademy.net/library/62b13fdfc80476be04e35a972b82367cf77538d9327931635d3bb6283a40f86c/ltdis.sh)

**Challenge** : #163

## Résolution

Binaire `static` + script `ltdis.sh` : `strings` sur le binaire remonte le flag.

## Flag

```
academy{d15a5m_t34s3r_fac3431a}
```

## Ce qu'il faut retenir

Un binaire « statique » garde ses chaînes en clair.
