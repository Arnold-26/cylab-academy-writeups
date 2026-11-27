# 762 — bytemancy 1

**Événement** : picoCTF 2026 · **Catégorie** : General Skills

> Synthèse rédigée à partir des sources publiques listées en fin de fiche : ce challenge a été
> résolu côté CyLab Academy, mais le writeup d'origine n'a pas été conservé.

## Énoncé

> Can you conjure the right bytes? Download `app.py` and recover the exact input the server expects.

Même service TCP que bytemancy 0, mais la quantité demandée change.

## Analyse

`app.py` contient la comparaison `if user_input == "\x65" * 1751:`. La bannière demande « Send me
ASCII DECIMAL 101 1751 times, side-by-side, no space ». Deux confusions à éviter : 101 est le code
du caractère `e` (pas le nombre de répétitions) et 1751 est le nombre de répétitions (pas un petit
compte à saisir à la main). Le passage de 3 à 1751 répétitions force l'automatisation : c'est un
challenge sur la génération de payload, pas sur le comptage.

## Solution

1. Lire le source et confirmer la constante :

```bash
grep -n 'user_input ==' app.py    # if user_input == "\x65" * 1751:
python3 -c 'print(len("e"*1751))' # 1751
```

2. Générer et envoyer la chaîne (le shell ne multiplie pas les chaînes, c'est Python qui calcule) :

```bash
python3 -c "print('e' * 1751)" | nc <HOST> <PORT>
```

3. Variante socket, où le `recv(512)` sert à consommer la bannière avant l'envoi :

```python
import socket
s = socket.create_connection(("<HOST>", PORT))
s.recv(512); s.sendall(b"e"*1751 + b"\n"); print(s.recv(512).decode())
```

## Flag

```
picoCTF{h0w_m4ny_e's???_7dbc095c}
```

Flag complet publié par le writeup Cdenton (transcription d'exécution) ; préfixe
`picoCTF{h0w_m4ny_e's???_` corroboré par picoCTF Solutions.

## Sources

- [picoCTF Solutions — bytemancy 1 (picoCTF 2026)](https://picoctfsolutions.com/picoctf-2026-bytemancy-1)
- [Cdenton — picoCTF 2026 writeup](https://cdenton1.github.io/2026/03/19/picoCTF-26.html)
