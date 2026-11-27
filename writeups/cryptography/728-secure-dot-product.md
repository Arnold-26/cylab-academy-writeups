# 728 — Secure Dot Product

**Événement** : picoCTF 2026 · **Catégorie** : Cryptography

## Énoncé
Un service calcule des produits scalaires en impliquant du matériel de clé AES, et son concepteur
suppose la construction sûre. Le source `remote.py` est fourni : il faut retrouver la clé que le
service divulgue, puis déchiffrer le flag.

## Analyse

### Ce que fait le serveur
```bash
cat remote.py
```

Le service calcule le **produit scalaire** du vecteur envoyé avec la **clé AES de 32 octets**, puis
renvoie un **MAC SHA-512**. La clé est donc traitée comme un vecteur de 32 octets, et une requête
valide fournit une combinaison linéaire de ses octets.

C'est déjà une fuite : si l'on peut interroger l'oracle, le vecteur `(1, 0, …, 0)` retourne le
premier octet de la clé, `(0, 1, 0, …)` le deuxième, et ainsi de suite. La base canonique `e_1 … e_32`
livre la clé entière en 32 requêtes — le produit scalaire n'est pas un chiffrement, c'est une
**projection**, et 32 projections indépendantes reconstituent le vecteur.

### Le verrou : le MAC
Le service n'accepte pas n'importe quel vecteur : chaque requête doit porter un MAC valide. Le défaut
est dans la construction du MAC :

```
MAC = SHA512(secret || message)
```

C'est du **SHA-512 nu**, pas un HMAC. Une telle construction est vulnérable à l'attaque par
**extension de longueur** : connaissant `SHA512(secret || m)` et la longueur du secret, on calcule
`SHA512(secret || m || padding || m')` sans connaître `secret`. L'état interne de la fonction de
compression après `secret || m` est précisément ce que le hash divulgué représente : il suffit de
reprendre le calcul à partir de cet état.

L'attaque produit un message contenant le **glue padding** de SHA-512 (`\x80`, des zéros, la longueur
en bits). Détail décisif : le parseur du serveur **supprime les caractères non numériques**, donc le
padding est absorbé sans casser le parsing — ce qui ressemble à de la robustesse est le complice de
l'attaque.

## Solution

### Préparer l'outil
```bash
cat remote.py
pip install hlextend
```

`hlextend` implémente l'attaque pour SHA-1, SHA-256 et SHA-512 sans avoir à recoder le padding.

### Forger les MAC
```python
import hlextend

h = hlextend.new('sha512')
new_msg  = h.extend(append_data, known_msg, secret_length, known_hash)
new_hash = h.hexdigest()
```

Deux paramètres doivent être justes, sinon tout échoue silencieusement :

- **`secret_length`** : longueur du secret préfixé. La clé AES fait 32 octets, donc `32`. Une valeur
  fausse produit un padding de longueur incorrect et un MAC invalide.
- **l'ordre des arguments** : `extend(données_ajoutées, données_connues, longueur_secret, hash)`. Les
  inverser donne un message différent de celui dont on a calculé le hash.

### Interroger l'oracle
```python
from pwn import remote

def dot(vec, mac):
    r = remote(HOST, PORT)
    r.sendlineafter(b'>', vec.hex().encode() + b' ' + mac)
    return r.recvall()

key = []
for i in range(32):
    vec  = bytes(1 if j == i else 0 for j in range(32))
    resp = dot(vec, forge(vec))
    key.append(extract_int(resp))
```

Chaque réponse est une valeur numérique : le produit scalaire d'un vecteur de base avec la clé vaut
exactement l'octet de la clé à cette position. Il n'y a pas de calcul à faire, seulement une
extraction.

### Déchiffrer
```python
from Crypto.Cipher import AES
pt = AES.new(bytes(key), AES.MODE_CBC, iv).decrypt(ct)
```
L'IV et le chiffré sont fournis par le service (ou dérivés de `remote.py`).

### Variante : vecteurs non triviaux
Sans la base canonique, il faut inverser une matrice **modulo 256** (`Z/256Z`) en arithmétique
exacte : `numpy.linalg.solve` travaille en flottants et une erreur de `1e-16` suffit à produire un
octet faux.

### Pourquoi ça marche
Deux erreurs de conception se cumulent. La première est de croire qu'un MAC protège la
**confidentialité** : il garantit l'intégrité d'un message pour qui possède la clé, il ne masque rien.
Ici la réponse est une fonction linéaire du secret, donc l'oracle est une fuite et le MAC un simple
portillon. La seconde est le choix de `SHA512(secret || message)` au lieu de `HMAC-SHA512` : une
construction de Merkle-Damgård expose son état interne comme hash intermédiaire. HMAC a été conçu
précisément pour rendre cette attaque inopérante
(`H(K⊕opad || H(K⊕ipad || m))`). Le nom du challenge — « secure » — est l'ironie du sujet.

## Pièges
- **Longueur du secret** : `secret_length` doit valoir exactement 32. C'est la cause d'échec la plus
  fréquente : message forgé syntaxiquement correct, MAC invalide.
- **Parser qui filtre** : si le serveur rejette le message forgé, vérifier son traitement des octets
  non numériques. Ici il les supprime, ce qui rend le padding inoffensif.

## Flag

Flag validé sur la plateforme (valeur non conservée).
