# 390 — ASCII Numbers

**Événement** : picoGym / Challenge Library Exclusive · **Catégorie** : General Skills

## Énoncé

« Convertissez la chaîne de nombres ASCII suivante en une chaîne lisible : »

```
0x70 0x69 0x63 0x6f 0x43 0x54 0x46 0x7b 0x34 0x35 0x63 0x31 0x31 0x5f 0x6e 0x30 0x5f ...
```

La chaîne complète compte 56 octets hexadécimaux séparés par des espaces. Indices : CyberChef est l'outil idéal pour tout encodage, en particulier ASCII ; essayer la recette « From Hex ».

## Analyse

Aucune cryptographie : chaque token est un octet écrit en hexadécimal, précédé de `0x`. La seule subtilité est de ne pas se contenter de remplacer les `0x` — il faut **réellement convertir** deux chiffres hexadécimaux en un caractère (par exemple `0x70` devient `p`, et non `70`).

La chaîne commence par les octets qui forment l'en-tête de flag de l'événement et finit par `0x7d`, l'accolade fermante : la structure est reconnaissable dès les premiers tokens, ce qui valide l'hypothèse avant même la fin du décodage.

Détail de lecture : toutes les valeurs sont comprises entre 0x20 et 0x7e, donc dans la plage ASCII imprimable. Une valeur hors de cette plage aurait signalé un encodage différent, par exemple de l'UTF-8 multi-octets.

## Solution

### CyberChef

Coller la chaîne dans *Input*, ajouter la recette **From Hex** avec `Auto` comme délimiteur : la sortie est le flag. Le mode `Auto` gère les espaces et les préfixes `0x` sans préparation.

### Python

```python
enc = "0x70 0x69 0x63 0x6f 0x43 0x54 0x46 0x7b ... 0x7d".split()
print(''.join(map(chr, map(lambda x: int(x, 16), enc))))
```

`int(x, 16)` accepte le préfixe `0x`, `chr` convertit le code en caractère. C'est reproductible et sans dépendance réseau.

### Shell

```bash
echo "70 69 63 6f 43 54 46 7b ... 7d" | xxd -r -p
```

`xxd -r -p` attend des octets hexadécimaux sans préfixe : il faut retirer les `0x` au préalable, par exemple avec `sed` :

```bash
sed 's/0x//g' <<< "0x70 0x69 0x63 0x6f ..." | tr -d ' \n' | xxd -r -p
```

### Vérification

La chaîne décodée ne doit contenir que des caractères imprimables et se terminer par l'accolade. Un caractère de contrôle signale une erreur de conversion, pas un flag valide.

### Pourquoi ça marche

Chaque token est un octet, et un octet ASCII imprimable correspond exactement à un caractère. Il n'y a donc aucune transformation à inverser : il suffit de lire la base 16 et de concaténer les caractères dans l'ordre. Les trois méthodes font la même chose, seule la syntaxe change.

## Pièges

- **Remplacer seulement les `0x`** : on obtient `7069636f...`, pas du texte ; il faut convertir les paires hexadécimales.
- **`tr -d '0x'`** : le jeu de caractères supprimés est `0` et `x`, donc tous les zéros disparaissent et certains octets sont corrompus ; `sed 's/0x//g'` est correct.
- **`xxd -r -p` avec les préfixes** : l'outil s'arrête sur le premier `x` et rend une sortie tronquée.
- **Délimiteur `Auto` oublié dans CyberChef** : avec un autre séparateur, la recette ne trouve pas les octets.
- **Copier la chaîne avec des retours à la ligne** : ils sont acceptés par la plupart des décodeurs, mais un `tr -d ' \n'` explicite évite les surprises.
- **Confondre ASCII et UTF-8** : ici tout tient sur un octet par caractère ; sur un texte accentué, `chr` produirait autre chose que `xxd`.
- **Oublier le dernier `0x7d`** : la chaîne se termine par l'accolade ; une copie partielle donne un flag refusé par la plateforme.

## Flag

Flag validé sur la plateforme (valeur non conservée).
