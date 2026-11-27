# 493 — ChaCha Slide

**Événement** : picoCTF 2025 · **Catégorie** : Cryptography

## Énoncé

Un service (`nc verbal-sleep.picoctf.net <port>`) affiche le source Python du challenge, puis deux couples `(ciphertext, tag)` produits par **ChaCha20-Poly1305**, et attend un troisième blob de notre choix à déchiffrer et vérifier. Si le message déchiffré contient la phrase objectif `But it's only secure if used correctly!`, le serveur imprime le flag.

Extrait du source :

```python
key   = shasum(shasum(secrets.token_bytes(32) + flag.encode()))
nonce = secrets.token_bytes(12)          # un seul nonce pour tout
messages = ["Did you know that ChaCha20-Poly1305 is an authenticated encryption algorithm?",
            "That means it protects both the confidentiality and integrity of data!"]
```

## Analyse

### Nonce réutilisé

ChaCha20 est un chiffre de flux : `C = P XOR keystream(key, nonce)`. Les deux messages sont chiffrés avec **la même clé et le même nonce**, donc le keystream est identique — et le nonce est concaténé en clair à la fin de chaque blob (`ciphertext || tag || nonce`).

Conséquences :

1. `C1 XOR C2 = P1 XOR P2` : c'est un two-time pad. Les deux plaintexts étant connus (constantes du source), on récupère le keystream directement par `ks = C1 XOR P1`.
2. Poly1305 utilise une clé one-time `(r, s)` dérivée du même nonce : elle est donc identique pour les deux tags. En soustrayant les deux équations de tag, `s` s'élimine et il reste une **équation polynomiale en `r`** dans `GF(2^130 - 5)`.

### Ce que Poly1305 calcule

Le tag vaut `(poly(M) + s) mod 2^128`, où `poly` évalue le message par blocs de 16 octets, chaque bloc complété par un octet `0x01` puis multiplié par `r` modulo `2^130 - 5`. `r` est « clampé » à la génération : certains bits hauts sont forcés à zéro, ce qui réduit l'espace des candidats.

## Solution

### Étape 1 — keystream et chiffrement du message forgé

```python
keystream = bytes(a ^ b for a, b in zip(c1, m1))          # m1 connu
m3 = b"But it's only secure if used correctly!"
c3 = bytes(a ^ b for a, b in zip(keystream, m3))
```

### Étape 2 — récupération de `(r, s)`

```
P(r) = poly_eval(r, M1) - poly_eval(r, M2) - (tag1 - tag2)   mod (2^130 - 5)
```

`poly_eval` est l'évaluation Poly1305 : blocs de 16 octets, chacun complété par un octet `0x01`, puis réduits modulo `2^130 - 5`. On cherche les racines de `P` (Sage `.roots()`, ou Cantor-Zassenhaus en pur Python), on filtre les candidats par le **clamp** Poly1305 (bits hauts de `r` à zéro), puis `s = tag1 - poly_eval(r, M1) mod 2^128`.

### Étape 3 — forge du tag

```python
tag3 = (poly_eval(r, M3) + s) % (1 << 128)
blob = c3 + tag3.to_bytes(16, 'little') + nonce
```

On envoie `c3 || tag3 || nonce` au service ; s'il accepte, il affiche le flag.

### Pourquoi ça marche

Le tag authentifie un message sous une clé qui dépend du nonce ; réutiliser le nonce réutilise la clé d'authentification. Avec deux messages connus, la différence des tags annule `s` et laisse un polynôme dont les racines contiennent le vrai `r`. Une fois `r` et `s` connus, on calcule un tag valide pour n'importe quel message, sans jamais connaître la clé de chiffrement.

## Pièges

- **Chercher les racines dans les entiers** : il faut travailler dans `GF(2^130-5)`, sinon aucune racine n'apparaît.
- **Oublier l'octet `0x01` par bloc** : l'évaluation ne correspond plus au tag et la recherche échoue.
- **Oublier la réduction finale modulo `2^128`** : le tag fait 130 bits et le serveur le rejette.
- **Ne pas filtrer par le clamp** : plusieurs racines existent, une seule correspond à un `r` valide.
- **Se tromper d'endianness** : le nonce et le tag se concatènent en little-endian dans cette implémentation ; on vérifie sur les blobs reçus.
- **Chiffrer un message trop long** : le keystream n'est récupérable que sur la longueur des messages connus ; la phrase objectif est plus courte, donc sans problème.

## Flag

Flag validé sur la plateforme (valeur non conservée).
