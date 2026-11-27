# 493 — ChaCha Slide

**Événement** : picoCTF 2025 · **Catégorie** : Cryptography · **Auteur** : non précisé dans les sources consultées

> Synthèse rédigée à partir des sources publiques listées en fin de fiche : ce challenge a été
> résolu côté CyLab Academy, mais le writeup d'origine n'a pas été conservé.

## Énoncé

Un service (`nc verbal-sleep.picoctf.net <port>`) affiche le source Python du challenge, puis
deux couples `(ciphertext, tag)` produits par **ChaCha20-Poly1305**, et attend un troisième
blob de notre choix à déchiffrer/vérifier. Si le message déchiffré contient la phrase objectif
`But it's only secure if used correctly!`, le serveur imprime le flag.

Extrait du source :

```python
key   = shasum(shasum(secrets.token_bytes(32) + flag.encode()))
nonce = secrets.token_bytes(12)          # un seul nonce pour tout
messages = ["Did you know that ChaCha20-Poly1305 is an authenticated encryption algorithm?",
            "That means it protects both the confidentiality and integrity of data!"]
```

## Analyse

ChaCha20 est un chiffre de flux : `C = P XOR keystream(key, nonce)`. Les deux messages sont
chiffrés avec **la même clé et le même nonce**, donc le keystream est identique — et le nonce
est concaténé en clair à la fin de chaque blob (`ciphertext || tag || nonce`).

Conséquences :

1. `C1 XOR C2 = P1 XOR P2` : deux-time pad. Les deux plaintexts étant connus (constantes du
   source), on récupère le keystream directement par `ks = C1 XOR P1`.
2. Poly1305 utilise une clé one-time `(r, s)` dérivée du même nonce : elle est donc
   identique pour les deux tags. En soustrayant les deux équations de tag, `s` s'élimine et
   il reste une **équation polynomiale en `r`** dans `GF(2^130 - 5)`.

## Solution

Étape 1 — keystream et chiffrement du message forgé :

```python
keystream = bytes(a ^ b for a, b in zip(c1, m1))          # m1 connu
m3 = b"But it's only secure if used correctly!"
c3 = bytes(a ^ b for a, b in zip(keystream, m3))
```

Étape 2 — récupération de `(r, s)` par recherche de racines :

```
P(r) = poly_eval(r, M1) - poly_eval(r, M2) - (tag1 - tag2)   mod (2^130 - 5)
```

`poly_eval` est l'évaluation Poly1305 : blocs de 16 octets, chacun complété par un octet
`0x01`, puis réduits modulo `2^130 - 5`. On cherche les racines de `P` (Sage
`.roots()`, ou Cantor-Zassenhaus en pur Python), on filtre les candidats par le **clamp**
Poly1305 (bits hauts de `r` à zéro), puis `s = tag1 - poly_eval(r, M1) mod 2^128`.

Étape 3 — forge du tag : `tag3 = (poly_eval(r, M3) + s) mod 2^128`, puis envoi de
`c3 || tag3 || nonce`.

Implémentation de référence utilisée par le writeup de cbarkr :
`chacha_poly1305_forgery_attack()` de `tl2cents/AEAD-Nonce-Reuse-Attacks`.

Pièges classiques : faire la recherche de racines dans les entiers au lieu du corps
`GF(2^130-5)` (aucune racine), oublier l'octet `0x01` par bloc, ou oublier la réduction
finale modulo `2^128` (tag sur 130 bits ⇒ rejet).

## Flag

Le serveur imprime le flag si le tag forgé est accepté. Cette valeur n'est **pas publiée** :
les sources publiques la retirent explicitement (« flag withdrawn »), le challenge étant
relié à une instance et à un `flag.txt` propres au serveur.

```
picoCTF{...}   # valeur non publiée — à récupérer sur l'instance
```

## Sources

- https://blog.cbarkr.com/ctf/picoCTF/2025/ChaChaSlide
- https://picoctfsolutions.com/picoctf-2025-chacha-slide
- https://datatracker.ietf.org/doc/html/rfc7539#section-2.5
