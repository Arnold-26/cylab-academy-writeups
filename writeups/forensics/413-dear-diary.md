# Dear Diary

**Catégorie** : Forensics · **Challenge** : #413 · **Résolu le** : 2026-11-25

## Énoncé

> disk.flag.img (1 Go, MBR 3 partitions)

## Résolution

Méthode : **14 occurrences du nom innocuous-file.txt -> fragments dans les entrees de repertoire**.

Image disque de 1 Go (MBR, 3 partitions : boot, swap, racine Alpine). Ma premiere copie etait **tronquee** (30 Mo de gz au lieu de 68, `gzip -t` en erreur) : c'est ce qui m'avait fait conclure a tort que l'asset etait incomplet. Verification decisive : l'ISIZE des 4 derniers octets du gz annoncait 2 Go, alors que mon fichier decompresse faisait 612 Mo. Apres re-telechargement complet (68 352 989 octets, `gzip -t` OK), l'image fait exactement 1 073 741 824 octets. Methode : le writeup dit que `its-all-in-the-name` est un indice et que le nom **innocuous-file.txt** apparait **14 fois**, chaque occurrence portant un fragment. Un simple `grep -aob innocuous-file.txt` sur l'image brute donne les 14 offsets (1 a 600033336 dans un ancien bloc de repertoire supprime, 13 groupes vers 728 730 000). En dumpant le contexte de chacune, on lit l'entree de repertoire suivante, dont le nom est un fragment : `pic`, `oCT`, `F{1`, `_53`, `3_n`, `4m3`, `5_a`, `1ee`, `d51`, `7}`. La concatenation donne `picoCTF{1_533_n4m35_a1eed517}` (leet : « I see the name is… »). **Piege** : j'ai d'abord concatene trop vite et insere un `3_` en trop, ce qui a fait echouer trois soumissions ; il faut reconstituer caractere par caractere en respectant les frontieres des fragments.

## Flag

```
academy{1_533_n4m35_a1eed517}
```

## Scripts

- [`solve.py`](../../solve/413/solve.py)
- *21 variantes intermediaires dans `solve/413/archive/`*
