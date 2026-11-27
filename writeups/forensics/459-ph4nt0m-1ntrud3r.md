# 459 — Ph4nt0m 1ntrud3r

**Événement** : picoCTF 2025 · **Catégorie** : Forensics · **Auteur** : non précisé dans les sources consultées

> Synthèse rédigée à partir des sources publiques listées en fin de fiche : ce challenge a été
> résolu côté CyLab Academy, mais le writeup d'origine n'a pas été conservé.

## Énoncé

Un « fantôme numérique » a exfiltré des données via un petit fichier de capture réseau
(`myNetworkTraffic.pcap`). Il faut remettre les paquets dans l'ordre chronologique, réassembler
les blobs Base64 de l'attaquant et les décoder pour révéler le message volé.

## Analyse

Triage :

```bash
capinfos myNetworkTraffic.pcap            # durée, nombre de paquets
tshark -r myNetworkTraffic.pcap -Y tcp \
  -T fields -e frame.number -e frame.time_epoch -e tcp.payload
```

La capture contient des segments TCP dont la charge utile est une **petite chaîne ASCII
Base64 terminée par `==`** : l'attaquant a découpé et encodé le message. Deux pièges :

1. Les paquets sont **hors ordre chronologique** dans le fichier. Trier par `frame.number`
   (ordre de capture sur disque) donne du charabia ; il faut trier par `frame.time_epoch`.
   L'ordre attendu sur la capture de référence est `9, 21, 17, 15, 20, 13, 8`.
2. Chaque fragment porte son propre padding `==`, donc la concaténation n'est pas un unique
   Base64 valide pour un décodeur strict (Python `b64decode` s'arrête ou produit du binaire
   après `picoCTF`). `base64 -d` de GNU redémarre à chaque padding et affiche tout.

## Solution

Extraction ordonnée puis décodage. Les sept fragments (donnés par la source publique, dans
l'ordre chronologique) :

```
cGljb0NURg==  ezF0X3c0cw==  bnRfdGg0dA==  XzM0c3lfdA==  YmhfNHJfOA==  ZTEwZTgzOQ==  fQ==
```

Concaténation puis décodage :

```bash
printf '%s' 'cGljb0NURg==ezF0X3c0cw==bnRfdGg0dA==XzM0c3lfdA==YmhfNHJfOA==ZTEwZTgzOQ==fQ==' | base64 -d
```

Contrôle de cohérence : le résultat doit commencer par `picoCTF{` ; sinon l'ordre des paquets
est faux, il faut re-trier. Le décodeur affiche les sept morceaux dans l'ordre :

```
picoCTF  {1t_w4s  nt_th4t  _34sy_t  bh_4r_8  e10e839  }
```

Alternative graphique : Wireshark → clic droit sur le premier paquet → **Follow → TCP Stream**.

## Flag

```
picoCTF{1t_w4snt_th4t_34sy_tbh_4r_8e10e839}
```

## Sources

- https://picoctfsolutions.com/picoctf-2025-ph4nt0m-1ntrud3r
- https://picoctfsolutions.com/posts/wireshark-pcap-ctf
