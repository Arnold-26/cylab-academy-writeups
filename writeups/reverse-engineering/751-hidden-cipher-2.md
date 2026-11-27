# 751 — Hidden Cipher 2

**Événement** : picoCTF 2026 · **Catégorie** : Reverse Engineering

## Énoncé

> The flag is right in front of you, kind of. You just need to solve a basic math problem to see it.
> To get the real flag, you'll have to understand how that math answer is used.

L'archive `hiddencipher2.zip` contient un binaire, et le service distant commence par poser un calcul
arithmétique simple. Le flag n'est jamais renvoyé en clair : le service livre un tableau d'entiers, et
l'énoncé prévient que la réponse au calcul sert à quelque chose.

## Analyse

### Premier contact avec le service

Une session interactive suffit à voir le protocole :

```bash
unzip hiddencipher2.zip
file hiddencipher2
nc <HOST> <PORT>
# What is 3 - 2?
```

On répond, et le service renvoie une liste de nombres. Les valeurs sont très supérieures à la plage
ASCII imprimable (32–126) : ce n'est pas un flag encodé en base classique, c'est un flag dont chaque
caractère a subi une transformation arithmétique.

### Le rôle de la réponse

On charge le binaire dans Ghidra (import, analyse automatique), puis on cherche la fonction appelée
juste après la lecture de la réponse. `main()` appelle `encode_flag()` à ce moment-là, et cette
fonction applique une seule opération à chaque octet du flag :

```c
for (i = 0; i < flag_len; i++)
    encoded[i] = (int)flag[i] * answer;
```

Chaque code ASCII est donc multiplié par la réponse au calcul. Le « chiffrement » n'a ni clé, ni état,
ni ronde : c'est une mise à l'échelle linéaire. La protection repose entièrement sur l'obscurité de
l'algorithme, et la décompilation la révèle en quelques secondes.

### La transformation inverse

La multiplication est inversible sur les entiers positifs tant que le multiplicateur est non nul : la
récupération se fait par division entière. Avec un tableau `[336, 315, 297]` et une réponse `3`, on
retrouve `336 / 3 = 112 = 'p'`, `315 / 3 = 105 = 'i'`, `297 / 3 = 99 = 'c'`.

## Solution

### 1. Récupérer la réponse et le tableau

Une session manuelle suffit pour valider la chaîne, mais il est plus sûr d'automatiser pour ne pas
perdre la valeur de la réponse :

```python
from pwn import *
import re

r = remote("<HOST>", PORT)
ligne = r.recvuntil(b"?", timeout=5).decode(errors="replace")
print(ligne)
a, op, b = re.search(r"What is (\d+)\s*([-+*/])\s*(\d+)", ligne).groups()
answer = {"+": int(a) + int(b), "-": int(a) - int(b),
          "*": int(a) * int(b), "/": int(a) // int(b)}[op]
print("reponse =", answer)
r.sendline(str(answer).encode())
data = r.recvall(timeout=5).decode(errors="replace")
print(data)
```

La formulation exacte de la question (« What is 3 - 2? ») est à revérifier sur la session courante :
on garde le `recvuntil(b"?")` et on imprime toujours la bannière brute avant de parser.

### 2. Décoder le tableau

```python
answer = 3
encoded = [336, 315, 297]                      # le tableau renvoyé par le service
assert all(n % answer == 0 for n in encoded)    # contrôle d'intégrité
print("".join(chr(n // answer) for n in encoded))
```

Le `assert` est le meilleur garde-fou : un seul reste non nul signifie que la réponse utilisée n'est
pas celle du calcul, ou que le tableau a été mal recopié.

### 3. Vérifier

Le clair doit commencer par le préfixe attendu et se terminer par `}`. Un texte illisible signale une
division par la mauvaise valeur ; un texte partiellement lisible signale une valeur manquante dans le
tableau.

### Pourquoi ça marche

Multiplier chaque code ASCII par un entier constant est une transformation bijective et sans perte :
le résultat contient exactement l'information d'origine, simplement sur une plage de valeurs plus
haute. Toute la difficulté tenait dans le fait de ne pas savoir qu'un simple `imul` était appliqué.
Dès que la fonction est lue, l'encodage n'offre plus aucune résistance.

## Pièges

- **Prendre les grands entiers pour du RSA ou du chiffrement à clé publique.** Les valeurs valent
  `ascii × réponse` ; chercher un module ou un exposant fait perdre du temps.
- **Oublier la réponse au calcul.** C'est la clé de l'encodage : la noter (ou l'automatiser) avant de
  répondre, sinon il faut relancer une session.
- **Recopier le tableau à la main.** Une valeur perdue au copier-coller donne un caractère manquant
  et un flag qui ne se valide pas.
- **Réponse égale à 1.** Les nombres sont alors directement les codes ASCII ; ce n'est pas un cas
  particulier à traiter, la même division fonctionne.
- **`encode_flag()` inlinée.** Le compilateur peut avoir replié la fonction dans `main()` : chercher
  l'instruction `imul` appliquée au tableau plutôt que le nom du symbole.

## Flag

Flag validé sur la plateforme (valeur non conservée).
