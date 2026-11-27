# 742 — bytemancy 0

**Événement** : picoCTF 2026 · **Catégorie** : General Skills

> Synthèse rédigée à partir des sources publiques listées en fin de fiche : ce challenge a été
> résolu côté CyLab Academy, mais le writeup d'origine n'a pas été conservé.

## Énoncé

> Can you conjure the right bytes? Download `app.py` and recover the exact input the server expects.

Un service TCP demande une saisie précise ; le code source `app.py` est fourni avec le challenge.
La bannière annonce : « Send me ASCII DECIMAL 101, 101, 101, side-by-side, no space ».

## Analyse

Le serveur compare la ligne lue à une chaîne littérale, `if user_input == "\x65\x65\x65":`.
Le piège classique est d'envoyer les chiffres `101101101` (neuf octets) au lieu de la valeur
ASCII 101 répétée trois fois. Or `101 = 0x65 = 'e'` : la réponse attendue est la chaîne `eee`.
En Python, `b'\x65'` et `b'e'` désignent exactement le même octet ; l'échappement hexadécimal
n'est qu'une notation.

## Solution

1. Lire le source et repérer la comparaison : `grep -n 'user_input ==' app.py` →
   `if user_input == "\x65\x65\x65":`
2. Vérifier la conversion : `python3 -c 'print(chr(101))'` → `e`.
3. Envoyer les trois octets, sans espace :
   `echo 'eee' | nc <HOST> <PORT>` (ou `printf 'eee' | nc ...`).

`input()` retire le `\n` final, donc `echo` passe ; c'est un espace ajouté qui ferait échouer la
comparaison (il n'est pas « strippé »).

## Flag

```
picoCTF{pr1n74813_ch4r5_...}
```

Le préfixe est celui publié par picoCTF Solutions, qui masque volontairement la fin. Deux writeups
donnent des suffixes différents (`...1ade0c44` chez Cdenton, `...334c472c` chez Shukularuni) : le
suffixe exact n'est donc pas recopié ici, flag complet non conservé.

## Sources

- [picoCTF Solutions — bytemancy 0 (picoCTF 2026)](https://picoctfsolutions.com/picoctf-2026-bytemancy-0)
- [Cdenton — picoCTF 2026 writeup](https://cdenton1.github.io/2026/03/19/picoCTF-26.html)
- [Shukularuni — bytemancy 0](https://shukularuni.neocities.org/guide/ctf/picoctf/general/bytemancy_0)
