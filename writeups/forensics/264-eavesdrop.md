# Eavesdrop

**Catégorie** : Forensics · **Challenge** : #264 · **Résolu le** : 2026-11-23

## Résolution

Méthode : **pcap -> mot de passe -> openssl des3**.

Le pcap contient une conversation en clair ou un utilisateur donne la commande `openssl des3 -d -salt -in file.des3 -out file.txt -k supersecretpassword123`. Le fichier `file.des3` se trouve dans un autre flux TCP (signature `Salted__`) : on l'extrait et on le dechiffre avec ce mot de passe.

## Flag

```
academy{nc_73115_411_02612719}
```

## Ce qu'il faut retenir

Un pcap se lit par flux (`-z follow,tcp,ascii`), pas paquet par paquet.
