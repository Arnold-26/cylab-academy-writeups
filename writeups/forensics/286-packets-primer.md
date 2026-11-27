# 286 — Packets Primer

**Événement** : picoCTF 2022 · **Catégorie** : Forensics · **Auteur** : non précisé dans les sources consultées

> Synthèse rédigée à partir des sources publiques listées en fin de fiche : ce challenge a été
> résolu côté CyLab Academy, mais le writeup d'origine n'a pas été conservé.

## Énoncé

« Téléchargez le fichier de capture réseau et utilisez un logiciel d'analyse de paquets pour
trouver le flag. » Le fichier fourni est un `.pcap` de quelques kilo-octets.

## Analyse

Capture très courte : un nombre limité de trames, dont une seule conversation TCP utile.
Le flag est transmis **en clair dans la charge utile applicative**, mais avec des espaces
insérés entre chaque caractère — la chaîne apparaît donc comme
`p i c o C T F { ... }` et ne matche pas un `grep picoCTF` naïf.

Deux observations importantes :

1. Il n'y a rien à déchiffrer : le challenge teste la capacité à reconstituer un flux TCP
   applicatif, pas de la cryptographie.
2. Le bruit d'espaces est un anti-`strings` volontaire ; la parade est de reconstruire le flux
   puis de supprimer les espaces.

## Solution

Approche Wireshark :

1. Ouvrir le pcap, clic droit sur la première trame TCP → **Follow → TCP Stream**.
2. Le flux 0 contient la chaîne espacée ; la copier.

Approche ligne de commande (reproductible) :

```bash
tshark -r capture.pcap -q -z follow,tcp,ascii,0
# ou, plus brutal :
strings -n 4 capture.pcap | tr -d ' ' | grep -o 'picoCTF{[^}]*}'
```

Nettoyage du bruit :

```python
"p i c o C T F { p 4 c k 3 7 _ 5 h 4 r k _ b 9 d 5 3 7 6 5 }".replace(" ", "")
```

## Flag

```
picoCTF{p4ck37_5h4rk_b9d53765}
```

## Sources

- https://ctftime.org/writeup/33097
- https://ctftime.org/writeup/33111
- https://picoctfsolutions.com/picoctf-2022-packets-primer
