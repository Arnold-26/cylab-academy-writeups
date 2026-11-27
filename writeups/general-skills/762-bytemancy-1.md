# 762 — bytemancy 1

**Événement** : picoCTF 2026 · **Catégorie** : Général Skills

## Énoncé

> Can you conjure the right bytes? Download `app.py` and recover the exact input the server expects.

Même service TCP que bytemancy 0, mais la quantité demandée change.

## Analyse

### Le code fourni

```bash
grep -n 'user_input' app.py
# if user_input == "\x65" * 1751:
```

La comparaison est explicite : le serveur attend `\x65` répété 1751 fois, soit le caractère `e`
recopié 1751 fois. Il n'y a ni hachage, ni transformation, ni clé.

### La bannière

Le service annonce « Send me ASCII DECIMAL 101 1751 times, side-by-side, no space ». Deux confusions
sont à éviter :

- **101 est le code du caractère**, pas le nombre de répétitions : `101` en décimal vaut `0x65`, donc
  `e`. Envoyer la chaîne `101101101…` ne correspond à rien.
- **1751 est le nombre de répétitions**, pas une petite quantité à saisir à la main.

### Pourquoi c'est un challenge d'automatisation

Le passage de 3 à 1751 répétitions rend la saisie manuelle impossible. Le challenge ne porte pas sur
le comptage mais sur la génération du payload : il faut produire la chaîne exacte et l'envoyer sur la
même ligne.

## Solution

### 1. Confirmer la constante

```bash
grep -n 'user_input ==' app.py        # if user_input == "\x65" * 1751:
python3 -c 'print(len("e" * 1751))'   # 1751
```

### 2. Générer et envoyer

Le shell ne multiplie pas les chaînes : c'est Python qui calcule, puis le tube envoie le résultat.

```bash
python3 -c "print('e' * 1751)" | nc <HOST> <PORT>
```

### 3. Variante socket

```python
import socket
s = socket.create_connection(("<HOST>", PORT), timeout=5)
s.recv(512)                                   # consommer la bannière
s.sendall(b"e" * 1751 + b"\n")
print(s.recv(512).decode(errors="replace"))
```

Le `recv(512)` initial n'est pas décoratif : sans lui, on peut envoyer le payload avant que le
serveur n'ait fini d'écrire sa bannière, et la lecture suivante récupère la bannière au lieu de la
réponse.

### 4. Vérifier avant d'envoyer

```bash
python3 -c "import sys; p=b'e'*1751; assert len(p)==1751; sys.stdout.buffer.write(p+b'\n')" \
  | wc -c        # 1752
```

Un contrôle de longueur évite l'erreur classique : 1750 ou 1752 caractères, et le serveur refuse sans
explication utile.

### Pourquoi ça marche

La comparaison porte sur une chaîne de longueur fixe, connue à l'avance. Comme le service ne demande
aucune transformation, le payload est déterminé par le seul code fourni : la difficulté est
purement mécanique. Générer 1751 octets et les envoyer d'un bloc est exactement ce que fait le
client légitime.

## Pièges

- **Envoyer `101` au lieu de `e`.** Le nombre est le code décimal du caractère attendu, pas la
  donnée à transmettre.
- **Compter les répétitions à la main.** 1751 est trop grand pour une saisie fiable ; la constante
  doit venir du code, pas d'une estimation.
- **Oublier le saut de ligne.** Si le serveur lit une ligne complète, un payload sans `\n` reste en
  attente dans le tampon et la session se bloque.
- **Envoyer le payload avant de lire la bannière.** La réponse lue est alors la bannière, ce qui
  donne l'impression d'un échec.
- **Utiliser `echo` avec des guillemets simples dans un shell qui interprète mal les longues
  chaînes.** Passer par Python évite toute ambiguïté de quoting.
- **Tronquer la sortie.** La réponse du serveur arrive après la bannière : lire assez d'octets ou
  boucler jusqu'à la fermeture.
