# 717 — Silent Stream

**Événement** : picoCTF 2026 · **Catégorie** : Reverse Engineering

## Énoncé

« We recovered a suspicious packet capture file that seems to contain a transferred file. The sender
was kind enough to also share the script they used to encode and send it. Can you reconstruct the
original file? »

Deux fichiers : `packets.pcap` et `encrypt.py`. L'encodeur est fourni, ce qui déplace tout l'enjeu
vers l'extraction du bon flux dans la capture.

## Analyse

### Lire l'encodeur
```bash
cat encrypt.py
```

Le script montre un encodage par **décalage additif** : chaque octet de l'original est décalé de 42
modulo 256.

```python
encoded = (original + 42) % 256
```

C'est un chiffrement de César appliqué aux octets, avec une clé de 1 octet. Le fichier encodé n'a
pas été emballé dans un protocole : il a simplement été envoyé tel quel sur le réseau, et la capture
en contient les paquets.

### Le piège : le PCAP contient plusieurs flux
```bash
capinfos packets.pcap
tshark -r packets.pcap -q -z conv,tcp
```

La capture contient plusieurs communications TCP entremêlées. La tentation est de faire
`tshark -r packets.pcap -T fields -e data` ou un `tcpdump -w` sur tout le fichier, puis de décoder
l'ensemble : cela produit des déchets, parce que les octets de flux différents sont concaténés dans
l'ordre de capture, pas dans l'ordre de chaque flux. Un fichier reconstitué à partir de plusieurs
flux n'est pas un fichier.

La bonne méthode est d'isoler **un seul flux TCP**, celui qui transporte le fichier, et de le lire
intégralement. Dans Wireshark : clic droit sur un paquet du flux → `Follow` → `TCP Stream`,
affichage en **`Raw`**, puis copie du contenu hexadécimal. L'affichage `ASCII` perdrait les octets
non imprimables, or ici tout le fichier est binaire : c'est le second piège.

### Identifier le flux utile
Le flux porteur est reconnaissable à sa taille : c'est le plus volumineux, et il contient une longue
suite d'octets sans structure ASCII. Un coup d'œil aux premiers octets décodés confirme le type de
fichier — un en-tête JPEG commence par `FF D8 FF`. Comme l'encodage est un simple décalage, les
premiers octets encodés valent `FF+42 = 0x29 (mod 256)` : une signature repérable sans décoder.

## Solution

### Extraction du flux
```bash
wireshark packets.pcap &
# clic droit sur un paquet du bon flux -> Follow -> TCP Stream
# "Show data as: Raw", puis copier le contenu hexadécimal dans silentstream.hex
```

En ligne de commande, l'équivalent :

```bash
tshark -r packets.pcap -q -z follow,tcp,raw,0 > stream.txt
# la sortie contient l'offset, les octets hexadécimaux et leur rendu ASCII
```

### Décodage
```bash
xxd -r -p silentstream.hex decoded.bin

python3 - <<'EOF'
data = open('decoded.bin','rb').read()
open('recovered','wb').write(bytes((b - 42) % 256 for b in data))
EOF

file recovered
mv recovered decoded.jpg
xdg-open decoded.jpg
```

Le décodage est l'inverse arithmétique exact du script fourni : `original = (encoded - 42) % 256`.
Le modulo est essentiel — sans lui, les octets inférieurs à 42 produiraient des valeurs négatives et
Python écrirait un `ValueError` au moment de construire le `bytes`.

### Le résultat
`file` identifie une image **JPEG** de 800×500. Sur une image blanche, le flag est écrit en rouge au
milieu. Il suffit de le lire.

### Pourquoi ça marche
Un décalage additif modulo 256 est une substitution monoalphabétique sur l'ensemble des 256 octets.
Il préserve l'ordre relatif des octets mais détruit les signatures de format — d'où l'impression
d'avoir affaire à des données aléatoires. Il ne résiste à rien : l'opération est bijective, donc
inversible sans clé si la clé est connue, et ici le script la donne. Même sans le script, une
signature de fichier aurait suffi : en testant les 256 décalages possibles sur les premiers octets et
en cherchant `FF D8 FF`, on retrouve 42 immédiatement. C'est la faiblesse fondamentale des
chiffrements à décalage : l'espace de clés est minuscule et vérifiable par force brute en quelques
millisecondes.

## Pièges

- **Ne pas dumper tout le PCAP** : les flux s'entremêlent et le résultat n'est pas un fichier. Il
  faut isoler un flux avant d'extraire les données.
- **Affichage ASCII** : `Follow → TCP Stream` doit être en `Raw`. En ASCII, les octets non
  imprimables sont remplacés et le fichier est corrompu de façon irréversible.
- **`xxd -r -p`** exige un hexadécimal pur, sans offset ni colonnes. Si le copier-coller contient des
  adresses ou des espaces de mise en forme, les octets sont décalés et le JPEG ne s'ouvre pas.
- **Modulo 256** : oublier le `% 256` fait planter le script au premier octet inférieur à 42.
- **Sens du décalage** : `+42` à l'encodage, donc `-42` au décodage. Inverser les deux donne une image
  bruitée qui ressemble à un échec d'extraction.
- **En-tête du JPEG** : si `file` ne reconnaît rien, vérifier les 3 premiers octets décodés. Ce sont
  eux qui valident l'extraction, avant même de regarder l'image.
