# 754 — Autorev 1

**Événement** : picoCTF 2026 · **Catégorie** : Reverse Engineering

> Synthèse rédigée à partir des sources publiques listées en fin de fiche : ce challenge a été
> résolu côté CyLab Academy, mais le writeup d'origine n'a pas été conservé.

## Énoncé

> You think you can reverse engineer? Let's test out your speed. Connect to the server - it sends
> you 20 binary files one at a time (1 second each) and you must extract the secret from each one.

## Analyse

Le serveur envoie 20 binaires encodés en hexadécimal, un par un, avec environ une seconde par
manche : impossible à traiter à la main, il faut un solveur. Chaque binaire affiche un prompt
« What's the secret? », lit la réponse avec `scanf`, et la compare à une valeur codée en dur. Ce
secret est un immédiat stocké par une instruction du type `mov DWORD PTR [rbp-0x8], 0x…` dans
`main()`. Le travail consiste donc à désassembler à la volée et à extraire cet immédiat, puis à
renvoyer sa valeur en décimal — vingt fois de suite.

## Solution

1. Récupérer un binaire pour l'analyser hors ligne :

```bash
nc <HOST> <PORT> | head -1 | xxd -r -p > /tmp/binary
objdump -d /tmp/binary | grep -A5 '<main>'
# repérer : mov DWORD PTR [rbp-0x8], 0x<SECRET>
```

2. Automatiser avec pwntools + capstone, sans écrire sur disque, en cherchant l'immédiat dans
   l'instruction `mov` relative à `rbp` :

```python
from pwn import *
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
import re
r = remote("<HOST>", PORT)
md = Cs(CS_ARCH_X86, CS_MODE_64)
for _ in range(20):
    r.recvuntil(b"bytes"); binary = bytes.fromhex(r.recvline().strip().decode())
    secret = 0
    for insn in md.disasm(binary, 0):
        m = re.search(r"mov dword ptr \[rbp - (?:8|4|0x8|0x4)\], (0x[0-9a-f]+|\d+)",
                      insn.mnemonic + " " + insn.op_str)
        if m: secret = int(m.group(1), 0); break
    r.recvuntil(b"secret"); r.sendline(str(secret).encode())
print(r.recvall(timeout=5).decode())
```

3. Après les 20 manches, le serveur renvoie le flag.

## Flag

```
picoCTF{4u7o_r3v_g0_brrr_...}
```

Préfixe publié par picoCTF Solutions (suffixe masqué à la source) : le flag complet n'est pas
recopié ici.

## Sources

- [picoCTF Solutions — Autorev 1 (picoCTF 2026)](https://picoctfsolutions.com/picoctf-2026-autorev-1)
- [snwau/picoCTF-2026-Writeup — Reverse Engineering/Autorev 1](https://github.com/snwau/picoCTF-2026-Writeup/blob/main/Reverse%20Engineering/Autorev%201/Autorev%201.md)
