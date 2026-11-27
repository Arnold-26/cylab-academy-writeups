# 35 — Based

**Événement** : picoCTF 2019 · **Catégorie** : Général Skills · **Auteur** : Alex Fulton/Daniel Tunitits

## Énoncé

Un service réseau demande de convertir des données entre plusieurs bases (binaire, octal,
hexadécimal) pour reconstituer des mots. La validation se fait en trois questions, avec un temps
limité (environ 45 secondes), d'où la nécessité d'automatiser.

## Analyse

On se connecte une première fois sans script, uniquement pour voir le format :

```bash
nc <HOST> 29221
```

Le service énonce un mot cible (« Convert this to ASCII: ») puis une suite de valeurs séparées par
des espaces. Chacune est le code ASCII d'un caractère, exprimé dans une base donnée. Trois familles
apparaissent :

- une suite de `0` et de `1` de longueur 8 par caractère : base 2 ;
- des valeurs dont le chiffre maximal est `7` (par exemple `146 141 154 143 157 156`) : base 8 ;
- une chaîne hexadécimale compacte (par exemple `737472656574`) : base 16, sans séparateur entre les
  octets.

La difficulté n'est pas la conversion mais la vitesse : trois questions à traiter en une
quarantaine de secondes, ce qui exclut le décodage manuel. Le service affiche par ailleurs le mot
attendu avant la question — comportement de debug — ce qui permet aussi de répondre sans décoder,
mais on préfère automatiser la conversion, plus fiable si le mot change.

## Solution

1. Décoder chaque famille à la main, pour vérifier la compréhension :

```python
''.join(chr(int(x, 2)) for x in '01100011 01101000 01100001 01101001 01110010'.split())
# chair

''.join(chr(int(x, 8)) for x in '146 141 154 143 157 156'.split())
# falcon

bytes.fromhex('737472656574').decode()
# street
```

2. Automatiser la boucle avec pwntools : lire la ligne de question, décoder, répondre, répéter.

```python
from pwn import *

io = remote("<HOST>", 29221)

def decode(valeurs):
    champs = valeurs.split()
    if all(c in '01' for c in valeurs.replace(' ', '')) and len(champs[0]) == 8:
        return ''.join(chr(int(v, 2)) for v in champs)          # base 2
    if len(champs) > 1:
        return ''.join(chr(int(v, 8)) for v in champs)          # base 8
    return bytes.fromhex(valeurs.strip()).decode()              # base 16

for _ in range(3):
    ligne = io.recvline().decode().strip()   # mot cible + question
    data = io.recvline().decode().strip()    # valeurs à convertir
    io.sendlineafter(b'Input:\n', decode(data).encode())

print(io.recvall().decode())
```

Les intitulés exacts des invites dépendent de l'instance : on ajuste les `recvline`/`sendlineafter`
après la première session d'observation, le principe de décodage ne change pas.

3. Lire la dernière ligne renvoyée par le service : elle contient le flag.

4. Alternative sans pwntools, si l'on veut rester en bibliothèque standard :

```python
import socket

s = socket.create_connection(("<HOST>", 29221))
# même boucle : lire, décoder, envoyer avec s.sendall((reponse + "\n").encode())
```

## Pièges

- **Ambiguïté binaire/octal.** Une valeur comme `111` peut être lue en base 2 ou en base 10. On
  tranche sur la longueur : la base 2 est donnée par groupes de 8 bits, un par caractère.
- **Hexadécimal compact.** `737472656574` n'a pas d'espaces : un `split()` sur les blancs renvoie
  une seule chaîne. Il faut découper en tranches de deux caractères, ce que fait `bytes.fromhex`.
- **Délai de 45 secondes.** Un aller-retour manuel par question ne passe pas. Le script doit boucler
  sans intervention, et sans affichage bloquant.
- **Lecture des invites.** Un `recvuntil` sur une chaîne trop précise bloque indéfiniment. On reste
  sur des lectures de lignes, plus tolérantes.
- **Réponse vide.** Une erreur de décodage renvoie une chaîne vide et le service la rejette
  immédiatement : journaliser la valeur reçue facilite le diagnostic.

**Pourquoi ça marche.** Le service ne teste que le résultat : il choisit une base, encode un mot et
compare la réponse. Le décodage est une conversion arithmétique déterministe, sans clé. La seule
contrainte réelle est le temps, et un script de vingt lignes la fait disparaître.
