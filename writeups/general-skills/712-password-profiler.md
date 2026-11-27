# 712 — Password Profiler

**Événement** : picoCTF 2026 · **Catégorie** : General Skills

## Énoncé

Le fichier intercepté ne contient que le **SHA-1** d'un mot de passe — inexploitable directement,
puisqu'un hash est à sens unique. Le challenge livre aussi des informations personnelles sur la
cible. Trois fichiers : `userinfo.txt`, `hash.txt` et `check_password.py`. Il faut générer une
wordlist sur mesure, retrouver le mot de passe, et le script de vérification affiche le flag.

## Analyse

### Le matériau fourni
```bash
cat userinfo.txt
cat hash.txt
```

`userinfo.txt` contient exactement ce que les gens mettent dans leurs mots de passe :

- prénom : `Alice` ;
- nom : `Johnson` ;
- surnom : `AJ` ;
- date de naissance : `15-07-1990` ;
- nom du partenaire : `Bob` ;
- prénom de l'enfant : `Charlie`.

Ce n'est donc **pas** une attaque par dictionnaire générique. Une liste comme rockyou contient des
millions de mots, mais rien ne garantit que le bon y figure. Ici, l'énoncé fournit le profil : c'est
de l'OSINT appliqué aux mots de passe, c'est-à-dire la génération de combinaisons à partir de champs
personnels — exactement la méthode des attaques réelles contre des comptes ciblés.

### Une recherche exhaustive mais bornée
Un SHA-1 ne s'inverse pas, mais il se compare : pour chaque candidat `p`, on calcule
`sha1(p.encode()).hexdigest()` et on compare à `hash.txt`. Le coût est linéaire en nombre de
candidats, d'où l'intérêt de réduire l'espace au profil. Six champs plus les transformations usuelles
(casse, séparateurs, suffixes) donnent quelques milliers à quelques millions de candidats : très
faisable localement, à condition de ne pas partir du dictionnaire complet.

### L'outil : CUPP
**CUPP** (Common User Passwords Profiler) est l'outil de cette situation : il pose une série de
questions (prénom, nom, surnom, date de naissance, partenaire, enfant, animal, entreprise…) et
produit une wordlist combinant ces champs avec les mutations classiques. En mode interactif (`-i`), il
écrit un fichier du type `alice.txt`.

`check_password.py` est le harnais du challenge : il lit un fichier `passwords.txt` (un candidat par
ligne), calcule le SHA-1 et le compare. Il faut donc **renommer** la sortie de CUPP : le script
n'accepte pas de nom libre.

## Solution

### Mise en place
```bash
cat userinfo.txt
cat hash.txt
cat check_password.py
```

La lecture du script confirme deux choses : l'algorithme (SHA-1, non salé) et le nom attendu du
fichier (`passwords.txt`). Sans cette étape, on génère une wordlist correcte que le script ignore.

### Génération
```bash
# récupérer CUPP (dépôt Mebus/cupp), puis :
cd cupp
python3 cupp.py -i
```

Réponses à saisir, en reprenant `userinfo.txt` :

```
First Name: Alice
Surname: Johnson
Nickname: AJ
Birthdate (DDMMYYYY): 15071990
Partner's Name: Bob
Child's Name: Charlie
```

La date est demandée au format **`DDMMYYYY` sans séparateur** : `15071990`, et non `15-07-1990` ni
`150790`. CUPP concatène la chaîne telle quelle ; un mauvais format produit des candidats qui ne
correspondent à rien.

```bash
ls -l alice.txt          # sortie de CUPP
cp alice.txt ../passwords.txt
cd ..
```

### Recherche
```bash
python3 check_password.py
```

Le script parcourt `passwords.txt`, compare les SHA-1 et affiche le flag sur une correspondance. Le
mot de passe retrouvé est de la forme `Aj_15901990` : surnom `AJ`, séparateur `_`, et un bloc de
chiffres dérivé de la date de naissance, avec la casse du surnom modifiée (`Aj`, pas `AJ`).

```bash
python3 -c "import hashlib; print(hashlib.sha1(b'Aj_15901990').hexdigest())"
```

### Pourquoi ça marche
SHA-1 est un hachage **non salé** : le même mot de passe produit toujours le même condensat, et rien
d'autre n'entre dans le calcul. Il n'y a donc aucune défense contre un dictionnaire ciblé : la seule
protection serait un sel, ou un KDF lent (bcrypt, argon2), qui rendrait chaque test coûteux et ferait
échouer les tables précalculées. Ici la faiblesse est double : hash nu **et** espace de recherche
réduit par les informations personnelles. La wordlist ciblée transforme une recherche impossible en
quelques secondes de calcul.

## Pièges

- **Format de la date** : `DDMMYYYY` sans séparateur, sinon la wordlist ne contient pas le candidat.
- **Nom du fichier** : `check_password.py` lit `passwords.txt`, pas `alice.txt`.
- **Casse et séparateurs** : le mot de passe réel est `Aj`, pas `AJ`, et le `_` vient du générateur ;
  si rien ne sort, ajouter séparateurs et suffixes à la main.
- **Pas de sel** : le hash est nu ; inutile de lancer `hashcat` sur rockyou, le profil est fourni.

## Flag

Flag validé sur la plateforme (valeur non conservée).
