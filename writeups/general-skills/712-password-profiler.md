# 712 — Password Profiler

**Événement** : picoCTF 2026 · **Catégorie** : General Skills

> Synthèse rédigée à partir des sources publiques listées en fin de fiche : ce challenge a été
> résolu côté CyLab Academy, mais le writeup d'origine n'a pas été conservé.

## Énoncé
Un fichier intercepté ne contient que le **SHA-1** d'un mot de passe. Des informations personnelles
sur la cible sont fournies : `userinfo.txt`, `hash.txt` et `check_password.py`. Il faut générer une
wordlist sur mesure et retrouver le mot de passe correspondant au hash.

## Analyse
`userinfo.txt` contient exactement le matériau qu'utilisent les gens dans leurs mots de passe :
prénom (`Alice`), nom (`Johnson`), surnom (`AJ`), date de naissance (`15-07-1990`), nom du
partenaire (`Bob`), prénom de l'enfant (`Charlie`). Il ne s'agit donc pas d'une attaque par
dictionnaire générique mais d'un profil OSINT : on génère les combinaisons à partir de ces champs.

L'outil adapté est **CUPP** (Common User Passwords Profiler), en mode interactif (`-i`) : il produit
un fichier du type `alice.txt`. `check_password.py` est fourni avec le challenge et lit un fichier
`passwords.txt` : il suffit de renommer la sortie de CUPP.

## Solution
```bash
cat userinfo.txt
cat hash.txt
cat check_password.py
git clone https://github.com/Mebus/cupp.git
cd cupp && python3 cupp.py -i      # saisir les champs de userinfo.txt
# CUPP écrit alice.txt
cp alice.txt ../passwords.txt
cd .. && python3 check_password.py
```
D'après les writeups, la date est demandée au format `DDMMYYYY` sans séparateur (`15071990`) et le
mot de passe trouvé est de la forme `Aj_15901990`. `check_password.py` affiche le flag dès qu'un
candidat correspond au SHA-1.

## Flag
```
picoCTF{Aj_15901990}
```
Ce flag est dérivé du mot de passe trouvé, il ne comporte donc pas de suffixe aléatoire.

## Sources
- https://picoctfsolutions.com/picoctf-2026-password-profiler — page de solution picoCTF 2026 (CUPP, `check_password.py`)
- https://qiita.com/8omp/items/8e1aa38aeda96fa0ecb6 — writeup picoCTF 2026 General Skills (contenu de `userinfo.txt`, flag complet)
- https://shukularuni.neocities.org/guide/ctf/picoctf/general/Password_Profiler.html — guide picoCTF/CyLab Academy sur le même challenge
