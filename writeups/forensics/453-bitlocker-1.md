# Bitlocker-1

**Catégorie** : Forensics · **Challenge** : #453 · **Résolu le** : 2026-11-25

## Énoncé

> bitlocker-1.dd (100 Mo)

## Résolution

Méthode : **BitLocker : cassage du mot de passe (john+rockyou) puis cryptsetup bitlk**.

Image disque BitLocker de 100 Mo. `cryptsetup bitlkDump` lit les metadonnees sans mot de passe : version 2, AES-128-CBC, description « DESKTOP-EKVR84B New Volume », deux keyslots (0 = recovery passphrase, 1 = passphrase utilisateur) et un FVEK. L'enonce dit que Jacky utilise « a simple password » : `bitlocker2john -i bitlocker-1.dd` extrait les hachages, et `john --wordlist=rockyou.txt` les casse en quelques minutes — le mot de passe est **jacqueline** (valable pour les deux slots). Ensuite `cryptsetup open --type bitlk --key-file=pw.txt bitlocker-1.dd bl1` cree /dev/mapper/bl1, un `mount -o ro` donne acces a la partition NTFS et `flag.txt` contient le drapeau. Note : cryptsetup >= 2.3 gere BitLocker nativement, dislocker n'est pas necessaire. Fichier recupere depuis le dossier Telechargements de l'utilisateur pour eviter un telechargement de 100 Mo.

## Flag

```
academy{us3_b3tt3r_p4ssw0rd5_pl5!_3242adb1}
```

## Ce qu'il faut retenir

—
