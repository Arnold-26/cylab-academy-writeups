# what's a net cat?

**Catégorie** : General Skills · **Difficulté** : Easy · **Épreuve** : picoCTF 2019
**Challenge** : #34

## Énoncé

> Using netcat (nc) is going to be pretty important. Can you connect to `chatelaine.cylabacademy.net` at port `20325` to get the flag?

**Entrée** : service TCP (endpoint fourni au démarrage)

## Résolution

`nc chatelaine.cylabacademy.net 20325` → le service renvoie directement le flag.

## Flag

```
academy{nEtCat_Mast3ry_Bc0C3F60}
```

## Ce qu'il faut retenir

`nc` est l'outil de base : `nc host port` puis lecture. Toujours fermer stdin (`< /dev/null`) en script.
