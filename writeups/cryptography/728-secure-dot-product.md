# 728 — Secure Dot Product

**Événement** : picoCTF 2026 · **Catégorie** : Cryptography

> Synthèse rédigée à partir des sources publiques listées en fin de fiche : ce challenge a été
> résolu côté CyLab Academy, mais le writeup d'origine n'a pas été conservé.

## Énoncé
Un service de produit scalaire mêle du matériel de clé AES à un protocole interrogeable et suppose
sa conception sûre. Le source `remote.py` est fourni : il faut retrouver la clé qu'il divulgue.

## Analyse
Le serveur calcule le produit scalaire du vecteur envoyé avec la **clé AES de 32 octets**, puis
renvoie un **MAC SHA-512**. Le défaut est le même que dans toutes les constructions naïves : le MAC
est calculé comme `SHA512(secret || message)`, sans HMAC, donc vulnérable à une attaque par
**extension de longueur**. Chaque requête n'est acceptée que si le vecteur fourni est accompagné
d'un MAC valide : l'extension de longueur permet de forger des MAC valides pour des messages
prolongés sans connaître le secret.

Détail utile : le parseur du serveur supprime les caractères non numériques, ce qui aide à faire
passer le padding de collage (*glue padding*) produit par l'attaque.

Une fois les requêtes forgées acceptées, l'oracle de produit scalaire livre la clé : il suffit
d'envoyer les vecteurs de la base canonique (un `1` par position), chaque réponse étant directement
un octet de la clé. On reconstitue la clé AES et on déchiffre le chiffré fourni par le service.

## Solution
```bash
cat remote.py
pip install hlextend
```
- Collecter des couples (vecteur, hash) valides auprès du service.
- Forger les vecteurs étendus avec `hlextend` (`extend(data, known_message, secret_len, known_hash)`
  renvoie le message forgé complet).
- Interroger avec la base canonique `e_1 … e_32` : chaque réponse = un octet de clé.
- Reconstruire la clé, déchiffrer le ciphertext.
- Si l'on utilise des vecteurs non triviaux, résoudre le système **modulo 256** (SageMath) et non en
  flottants (`numpy.linalg.solve` accumule les erreurs).

## Flag
```
picoCTF{n0t_so_s3cure_.x_w1th_sh@512_1bb6154f}
```
(Valeur recopiée telle que publiée, y compris la graphie `.x`.)

## Sources
- https://picoctfsolutions.com/picoctf-2026-secure-dot-product — page de solution picoCTF 2026 (MAC SHA-512, `hlextend`, base canonique, algèbre mod 256)
- https://cyb3r-bo1.github.io/posts/picoCTF_2026_writeup/ — writeup picoCTF 2026 (enchaînement complet, flag)
