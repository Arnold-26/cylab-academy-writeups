# 362 — PcapPoisoning

**Événement** : picoCTF 2023 · **Catégorie** : Forensics · **Auteur** : Mubarak Mikail

> Synthèse rédigée à partir des sources publiques listées en fin de fiche : ce challenge a été
> résolu côté CyLab Academy, mais le writeup d'origine n'a pas été conservé.

## Énoncé

« Et si on jouait à cache-cache ? Téléchargez ce fichier et trouvez le flag. »
Le fichier fourni est `trace.pcap`.

## Analyse

Le nom du challenge (« poisoning ») suggère une injection de paquets TCP, mais la recherche
est beaucoup plus simple : le flag circule **en clair dans la charge utile** d'un unique
segment, sans encodage ni chiffrement.

Deux chemins équivalents :

- **Wireshark** : filtre d'affichage `tcp.payload contains "picoCTF"` — un seul paquet
  remonte (le paquet n°507 dans les captures publiques), et le flag apparaît dans la colonne
  ASCII du volet « Packet bytes ».
- **`strings`** : les octets du PCAP contiennent la chaîne telle quelle, donc
  `strings trace.pcap | grep pico` suffit. C'est le triage à faire *avant* d'ouvrir une GUI.

## Solution

```bash
wget https://artifacts.picoctf.net/c/371/trace.pcap
strings trace.pcap | grep pico
```

En Wireshark, la même valeur se lit dans l'en-tête TCP du paquet trouvé par le filtre. La
source publique donne le dump hexadécimal de la charge utile :

```
0030   50 36 34 50 5f 34 4e 34 4c 37 53 31 53 5f 53 55   P64P_4N4L7S1S_SU
0040   35 35 33 35 35 46 55 4c 5f 34 64 37 32 64 66 63   55355FUL_4d72dfc
0050   63 7d                                             c}
```

La colonne ASCII est caviardée dans le writeup, mais le décodage des octets hexadécimaux
ci-dessus reconstruit intégralement la chaîne du flag (données de la source, pas d'invention).

## Flag

```
picoCTF{P64P_4N4L7S1S_SU55355FUL_4d72dfcc}
```

## Sources

- https://github.com/snwau/picoCTF-2023-Writeup/blob/main/Forensics/PcapPoisoning/PcapPoisoning.md
- https://picoctfsolutions.com/picoctf-2023-pcappoisoning
- https://github.com/Cajac/picoCTF-Writeups/blob/main/picoCTF_2023/Forensics/PcapPoisoning.md
