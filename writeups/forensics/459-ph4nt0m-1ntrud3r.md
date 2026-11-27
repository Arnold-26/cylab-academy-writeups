# 459 — Ph4nt0m 1ntrud3r

**Événement** : picoCTF 2025 · **Catégorie** : Forensics

## Énoncé

Un « fantôme numérique » a exfiltré des données via un petit fichier de capture réseau (`myNetworkTraffic.pcap`). Il faut remettre les paquets dans l'ordre chronologique, réassembler les blobs Base64 de l'attaquant et les décoder pour révéler le message volé.

## Analyse

### Triage

```bash
capinfos myNetworkTraffic.pcap
tshark -r myNetworkTraffic.pcap -Y tcp -T fields -e frame.number -e frame.time_epoch -e tcp.payload
```

`capinfos` donne la durée et le nombre de paquets ; la seconde commande liste, pour chaque segment, son numéro de capture, son horodatage et sa charge utile.

Les charges utiles sont de **petites chaînes ASCII Base64 terminées par `==`** : l'attaquant a découpé et encodé le message. Deux pièges :

1. Les paquets sont **hors ordre chronologique** dans le fichier. Trier par `frame.number` (ordre de capture sur disque) donne du charabia ; il faut trier par `frame.time_epoch`. L'ordre chronologique observé sur la capture est `9, 21, 17, 15, 20, 13, 8`.
2. Chaque fragment porte son propre padding `==`, donc la concaténation n'est pas un unique Base64 valide pour un décodeur strict : Python `b64decode` s'arrête ou produit du binaire après le préfixe. `base64 -d` de GNU redémarre à chaque padding et affiche tout.

### Pourquoi les numéros de trame trompent

Une capture peut être réassemblée depuis plusieurs sources : les numéros de trame suivent l'ordre d'écriture dans le fichier, pas l'ordre d'émission. `frame.time_epoch` vient de l'horodatage du paquet et reflète l'ordre réel. C'est la seule clé de tri fiable sur ce fichier.

## Solution

### 1. Extraire et trier

```bash
tshark -r myNetworkTraffic.pcap -Y 'tcp.len > 0' -T fields -e frame.number -e frame.time_epoch -e tcp.payload \
  | sort -k2,2g | cut -f3 | tr -d '\n' | xxd -r -p > blobs.b64
```

`sort -k2,2g` trie sur l'horodatage, `cut -f3` garde la charge utile en hexadécimal, `xxd -r -p` la reconvertit en ASCII, et `tr -d '\n'` recolle le tout sur une ligne. Le filtre `tcp.len > 0` évite les paquets de contrôle, qui n'ont pas de charge utile.

### 2. Décoder

```bash
base64 -d blobs.b64
```

Le décodeur tolérant de GNU redémarre après chaque `==` et produit le message complet.

En Python, on décode fragment par fragment pour éviter le même écueil :

```python
import base64, re
data = open('blobs.b64','rb').read()
for m in re.finditer(rb'[A-Za-z0-9+/]{4,}={0,2}', data):
    print(base64.b64decode(m.group()).decode(), end='')
print()
```

### 3. Contrôle de cohérence

Le résultat doit commencer par le préfixe de flag de l'événement. Sinon, l'ordre des paquets est faux : on re-trie, ou on vérifie que le filtre n'a pas laissé passer des paquets sans données.

Alternative graphique : Wireshark → clic droit sur le premier paquet → **Follow → TCP Stream**. Attention, le suivi reconstruit le flux d'une connexion, pas la séquence chronologique inter-connexions de l'exfiltration.

### Pourquoi ça marche

Chaque fragment est un Base64 autonome : le message complet est la concaténation des textes décodés, et l'ordre chronologique est la seule information qui donne la bonne séquence. Le padding par fragment est volontaire, il empêche un décodeur naïf de reconstruire un Base64 unique à partir du fichier brut.

## Pièges

- **Trier par `frame.number`** : c'est l'ordre du fichier, pas celui des paquets.
- **Concaténer puis `b64decode` strict** : le padding intermédiaire casse le décodage.
- **Filtre trop large** : les paquets sans charge utile ajoutent des lignes vides dans le flux.
- **`sort` sans `-g`** : les horodatages sont triés comme des chaînes et l'ordre est cassé.
- **Perdre les fins de ligne** : `tr -d '\n'` doit s'appliquer avant `xxd -r -p`, pas après.
- **Négliger le préfixe** : un message qui ne commence pas par l'en-tête attendu signifie un mauvais ordre, pas un mauvais décodage.
