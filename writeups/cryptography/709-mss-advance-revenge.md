# 709 — MSS_ADVANCE Revenge

**Événement** : picoCTF 2026 · **Catégorie** : Cryptography

## Énoncé
`chall.py` et `output.txt` sont fournis. Le script implémente un schéma de partage de secret présenté
comme une variante de Shamir — un « modified Shamir » — et `MASTER_KEY` chiffre le flag en AES-CBC.

## Analyse

### Le schéma
`chall.py` construit un polynôme de degré 29 sur un corps premier `p` de 1024 bits, avec 30
coefficients `c_0 … c_29`. Particularité : les coefficients ne sont pas tirés au hasard, ils sont
dérivés les uns des autres par

```
c_(i+1) = SHA-256(c_i)
```

Chacun vaut donc environ **256 bits** dans un corps de 1024. Le coefficient de tête `c_0` **est**
`MASTER_KEY`, défini comme `sha256(flag)` interprété comme un entier.

### Le défaut : 20 points pour 30 inconnues
`output.txt` ne contient que **20 points** `(x_i, f(x_i))`. Le système linéaire modulo `p` est
sous-déterminé : il admet `p^10` solutions et l'algèbre linéaire classique ne conclut rien. C'est le
piège central — on a l'impression qu'il manque des données, et c'est vrai au sens strict.

Sauf que l'espace des solutions n'est pas homogène. Le vecteur `(c_0, …, c_29)` est **anormalement
court** : 256 bits par composante contre 1024 pour le module. Une solution tirée au hasard aurait des
composantes uniformes sur 1024 bits. Celle qu'on cherche est statistiquement minuscule : c'est le
profil exact d'une attaque par **réduction de réseau**.

## Solution

### 1. Construire le réseau
On écrit les 20 équations comme combinaisons entières des 30 inconnues, en absorbant l'arithmétique
modulaire par des variables d'écart multiples de `p`. Matrice entière de
`(m + n + 1) × (m + n + 1)` avec `m = 20`, `n = 30` :

- puissances `x_i^(n-1-j) mod p` dans les lignes d'équations ;
- `p · W` sur la diagonale des variables d'écart, avec `W = 2^512` ;
- `-f(x_i) · W` dans la dernière ligne.

Le poids `W` équilibre les ordres de grandeur : sans lui, les constantes de l'ordre de `p` écrasent
les coefficients utiles et LLL ne trouve rien d'exploitable.

### 2. Réduire avec LLL
```python
# SageMath
from sage.all import *

p   = ...        # premier de 1024 bits lu dans output.txt
pts = [...]      # 20 couples (x_i, f(x_i))
m, n = len(pts), 30
W = 2**512

M = matrix(ZZ, m + n + 1, m + n + 1)
for i, (x, y) in enumerate(pts):
    for j in range(n):
        M[i, j] = pow(x, n - 1 - j, p) * W
    M[i, n + i] = p * W           # variable d'écart de l'équation i
    M[i, -1]    = -y * W
for j in range(n):
    M[m + j, j] = 1               # identification des inconnues
M[-1, -1] = 1

R = M.LLL()
```

### 3. Extraire `MASTER_KEY`
Dans la matrice réduite, les lignes sont des vecteurs courts. On cherche les entrées dont la taille
binaire tombe entre **250 et 260 bits** : signature d'un digest SHA-256. Chaque candidat est converti
en 32 octets **big-endian**, puis testé comme clé AES.

```python
from Crypto.Cipher import AES

for row in R.rows():
    for v in row:
        a = abs(int(v))
        if a.bit_length() in range(250, 261):
            try:
                key = a.to_bytes(32, 'big')
                pt  = AES.new(key, AES.MODE_CBC, b'\x00' * 16).decrypt(ct)
            except Exception:
                continue
            if b'picoCTF' in pt:
                print(key.hex(), pt)
```

L'IV est de 16 octets à zéro, codé en dur dans `chall.py` : il n'a pas à être deviné.

### 4. Vérification
```bash
cat chall.py
cat output.txt
grep -nE 'def |%|pow|coeff|MASTER|share|range' chall.py   # 30 coefficients, 20 évaluations
```

### Pourquoi ça marche
LLL cherche des vecteurs plus courts que ce que la taille du module laisse attendre. Ici le vecteur
cible est court **par construction** : la chaîne de hachages impose des composantes de 256 bits, et
le poids `W` place ce vecteur à une norme nettement inférieure aux autres. Le défaut n'est donc pas
le nombre de points publiés, mais l'absence d'uniformité des coefficients : un Shamir correct tire
dans `[0, p[`, ce qui rend ce type d'attaque inopérant.

## Pièges
- **Re-hacher la clé** : `MASTER_KEY` est **déjà** un digest SHA-256. Un `sha256()` de plus donne un
  clair aléatoire. C'est l'erreur la plus coûteuse en temps.
- **Endianness** : entier → octets en big-endian, sur exactement 32 octets.
- **Fenêtre de bits** : exiger `== 256` rate les candidats dont le bit de tête est nul ; 250–260
  absorbe ce cas.
- **Poids `W`** : trop petit, les constantes dominent ; trop grand, les variables d'écart noient le
  vecteur court.
- **Un seul candidat** : plusieurs entrées peuvent tomber dans la plage, il faut toutes les tester.

## Flag

Flag validé sur la plateforme (valeur non conservée).
