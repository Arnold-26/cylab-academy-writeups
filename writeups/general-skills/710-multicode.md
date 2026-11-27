# 710 — MultiCode

**Événement** : picoCTF 2026 · **Catégorie** : Général Skills

## Énoncé

« We intercepted a suspiciously encoded message, but it's clearly hiding a flag. No encryption, just
multiple layers of obfuscation. Can you peel back the layers and reveal the truth? »

Un seul fichier est fourni : `message.txt`.

## Analyse

### Reconnaître la première couche
```bash
cat message.txt | head -c 200
wc -c message.txt
```

Trois indices convergent vers du **base64** :

- la chaîne se termine par un ou plusieurs `=` (le remplissage) ;
- elle n'utilise que l'alphabet `A-Za-z0-9+/`, sans autre caractère ;
- sa longueur est un multiple de 4.

C'est cohérent avec l'énoncé : « no encryption », donc pas de clé à chercher, uniquement des
couches d'encodage successives. Chaque couche est un encodage **réversible sans secret** — c'est ce
qui rend le challenge résoluble à la main.

### Les couches, dans l'ordre
1. **Base64** → on obtient une longue suite de chiffres et de lettres `a`–`f`. C'est de
   l'hexadécimal : le jeu de caractères est réduit à 16 symboles.
2. **From Hex** (delimiter `None`, car la chaîne est d'un seul bloc sans séparateur) → apparaissent
   des séquences `%7B`, `%5F`. Ce sont des caractères **percent-encodés** : `%7B` est `{`, `%5F` est
   `_`. On est donc passé sur de l'URL encoding.
3. **URL Decode** → la chaîne prend la forme d'un flag : accolades, underscores, structure
   reconnaissable. Mais le contenu reste illisible — des lettres décalées, typiques d'un chiffrement
   par substitution.
4. **ROT13** → le texte devient du français/anglais lisible, et le flag apparaît en clair.

L'ordre est contraint par la nature des données : chaque décodage produit le format attendu par le
suivant. C'est ce qui permet de valider une couche avant de passer à la suivante — si la sortie ne
ressemble pas à de l'hexadécimal, on s'est trompé quelque part.

## Solution

### À la main, dans CyberChef
Recette, dans cet ordre exact :

```
From Base64  →  From Hex (delimiter: None)  →  URL Decode  →  ROT13
```

L'opération `From Hex` de CyberChef accepte un délimiteur ; avec des espaces ou des virgules en
entrée, la chaîne est interprétée de travers. Il faut explicitement `None` puisque la sortie base64
donne un bloc continu.

### Par script
```bash
cat message.txt
python3 - <<'EOF'
import base64, binascii, urllib.parse, codecs

s = open('message.txt').read().strip()
s = base64.b64decode(s).decode()
s = bytes.fromhex(s).decode()          # 'From Hex', bloc unique
s = urllib.parse.unquote(s)            # URL decode
s = codecs.decode(s, 'rot13')          # ROT13
print(s)
EOF
```

### Décodeur glouton
Pour une version générique, on boucle : à chaque tour, détecter l'encodage à partir du jeu de
caractères, appliquer le décodage, vérifier que la sortie est « plus lisible » que l'entrée, et
recommencer jusqu'à ce qu'aucune détection ne s'applique.

```python
import re, base64, urllib.parse, codecs

def looks_binary(s):  return set(s) <= {'0', '1'} and len(s) % 8 == 0
def looks_hex(s):     return re.fullmatch(r'[0-9a-fA-F]+', s) and len(s) % 2 == 0
def looks_b64(s):     return re.fullmatch(r'[A-Za-z0-9+/]+={0,2}', s) and len(s) % 4 == 0
def looks_url(s):     return '%' in s
```

L'**ordre des tests compte** : le binaire (uniquement des `0` et des `1`) doit être testé avant
l'hexadécimal, qui en est un sur-ensemble. Sinon une chaîne binaire est décodée comme de l'hexa et
produit des octets aléatoires. Même remarque pour base64, qui est un sur-ensemble très large : il
faut le tester en dernier, quand aucune détection plus spécifique n'a fonctionné.

### Pourquoi ça marche
Aucune de ces transformations n'ajoute d'entropie : base64, hexadécimal et percent-encoding sont des
**bijections** sur leur domaine, et ROT13 est une involution (l'appliquer deux fois redonne
l'original). Empiler des encodages ne protège donc rien — cela ne fait que déplacer l'information
dans un alphabet différent. Le seul « secret » est l'**ordre** des couches, et cet ordre est
entièrement déductible : chaque couche produit un alphabet reconnaissable qui désigne la suivante.
C'est la différence de fond avec un chiffrement, où la clé est indispensable même en connaissant
l'algorithme.

## Pièges

- **Le délimiteur de `From Hex`** : en laissant la valeur par défaut (espace), CyberChef ne décode
  qu'une partie de la chaîne, ou rien. Il faut `None`.
- **Le `=` final** : c'est du padding base64, pas un caractère du message. Le conserver lors des
  manipulations suivantes n'a pas d'importance tant qu'on décode la totalité de la chaîne.
- **Ordre de détection** : hexadécimal avant binaire, base64 après tout le reste. Un décodeur
  glouton mal ordonné transforme une chaîne binaire en bouillie hexadécimale.
- **ROT13 vs ROT-n** : ici c'est bien 13, involution ; tester ROT47 ou un ROT arbitraire ne donne
  rien de lisible et fait perdre du temps.
- **Ne pas confondre les couches** : `%7B` est du percent-encoding, pas du HTML entity ni du base64.
  Chercher un `&` ou un `;` oriente vers la mauvaise piste.
