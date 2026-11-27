# 742 — bytemancy 0

**Événement** : picoCTF 2026 · **Catégorie** : Général Skills

## Énoncé

> Can you conjure the right bytes? Download `app.py` and recover the exact input the server expects.

Le code source `app.py` est fourni avec le challenge. Un service TCP attend une saisie précise et sa bannière annonce : « Send me ASCII DECIMAL 101, 101, 101, side-by-side, no space ».

## Analyse

Le serveur lit une ligne et la compare à une chaîne littérale :

```python
if user_input == "\x65\x65\x65":
```

Trois octets, tous égaux à `0x65`. La bannière les décrit en décimal : `101, 101, 101`, côte à côte, sans espace.

La conversion est immédiate : `101 = 0x65`, et `0x65` est le code ASCII de la lettre `e`. La réponse attendue est donc la chaîne `eee`.

Le piège est une confusion de niveaux de représentation. `\x65` en Python n'est pas une suite de caractères visible mais une **notation d'échappement** qui produit un seul octet de valeur `0x65` ; `b'\x65'` et `b'e'` désignent exactement le même octet. Envoyer `101101101`, c'est-à-dire la concaténation des trois nombres décimaux écrits à la suite, envoie neuf octets et non trois : la comparaison échoue. Envoyer `101 101 101` ajoute des espaces, qui ne sont pas retirés par la lecture de la ligne.

Le champ est lu avec `input()`, qui supprime le saut de ligne final mais **pas** les espaces. C'est ce détail qui rend `echo 'eee' | nc` fonctionnel alors qu'un `printf 'eee '` échouerait.

## Solution

### 1. Repérer la comparaison dans le source

```bash
grep -n 'user_input' app.py
grep -n 'user_input ==' app.py
# if user_input == "\x65\x65\x65":
```

### 2. Vérifier la conversion

```bash
python3 -c 'print(chr(101))'        # e
python3 -c 'print(hex(ord("e")))'   # 0x65
python3 -c 'print("\x65\x65\x65")'  # eee
```

Les trois commandes confirment la même chose sous trois angles : le décimal, l'hexadécimal et l'échappement décrivent un unique octet.

### 3. Envoyer les trois octets

```bash
echo 'eee' | nc <HOST> <PORT>
```

Variante qui garantit l'absence de `\n` parasite et n'ajoute rien :

```bash
printf 'eee' | nc -q 1 <HOST> <PORT>
```

Variante socket, utile pour voir la bannière avant l'envoi :

```python
import socket
s = socket.create_connection(("<HOST>", <PORT>))
print(s.recv(512).decode())        # bannière
s.sendall(b"eee\n")
print(s.recv(512).decode())
```

### 4. Lire la réponse

Le service renvoie une confirmation contenant le flag. Si la réponse est du type « wrong » ou « try again », c'est que la charge utile contient un octet de trop — un espace, un `\r`, ou un saut de ligne non absorbé.

### Pourquoi ça marche

La vérification porte sur la valeur des octets reçus, pas sur leur écriture. `\x65` est une simple commodité de notation côté source : à l'exécution, la constante est un objet `str` de trois caractères dont chacun vaut `e`. Tout ce qui produit ces trois octets est accepté, quelle que soit la façon dont on les a tapés.

## Pièges

- **Envoyer les chiffres au lieu du caractère.** `101101101` est la lecture naïve de « 101, 101, 101 » ; c'est neuf octets, pas trois.
- **Les séparateurs.** « side-by-side, no space » est une consigne littérale : une virgule ou une espace fait échouer la comparaison, car `input()` ne fait que retirer le `\n`.
- **Le `\r` sous Windows.** Un `printf` depuis un terminal mal configuré peut produire `eee\r\n` ; le `\r` reste et casse l'égalité. Vérifier avec `printf 'eee' | xxd`.
- **Fermer la connexion trop tôt.** `nc` sans `-q` peut couper avant la réponse ; `-q 1` laisse une seconde au serveur pour répondre.
