# 724 — bytemancy 2

**Événement** : picoCTF 2026 · **Catégorie** : General Skills

> Synthèse rédigée à partir des sources publiques listées en fin de fiche : ce challenge a été
> résolu côté CyLab Academy, mais le writeup d'origine n'a pas été conservé.

## Énoncé
« Can you conjure the right bytes? » Le source `app.py` est fourni ; il faut envoyer au service
l'entrée exacte qu'il attend.

## Analyse
`app.py` lit l'entrée avec `sys.stdin.buffer.readline().rstrip(b"\n")` et la compare à
`b'\xff\xff\xff'` : trois fois l'octet `0xFF`, sans espace. Contrairement aux opus précédents de la
série, la lecture se fait en **mode binaire brut**, donc il faut envoyer les octets littéraux et non
leur écriture textuelle (`ff`, `\xff`, …).

Deux erreurs classiques, documentées par les writeups :
- `python3 -c "print(b'\xff'*3)"` envoie la **représentation** de l'objet bytes (`b'\xff\xff\xff'`,
  soit 15 caractères ASCII) ;
- sans le préfixe `b`, stdout en mode texte ré-encode `U+00FF` en UTF-8, soit les deux octets
  `c3 bf`.

Il faut donc `sys.stdout.buffer.write(...)` ou `printf`, **et** terminer par un `\n`, sinon le
serveur reste bloqué dans `readline()` en attendant la fin de ligne.

## Solution
```bash
cat app.py
# variante pwntools (pas de corruption d'encodage)
python3 - <<'PY'
from pwn import remote, context
context.log_level = 'error'
r = remote('<HOST>', <PORT>)
r.send(b'\xff\xff\xff\n')
print(r.recvall().decode(errors='replace'))
PY

# variante shell (bash, pas dash)
python3 -c "import sys; sys.stdout.buffer.write(b'\xff\xff\xff\n')" | nc <HOST> <PORT>
printf '\xff\xff\xff\n' | nc <HOST> <PORT>
```
Le serveur répond avec le contenu de `flag.txt`.

## Flag
```
picoCTF{3ff5_4_d4yz_9a6da265}
```

## Sources
- https://picoctfsolutions.com/picoctf-2026-bytemancy-2 — page de solution picoCTF 2026 (lecture binaire, pièges `print`/UTF-8)
- https://qiita.com/8omp/items/8e1aa38aeda96fa0ecb6 — writeup picoCTF 2026 General Skills (source `app.py`, flag complet)
