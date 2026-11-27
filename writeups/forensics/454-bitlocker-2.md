# Bitlocker-2

**Catégorie** : Forensics · **Challenge** : #454 · **Résolu le** : 2026-11-25

## Énoncé

> bitlocker-2.dd (199 Mo) + memdump.mem.gz (2 Go)

## Résolution

Méthode : **contenu dechiffre present en clair dans le dump RAM (volume monte)**.

Le mot de passe BitLocker est volontairement long et complexe, donc le cassage est exclu. Mais l'enonce fournit un **dump de la RAM** capture pendant que le volume etait monte : les donnees dechiffrees (et la cle) sont donc en memoire physique. Solution directe, sans decompresser les 2 Go : `zcat memdump.mem.gz | strings -n 8 | grep -oE "(academy|picoCTF)\{[^}]+\}" | sort -u` — le drapeau apparait en clair, present plusieurs fois (cache FS, tas de processus, tampons) donc `sort -u` est utile pour dedupliquer. `cryptsetup bitlkDump` confirme que le volume est bien en AES-XTS-256 avec deux keyslots (passphrase + recovery), mais aucun n'est necessaire. Piste alternative si l'on voulait la cle plutot que le texte : Volatility 3 avec le plugin `windows.bitlocker` extrait le FVEK du dump. Fichiers deja presentes dans le dossier Telechargements de l'utilisateur.

## Flag

```
academy{B1tl0ck3r_dr1v3_d3crypt3d_9029ae5b}
```

## Ce qu'il faut retenir

—
