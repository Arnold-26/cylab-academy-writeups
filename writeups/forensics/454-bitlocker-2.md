# Bitlocker-2

**Catégorie** : Forensics · **Challenge** : #454 · **Résolu le** : 2026-11-25

## Énoncé

> bitlocker-2.dd (199 Mo) + memdump.mem.gz (2 Go)

## Résolution

Méthode : **contenu déchiffre present en clair dans le dump RAM (volume monte)**.

Le mot de passe BitLocker est volontairement long et complexe, donc le cassage est exclu. Mais l'énoncé fournit un **dump de la RAM** capture pendant que le volume etait monte : les données dechiffrees (et la clé) sont donc en mémoire physique. Solution directe, sans decompresser les 2 Go : `zcat memdump.mem.gz | strings -n 8 | grep -oE "(academy|picoCTF)\{[^}]+\}" | sort -u` — le drapeau apparait en clair, present plusieurs fois (cache FS, tas de processus, tampons) donc `sort -u` est utile pour dedupliquer. `cryptsetup bitlkDump` confirme que le volume est bien en AES-XTS-256 avec deux keyslots (passphrase + recovery), mais aucun n'est nécessaire. Piste alternative si l'on voulait la clé plutôt que le texte : Volatility 3 avec le plugin `windows.bitlocker` extrait le FVEK du dump. Fichiers déjà presentes dans le dossier Telechargements de l'utilisateur.

## Flag

```
academy{B1tl0ck3r_dr1v3_d3crypt3d_9029ae5b}
```
