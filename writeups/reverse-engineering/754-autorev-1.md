# 754 — Autorev 1

**Événement** : picoCTF 2026 · **Catégorie** : Reverse Engineering

## Énoncé

> You think you can reverse engineer? Let's test out your speed. Connect to the server - it sends
> you 20 binary files one at a time (1 second each) and you must extract the secret from each one.

Vingt manches, un binaire par manche, environ une seconde par manche : le challenge ne porte pas sur
un binaire difficile mais sur la vitesse d'analyse.

## Analyse

### Le protocole

À la connexion, le serveur annonce chaque manche puis envoie une ligne contenant le binaire encodé en
hexadécimal. Un `head -1` suivi d'un `xxd -r -p` reconstitue un ELF valide : le transport est de
l'hexadécimal brut, ni base64 ni archive.

Chaque binaire affiche un prompt « What's the secret? », lit un entier avec `scanf("%d", …)` et le
compare à une constante codée en dur. Aucune cryptographie, aucune valeur à deviner : le secret est
dans le corps de la fonction principale.

### Où se trouve le secret

Le compilateur matérialise la constante par un store immédiat sur la pile, juste avant la
comparaison :

```asm
mov     DWORD PTR [rbp-0x8], 0x1f2a     ; le secret
...
lea     rax, [rbp-0x8]
mov     rsi, rax
mov     rdi, <saisie>
call    strcmp
```

L'analyse consiste donc à désassembler à la volée et à extraire l'immédiat du `mov` dont la
destination est relative à `rbp`. Le reste — prompt, comparaison, affichage — est du bruit.

### Pourquoi il faut automatiser

Une seconde par manche et vingt manches : toute intervention humaine casse la cadence et la
connexion est perdue. Le solveur doit, pour chaque binaire, décoder l'hexadécimal, désassembler,
extraire l'immédiat, envoyer sa valeur en décimal et enchaîner immédiatement la manche suivante.

## Solution

### 1. Valider la chaîne à la main sur une manche

```bash
nc <HOST> <PORT> | head -1 | xxd -r -p > /tmp/binary
file /tmp/binary
objdump -d /tmp/binary | grep -A8 '<main>'
# repérer : mov DWORD PTR [rbp-0x8], 0x<SECRET>
```

Cette étape sert uniquement à confirmer la forme de l'instruction et l'offset de pile ; elle consomme
une manche.

### 2. Automatiser sans écrire sur disque

```python
from pwn import *
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
import re

r = remote("<HOST>", PORT)
md = Cs(CS_ARCH_X86, CS_MODE_64)

for i in range(20):
    r.recvuntil(b"bytes", timeout=5)
    binary = bytes.fromhex(r.recvline().strip().decode())
    secret = None
    for insn in md.disasm(binary, 0):
        m = re.search(r"mov dword ptr \[rbp - (?:8|4|0x8|0x4)\], (0x[0-9a-f]+|\d+)",
                      insn.mnemonic + " " + insn.op_str)
        if m:
            secret = int(m.group(1), 0)
            break
    if secret is None:
        log.failure(f"manche {i}: immédiat non trouvé")
        break
    r.recvuntil(b"secret")
    r.sendline(str(secret).encode())
    log.success(f"manche {i}: {secret}")

print(r.recvall(timeout=5).decode(errors="replace"))
```

Le `recvuntil(b"bytes")` consomme l'annonce de la manche, le `recvline` récupère la ligne
hexadécimale. Les deux réceptions portent un `timeout` pour éviter de rester bloqué si le protocole
dérive.

### 3. Lire le flag

Après la vingtième réponse, le serveur renvoie le flag sur la même connexion : le `recvall` final suffit.

### Pourquoi ça marche

Le secret n'est pas calculé à l'exécution : il est écrit en dur dans `main`. Capstone restitue
exactement l'opérande que le compilateur a généré, et le format d'envoi correspond au `%d` du
`scanf`. Tout le travail réel consiste à tenir vingt manches sans latence humaine.

## Pièges

- **Écrire chaque binaire sur disque.** `open()` puis `objdump` puis parsing dépassent la seconde
  accordée ; capstone en mémoire tient la cadence.
- **Envoyer en hexadécimal.** Le binaire lit avec `%d` : c'est la valeur décimale qu'il attend.
- **Oublier de consommer le prompt avant l'envoi.** Le `sendline` part trop tôt et décale toutes les
  manches suivantes.
- **Un seul motif de recherche.** Si le `mov` attendu n'apparaît pas, élargir aux stores sur
  `[rbp-0x4]` et aux `mov eax, 0x…` qui précèdent la comparaison.
- **Immediat négatif.** Capstone peut afficher `-0x…` : la conversion doit rester en base 0 pour ne
  pas envoyer `0`.

## Flag

Flag validé sur la plateforme (valeur non conservée).
