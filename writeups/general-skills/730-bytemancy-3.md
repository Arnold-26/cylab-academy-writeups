# 730 — bytemancy 3

**Événement** : picoCTF 2026 · **Catégorie** : General Skills

## Énoncé

« Can you conjure the right bytes? »

Deux fichiers : `app.py` et le binaire `spellbook`. Il faut reconstituer la charge utile exacte
attendue par le service et l'envoyer.

## Analyse

### Le protocole
`app.py` énonce la règle du jeu :

> I will name four procedures hidden inside spellbook. Each round, send me their *raw* 4-byte
> addresses in little-endian form.

Les quatre fonctions sont `ember_sigil`, `glyph_conflux`, `astral_spark` et `binding_word`. Le serveur
en tire **trois** au hasard, une par tour, et attend pour chacune son adresse sous forme de **4 octets
bruts en little-endian**. Trois contraintes, chacune avec son piège :

- « **raw** » : les octets eux-mêmes, pas leur écriture hexadécimale (`08049176`) ni décimale ;
- « **4-byte** » : exactement quatre octets, une adresse 32 bits ;
- « **little-endian** » : octet de poids faible d'abord, donc `76 91 04 08` et non `08 04 91 76`.

### Pourquoi les adresses sont connues d'avance
```bash
cat app.py
file spellbook
```

`file` répond : ELF **32 bits**, **non-PIE**, **non strippé**. Cette combinaison est déterminante :

- **non-PIE** : le binaire est chargé à une adresse de base fixe, donc les adresses des fonctions sont
  identiques à chaque exécution et identiques à celles de la table des symboles ;
- **non strippé** : la table des symboles est présente, les noms de fonctions y figurent avec leurs
  adresses — inutile de retrouver les offsets à la main.

Si le binaire avait été PIE, il aurait fallu une fuite d'adresse à l'exécution ; s'il avait été
strippé, il aurait fallu identifier les quatre fonctions par leur code dans Ghidra ou radare2. Ici,
`nm` suffit.

### La lecture côté serveur
Le serveur lit quatre octets exactement, pas une ligne : un `\n` en trop resterait dans le tampon et
décalerait toutes les réponses suivantes.

## Solution

### Récupérer les adresses
```bash
cat app.py
file spellbook
nm spellbook | grep -E "ember_sigil|glyph_conflux|astral_spark|binding_word"
```

Sortie pour le binaire distribué :

```
08049176 T ember_sigil
0804919a T glyph_conflux
080491c1 T astral_spark
080491e3 T binding_word
```

Le `T` signifie « symbole dans la section `.text` », donc une fonction. On recoupe avec
`objdump -d spellbook | grep '<ember_sigil>'` : la table des symboles peut mentir si le binaire a été
bricolé, pas le désassembleur.

### Construire l'exploit
```python
from pwn import *
context.log_level = 'error'
context.arch = 'i386'

ADDR = {
    b'ember_sigil':   0x08049176,
    b'glyph_conflux': 0x0804919a,
    b'astral_spark':  0x080491c1,
    b'binding_word':  0x080491e3,
}

r = remote('<HOST>', <PORT>)
for _ in range(3):
    line = r.recvline()
    for name, addr in ADDR.items():
        if name in line:
            r.send(p32(addr))       # 4 octets bruts, little-endian, sans \n
            break

print(r.recvall(timeout=5).decode(errors='replace'))
```

`p32()` encode l'entier sur 32 bits en little-endian, et `send()` transmet les octets sans rien
ajouter. `p32(0x08049176)` produit `\x76\x91\x04\x08` — quatre octets, dont deux non imprimables.
Toute la difficulté est là : le payload n'est pas une chaîne, c'est une structure binaire.

### Pourquoi ça marche
Une adresse virtuelle dans un exécutable non-PIE est une **constante de compilation**. Le chargeur
place le segment de code à une adresse fixe, connue du linker, et y écrit les adresses des fonctions
comme des valeurs littérales ; la table des symboles n'est qu'un index de ces constantes. Envoyées au
serveur, elles lui permettent de sauter directement dans la fonction nommée — il se contente d'appeler
le pointeur reçu. Le challenge est donc un exercice de passage de données binaires : comprendre qu'une
adresse n'est pas un texte mais quatre octets, et que leur ordre est normé par l'architecture.

## Pièges

- **`sendline` au lieu de `send`** : le `\n` supplémentaire décale la lecture. Le premier tour peut
  passer, les suivants échouent.
- **Mauvais endianness** : `p32(addr, endian='big')` ou `pack('>I', addr)` envoie les octets à
  l'envers, le serveur lit une adresse absurde.
- **Écriture hexadécimale** : envoyer la chaîne `08049176` (8 caractères ASCII) au lieu des 4 octets.
  Même piège que dans *bytemancy 2*, transposé aux adresses.
- **Nom mal extrait** : le serveur peut écrire les noms dans une phrase. Un `recvline()` suivi d'une
  recherche de sous-chaîne est plus robuste qu'un `recvuntil(nom)` sur un nom inconnu.
- **Ordre aléatoire** : le serveur tire trois des quatre fonctions. Coder une boucle qui réagit au nom
  annoncé, jamais une séquence figée.

## Flag

Flag validé sur la plateforme (valeur non conservée).
