# 724 — bytemancy 2

**Événement** : picoCTF 2026 · **Catégorie** : General Skills

## Énoncé
« Can you conjure the right bytes? »

Le source `app.py` est fourni, ainsi qu'un service distant. Il faut lui envoyer l'entrée exacte
qu'il attend. Le titre de la série, *bytemancy*, est explicite : le challenge porte sur la
manipulation d'octets, pas sur une faille de logique.

## Analyse

### Le code
```bash
cat app.py
```

La partie utile du script tient en deux lignes :

```python
data = sys.stdin.buffer.readline().rstrip(b"\n")
if data == b'\xff\xff\xff':
    ...
```

Trois informations décisives :

- la lecture se fait avec `sys.stdin.buffer`, donc en **mode binaire brut**. Aucun décodage de texte
  n'intervient : le programme compare des octets.
- `readline()` lit jusqu'au premier `\n` : l'entrée doit donc être terminée par un saut de ligne,
  sinon le serveur reste bloqué en attente.
- `rstrip(b"\n")` retire **uniquement** le `\n` final. Le reste est comparé tel quel à
  `b'\xff\xff\xff'` : trois fois l'octet `0xFF`, sans espace, sans séparateur, sans octal écrit en
  clair.

La cible est donc une séquence de trois octets de valeur 255, suivie d'un saut de ligne.

### Pourquoi c'est piégeux
Contrairement aux opus précédents de la série, il ne s'agit pas d'écrire *l'écriture textuelle* de ces
octets (`ff`, `\xff`, `255`, `ÿ`) mais de les envoyer **littéralement**. C'est la distinction entre
la représentation d'une donnée et la donnée elle-même — et Python encourage la confusion, parce que
`print` fait passer par une couche d'encodage.

Deux erreurs classiques, et nous les avons rencontrées toutes les deux :

1. `python3 -c "print(b'\xff'*3)"` n'envoie pas trois octets `0xFF`. `print` appelle `str()` sur
   l'objet `bytes`, ce qui produit la **représentation** `b'\xff\xff\xff'` — quinze caractères ASCII
   (`b`, `'`, `\`, `x`, `f`, `f`, …). Le serveur reçoit du texte, pas des octets.
2. Sans le préfixe `b`, `print('\xff')` envoie le caractère `U+00FF`, que Python encode en **UTF-8**
   sur deux octets : `c3 bf`. On obtient six octets au lieu de trois, et la comparaison échoue.

Dans les deux cas, le programme répond « wrong » sans autre explication : la comparaison d'octets ne
donne pas d'indice sur ce qui a été reçu.

### La contrainte du saut de ligne
`readline()` ne rend la main qu'à la réception d'un `\n` (ou à la fermeture du flux). Sans `\n`, le
serveur attend indéfiniment et le client aussi : le symptôme est un timeout, pas une erreur. Il faut
donc envoyer exactement **quatre** octets : `ff ff ff 0a`.

## Solution

### Variante pwntools
La plus fiable, parce qu'elle ne passe jamais par la couche texte :

```bash
python3 - <<'PY'
from pwn import remote, context
context.log_level = 'error'

r = remote('<HOST>', <PORT>)
r.recvuntil(b'>')                    # laisser le service afficher son prompt
r.send(b'\xff\xff\xff\n')            # 3 octets 0xFF + saut de ligne
print(r.recvall(timeout=5).decode(errors='replace'))
PY
```

`send` (et non `sendline`) est volontaire : on maîtrise exactement les octets transmis, et on ajoute
le `\n` soi-même. `sendline` ajouterait le saut de ligne après coup, ce qui revient au même ici, mais
`send` rend le payload explicite.

### Variante shell
```bash
python3 -c "import sys; sys.stdout.buffer.write(b'\xff\xff\xff\n')" | nc <HOST> <PORT>
```

`sys.stdout.buffer` contourne l'encodage de `sys.stdout` : les octets sont écrits tels quels sur le
descripteur 1.

```bash
printf '\xff\xff\xff\n' | nc <HOST> <PORT>
```

`printf` interprète les échappements `\xNN` et écrit les octets bruts. Attention : avec `echo`, le
comportement dépend du shell (`echo -e` en bash, interprétation systématique en `sh`/`dash`), ce qui
rend le résultat non reproductible. Utiliser `printf`, toujours.

Le serveur répond alors avec le contenu de `flag.txt`.

### Pourquoi ça marche
Le programme compare des octets, pas une chaîne : il n'y a ni normalisation Unicode, ni décodage, ni
tolérance sur les espaces. Toute la difficulté est donc côté client — il faut réussir à faire sortir
trois `0xFF` tels quels d'une chaîne d'outils conçue pour du texte. C'est un rappel utile : en
informatique, « envoyer `\xff` » et « envoyer les quatre caractères `\`, `x`, `f`, `f` » sont deux
opérations différentes, et la plupart des langages de haut niveau choisissent implicitement la
seconde dès qu'on utilise `print`.

## Pièges
- **`print(bytes)`** : envoie la représentation, pas les octets. C'est le piège principal de ce
  challenge.
- **`print('\xff')`** : encode en UTF-8 (`c3 bf`), donc six octets au lieu de trois.
- **Oublier le `\n`** : le serveur reste dans `readline()` et le client attend une réponse qui
  n'arrive jamais. Un timeout n'est pas une mauvaise réponse.
- **CRLF** : `rstrip(b"\n")` ne retire pas le `\r`. Un envoi depuis un terminal Windows laisse un `\r`
  final, et la comparaison échoue pour un octet invisible : hexdumper ce qui part réellement.
- **Nombre d'octets** : trois, pas quatre. `b'\xff'*4` échoue aussi silencieusement.

## Flag

Flag validé sur la plateforme (valeur non conservée).
