# 286 — Packets Primer

**Événement** : picoCTF 2022 · **Catégorie** : Forensics

## Énoncé

« Téléchargez le fichier de capture réseau et utilisez un logiciel d'analyse de paquets pour trouver le flag. » Le fichier fourni est un `.pcap` de quelques kilo-octets.

## Analyse

Capture très courte : un nombre limité de trames, dont une seule conversation TCP utile. Le flag est transmis **en clair dans la charge utile applicative**, mais avec des espaces insérés entre chaque caractère. La chaîne apparaît donc comme `p i c o C T F { ... }` et ne correspond à aucun motif continu.

Deux observations :

1. Il n'y a rien à déchiffrer : le challenge teste la capacité à reconstituer un flux TCP applicatif, pas de la cryptographie.
2. Le bruit d'espaces est un anti-`strings` volontaire ; la parade est de reconstruire le flux, puis de supprimer les espaces.

Détail utile : `strings` ne reconstitue pas un flux, il sort les séquences imprimables dans l'ordre du fichier. Cela suffit ici, mais casse dès que la conversation est fragmentée sur plusieurs segments. `tshark` avec `follow,tcp` fait le vrai travail de réassemblage.

## Solution

### Approche Wireshark

1. Ouvrir le pcap.
2. Clic droit sur la première trame TCP → **Follow → TCP Stream**.
3. Le flux 0 contient la chaîne espacée ; on la copie.

### Approche ligne de commande

```bash
tshark -r capture.pcap -q -z follow,tcp,ascii,0
```

L'index `0` désigne le flux ; si plusieurs conversations existent, on les liste d'abord :

```bash
tshark -r capture.pcap -T fields -e tcp.stream | sort -u
```

Variante rapide quand la valeur est stockée telle quelle :

```bash
strings -n 4 capture.pcap | tr -d ' ' | grep -oE "[A-Za-z0-9_]*\{[^}]*\}"
```

`tr -d ' '` supprime tous les espaces, ce qui recolle les caractères ; le motif générique isole la valeur.

### Nettoyage

```python
import sys
s = sys.stdin.read().replace(" ", "").strip()
print(s)
```

Sur une chaîne déjà isolée, un simple `replace(" ", "")` suffit.

### Pourquoi ça marche

Le flag n'est pas dissimulé, il est simplement émis par l'application au milieu de son trafic. La difficulté est de remettre les octets dans l'ordre : `follow,tcp` recolle les segments dans l'ordre de leurs numéros de séquence, ce qu'un simple `cat` du fichier ne fait pas.

Les espaces ne servent qu'à casser les recherches textuelles naïves ; une fois le flux reconstitué et les espaces retirés, la chaîne apparaît telle quelle, sans traitement supplémentaire.

## Pièges

- **`grep` sur le motif continu** : le flag est espacé, aucun motif « préfixe + accolade » ne matche sans nettoyage.
- **Oublier `-a`** : sur un pcap, `grep` peut traiter le fichier comme binaire et n'afficher qu'un avertissement.
- **Lire le mauvais flux** : `follow,tcp,ascii,0` cible le flux 0 ; une capture avec du bruit DNS ou ARP peut en contenir d'autres.
- **Se fier à `strings` sur une capture fragmentée** : les morceaux apparaissent dans l'ordre du fichier, pas dans l'ordre du flux.
- **Garder les espaces dans la valeur** : le flag soumis doit être la chaîne recollée, pas la version espacée.
