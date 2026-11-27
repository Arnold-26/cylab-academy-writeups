# 730 — bytemancy 3

**Événement** : picoCTF 2026 · **Catégorie** : General Skills

> Synthèse rédigée à partir des sources publiques listées en fin de fiche : ce challenge a été
> résolu côté CyLab Academy, mais le writeup d'origine n'a pas été conservé.

## Énoncé
« Can you conjure the right bytes? » Deux fichiers : `app.py` et le binaire `spellbook`. Il faut
reconstituer la charge utile exacte attendue.

## Analyse
`app.py` annonce : « I will name four procedures hidden inside spellbook. Each round, send me their
*raw* 4-byte addresses in little-endian form. » Les quatre fonctions sont `ember_sigil`,
`glyph_conflux`, `astral_spark`, `binding_word`, et le serveur en tire **trois** au hasard.

Tout repose sur le fait que `spellbook` est un ELF **32 bits, non-PIE et non strippé** : les adresses
des symboles sont donc fixes et lisibles dans la table des symboles. On envoie ensuite chaque adresse
en 4 octets bruts, en **little-endian**, sans passage par une représentation texte — d'où l'usage de
`p32()` et de `send()` plutôt que `sendline()`.

## Solution
```bash
cat app.py
file spellbook          # ELF 32-bit, not stripped, sans PIE
nm spellbook | grep -E "ember_sigil|glyph_conflux|astral_spark|binding_word"
```
Adresses publiées pour le binaire distribué :
```
08049176 T ember_sigil
0804919a T glyph_conflux
080491c1 T astral_spark
080491e3 T binding_word
```
Boucle pwntools : lire le prompt, extraire le nom demandé, envoyer `p32(adresse)` (4 octets, sans
`\n`), trois fois, puis lire le flag. Si le binaire était strippé, il faudrait retrouver les adresses
dans Ghidra/radare2.

## Flag
```
picoCTF{0bjdump_m4g1c_9ee35d3a}
```

## Sources
- https://picoctfsolutions.com/picoctf-2026-bytemancy-3 — page de solution picoCTF 2026 (non-PIE, `p32`, protocole 3 rounds)
- https://qiita.com/8omp/items/8e1aa38aeda96fa0ecb6 — writeup picoCTF 2026 General Skills (sortie `nm`, script, flag complet)
