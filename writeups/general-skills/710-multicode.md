# 710 — MultiCode

**Événement** : picoCTF 2026 · **Catégorie** : General Skills

> Synthèse rédigée à partir des sources publiques listées en fin de fiche : ce challenge a été
> résolu côté CyLab Academy, mais le writeup d'origine n'a pas été conservé.

## Énoncé
« We intercepted a suspiciously encoded message, but it's clearly hiding a flag. No encryption,
just multiple layers of obfuscation. Can you peel back the layers and reveal the truth? » Le
fichier `message.txt` est fourni.

## Analyse
Le message se termine par des `=` et n'utilise que l'alphabet `A-Za-z0-9+/` : c'est du **base64**.
Chaque couche annonce la suivante :

1. **Base64** → on obtient une longue suite de chiffres et de lettres `a`-`f` (hexadécimal) ;
2. **From Hex** (delimiter `None`, la chaîne est d'un seul bloc) → apparaissent des `%7B`, `%5F` :
   de l'**URL encoding** ;
3. **URL Decode** → une chaîne à la forme d'un flag mais illisible ;
4. **ROT13** → le flag en clair.

## Solution
À la main dans CyberChef (recette `From Base64` → `From Hex` → `URL Decode` → `ROT13`), ou par
script avec un décodeur glouton qui détecte l'encodage à partir du jeu de caractères :
```bash
cat message.txt
python3 - <<'EOF'
# boucle : essayer base64 / hex / url / rot13, appliquer la première détection qui réussit
EOF
```
L'ordre de détection compte : le binaire (uniquement 0/1) doit être testé avant l'hexadécimal, qui
en est un sur-ensemble.

## Flag
```
picoCTF{nested_enc0ding_1d75be63}
```
Le suffixe hexadécimal final varie selon l'instance : on trouve aussi `nested_enc0ding_f3a24f73`
dans un autre writeup. Le corps `nested_enc0ding` est stable.

## Sources
- https://picoctfsolutions.com/picoctf-2026-multicode — page de solution picoCTF 2026 (ordre des couches, script de décodage)
- https://qiita.com/8omp/items/8e1aa38aeda96fa0ecb6 — writeup picoCTF 2026 General Skills (flag complet)
- https://shukularuni.neocities.org/guide/ctf/picoctf/general/MultiCode.html — guide CyLab Academy/picoCTF (variante du flag)
