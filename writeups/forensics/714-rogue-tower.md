# 714 — Rogue Tower

**Événement** : picoCTF 2026 · **Catégorie** : Forensics

## Énoncé
« A suspicious cell tower has been detected. »

La capture `rogue_tower.pcap` doit permettre d'identifier la tour pirate et de récupérer les données
qu'elle a exfiltrées. L'habillage est cellulaire, mais il faut se méfier des apparences.

## Analyse

### Le trafic utile est du HTTP ordinaire
```bash
capinfos rogue_tower.pcap
tshark -r rogue_tower.pcap -q -z io,phs
tshark -r rogue_tower.pcap -Y 'http' -T fields -e http.host -e http.request.method | head
```

Malgré le scénario — un téléphone compromis qui balise vers une « tour » pirate — le protocole utile
est du **HTTP** classique. C'est un point de méthode important : en forensics réseau, on ne part pas
du scénario énoncé, on part de ce que la capture contient réellement. Le vocabulaire cellulaire
(IMSI, CELL, PLMN) n'est ici qu'un habillage de champs applicatifs.

### Où voyage l'identité de l'appareil
Les balises du téléphone portent l'identité de l'appareil dans un en-tête **`User-Agent`** :

```
MobileDevice/1.0 (IMSI:310410185261676; CELL:96261)
```

L'IMSI est l'identifiant de la carte SIM, le CELL celui de la cellule. Un user-agent est un champ
libre : n'importe quel client peut y écrire ce qu'il veut, ce qui en fait un canal de fuite discret
et parfaitement légitime du point de vue d'un proxy ou d'un IDS basique.

D'une capture à l'autre, la tour est aussi annoncée par un **broadcast UDP sur le port 55000**,
contenant `PLMN=00101` et `CELLID=91043`. Les captures étant régénérées à chaque instance, les
valeurs diffèrent d'un tirage à l'autre — mais la structure, elle, ne change pas.

### L'exfiltration
Le flag est découpé en morceaux, chaque morceau étant encodé en base64 puis placé dans le **corps
d'une requête `POST`** distincte. Le tout est chiffré par XOR avec une clé dérivée de l'IMSI : les
**8 derniers chiffres** de l'IMSI dans la variante observée (`85261676`).

Deux conséquences pratiques :

- il faut **remettre les segments dans l'ordre des requêtes** avant de décoder, sinon le base64 est
  concaténé dans le désordre et ne produit rien d'exploitable ;
- il faut retrouver la clé XOR, qui n'est pas transmise telle quelle mais déductible de l'IMSI.

## Solution

### Énumérer le trafic
```bash
tshark -r rogue_tower.pcap -Y http -T fields \
       -e frame.number -e ip.dst -e http.host -e http.user_agent -e http.request.uri
tshark -r rogue_tower.pcap -Y 'http.user_agent contains "IMSI"' -T fields -e http.user_agent
tshark -r rogue_tower.pcap -Y 'udp.port == 55000' -V | grep -E 'PLMN|CELL'
```

### Extraire les segments
```bash
tshark -r rogue_tower.pcap -Y 'http.request.method == "POST"' \
       -T fields -e frame.number -e http.file_data > segments.txt
```

On garde `frame.number` : c'est lui qui donne l'ordre, et non l'ordre d'apparition des paquets dans
le fichier tel qu'on pourrait le croire après un tri par IP ou par flux.

### Reconstituer et casser le XOR
```python
import base64

segs = []
for line in open('segments.txt'):
    num, data = line.strip().split('\t', 1)
    segs.append((int(num), data.replace(':', '')))

blob = base64.b64decode(''.join(d for _, d in sorted(segs)))
```

Le XOR est appliqué avec une clé répétée. On n'a pas la clé, mais on connaît le début du clair : tout
flag commence par `picoCTF{`. C'est un **known-plaintext** de 8 octets — exactement la longueur de la
clé :

```python
ks = bytes(c ^ p for c, p in zip(blob, b'picoCTF{'))
print(ks)                      # doit être une suite de chiffres ASCII
pt = bytes(c ^ ks[i % len(ks)] for i, c in enumerate(blob))
print(pt.decode())
```

Le test de validité est immédiat : les 8 octets obtenus doivent être des chiffres ASCII (`0x30` à
`0x39`), ce qui confirme que la clé est bien la fin de l'IMSI, dont on a lu la valeur dans le
`User-Agent`.

### Pourquoi ça marche
Un XOR à clé répétée n'a aucune sécurité intrinsèque : sa faiblesse structurelle est que la clé est
plus courte que le message, donc chaque octet de clé est réutilisé. Dès qu'on connaît **huit octets
consécutifs de clair**, on obtient les huit octets de clé, et le reste du message tombe. Le choix de
`picoCTF{` comme known-plaintext n'est pas un privilège d'attaquant : c'est une information publique
— le format du flag est connu de tous. Utiliser un préfixe de format comme known-plaintext est une
technique générale, applicable dès qu'un protocole impose un en-tête fixe (magic bytes, `GET /`,
signature de fichier).

## Pièges
- **Ordre des segments** : concaténer dans l'ordre de capture des paquets ne fonctionne que si le
  fichier est déjà trié. Trier explicitement par numéro de trame (`frame.number`) est la seule
  méthode fiable.
- **Découpage de l'IMSI** : la clé est la **fin** de l'IMSI, pas son début. Le test « les octets
  récupérés sont des chiffres » tranche immédiatement ; s'il donne des caractères bizarres, on a
  pris le mauvais découpage ou la mauvaise longueur.
- **Longueur de clé** : si `picoCTF{` donne des chiffres mais que le reste du message est illisible,
  la clé n'est pas de 8 octets — essayer 4 ou 16, toujours en vérifiant le jeu de caractères obtenu.
- **`http.file_data` vide** : le corps est parfois réassemblé ; utiliser `-z follow,tcp,raw,<n>` sur
  le bon flux et vérifier que `segments.txt` n'est pas vide.

## Flag

Flag validé sur la plateforme (valeur non conservée).

## Scripts

- [`_z_714a.sh`](../../solve/714/_z_714a.sh)
- [`_z_714b.sh`](../../solve/714/_z_714b.sh)
- [`_z_714c.py`](../../solve/714/_z_714c.py)
- [`_z_714d.py`](../../solve/714/_z_714d.py)
- [`_z_714e.py`](../../solve/714/_z_714e.py)
- [`_z_714f.py`](../../solve/714/_z_714f.py)
- [`_z_714g.py`](../../solve/714/_z_714g.py)
- [`_z_714h.sh`](../../solve/714/_z_714h.sh)
- [`_z_714i.sh`](../../solve/714/_z_714i.sh)
- [`_z_714j.sh`](../../solve/714/_z_714j.sh)
- [`_z_714k.py`](../../solve/714/_z_714k.py)
- [`_z_714l.py`](../../solve/714/_z_714l.py)
