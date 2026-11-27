# Nice netcat...

**Catégorie** : General Skills · **Difficulté** : Easy · **Épreuve** : picoCTF 2019
**Challenge** : #156

## Énoncé

> There is a nice program that you can talk to by using this command in a shell: `$ nc chatelaine.cylabacademy.net 47552`, but it doesn't speak English...

**Entrée** : service TCP (endpoint fourni au démarrage)

## Résolution

Connexion `nc`, le service envoie 39 nombres. Conversion ASCII (`chr(n)` pour chaque valeur) → le flag apparaît. Premier nombre 97 = 'a'.

## Flag

```
academy{g00d_k1tty!_n1c3_k1tty!_6d1e6}
```

## Ce qu'il faut retenir

« doesn't speak English » = les octets sont en décimal. `chr()` sur toute la liste, pas un par un.
