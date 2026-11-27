# 362 — PcapPoisoning

**Événement** : picoCTF 2023 · **Catégorie** : Forensics

## Énoncé

« Et si on jouait à cache-cache ? Téléchargez ce fichier et trouvez le flag. » Le fichier fourni est `trace.pcap`.

## Analyse

Le nom du challenge (« poisoning ») suggère une injection de paquets TCP, mais la recherche est beaucoup plus simple : le flag circule **en clair dans la charge utile** d'un unique segment, sans encodage ni chiffrement.

Deux chemins équivalents :

- **Wireshark** : filtre d'affichage `tcp.payload contains "pico"` ; un seul paquet remonte (le paquet n°507) et le flag apparaît dans la colonne ASCII du volet « Packet bytes ».
- **`strings`** : les octets du pcap contiennent la chaîne telle quelle, donc `strings trace.pcap | grep pico` suffit. C'est le triage à faire *avant* d'ouvrir une interface graphique.

Le filtre `tcp.payload contains` travaille sur un segment isolé : si le message était réparti sur plusieurs paquets, il ne remonterait pas. D'où le second réflexe, réassembler le flux avant de conclure.

Un pcap est un conteneur d'enregistrements, pas un format chiffré : si l'application écrit la valeur en clair, elle est présente telle quelle dans le fichier, à l'endroit exact de la charge utile. C'est ce qui explique l'efficacité du triage textuel avant toute analyse protocolaire.

## Solution

### Triage rapide

```bash
file trace.pcap
strings -n 6 trace.pcap | grep -i pico
```

### Recherche ciblée

```bash
tshark -r trace.pcap -Y "tcp.payload contains \"pico\"" -T fields -e frame.number -e tcp.payload
```

La charge utile sort en hexadécimal ; on la reconvertit en texte :

```bash
echo "<hex>" | xxd -r -p
```

### Wireshark

Filtre d'affichage `tcp.payload contains "pico"`, puis volet « Packet bytes » : la colonne ASCII affiche la chaîne. Le flag occupe la fin de la charge utile, collé au reste du message applicatif.

### Pourquoi ça marche

Le flag est écrit par l'application elle-même, en clair, dans un segment TCP. Rien ne le protège : ni TLS, ni encodage, ni découpage volontaire. Le seul travail est de le localiser, soit par recherche binaire, soit par filtre d'affichage.

### Contrôle avec tcpdump

```bash
tcpdump -r trace.pcap -A -n | grep -A 2 -i pico
```

`-A` affiche la charge utile en ASCII : c'est une seconde lecture indépendante de `strings` et de Wireshark. Les trois méthodes doivent donner la même valeur, ce qui évite de coller une chaîne tronquée.

## Pièges

- **Chercher un empoisonnement** : le nom est un leurre ; il n'y a pas d'injection ARP ou DNS à exploiter.
- **`strings` sans `-n`** : la longueur minimale par défaut peut noyer la valeur dans du bruit ; on ajuste le seuil.
- **Filtre `contains` sur le payload** : il ne matche que dans un seul segment ; un flag fragmenté exige `Follow → TCP Stream`.
- **Se tromper de colonne** : le volet hexadécimal et la colonne ASCII se lisent côte à côte ; la valeur est dans l'ASCII, pas dans les offsets.
- **Coller des octets parasites** : la chaîne peut être suivie d'octets non imprimables ; on ne garde que le motif jusqu'à l'accolade.
- **Oublier `-n` avec `tcpdump`** : sans résolution de noms, la sortie reste lisible et rapide.
- **Confondre charge utile et en-tête** : le filtre porte sur `tcp.payload` ; `tcp contains` cherche dans tout le segment, en-têtes compris.

## Flag

Flag validé sur la plateforme (valeur non conservée).
