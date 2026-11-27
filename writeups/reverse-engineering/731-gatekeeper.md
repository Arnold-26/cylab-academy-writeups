# 731 — Gatekeeper

**Événement** : picoCTF 2026 · **Catégorie** : Reverse Engineering

## Énoncé

« What's behind the numeric gate? You only get access if you enter the right kind of number. »

Le binaire `gatekeeper` est fourni. Il faut inverser ses contrôles numériques et fournir la valeur
qui les satisfait tous.

## Analyse

### Le comportement observable
```bash
chmod +x gatekeeper
./gatekeeper
```

Le programme demande un nombre. Une saisie quelconque est refusée avec un message générique : aucune
indication sur le contrôle qui a échoué, ni sur le format attendu. C'est le premier obstacle — le
binaire ne dit pas ce qu'il veut, il dit seulement non.

### Deux contrôles indépendants
L'analyse du binaire révèle **deux vérifications successives** :

1. une contrainte de **longueur** sur la chaîne saisie : trois caractères exactement ;
2. un contrôle de **valeur** sur l'entier obtenu après conversion : il doit être **supérieur à 999**.

Prises séparément, chacune est triviale. Ensemble, elles sont contradictoires — à première vue. Un
entier décimal de trois caractères ne peut pas dépasser 999 : `999` est le maximum, et la condition
est strictement supérieure. Autrement dit, **aucune entrée décimale ne peut satisfaire les deux
contrôles**. C'est exactement ce que l'énoncé appelle « the right *kind* of number » : la solution
n'est pas une valeur, c'est un **format**.

### Le format qui débloque
Le binaire convertit la chaîne avec `strtol`. Cette fonction accepte une **base**, et le binaire
l'appelle en base 16 : la chaîne est donc lue comme de l'hexadécimal.

- Longueur : `3e8` fait trois caractères. Premier contrôle satisfait.
- Valeur : `0x3e8` vaut 1000, qui est bien supérieur à 999. Second contrôle satisfait.

Le raisonnement sur la base est d'ailleurs contraint : si le binaire utilisait `strtol(s, NULL, 0)`
(détection automatique), il faudrait le préfixe `0x`, soit `0x3e8` — cinq caractères, rejeté par le
contrôle de longueur. La seule combinaison cohérente est donc une base 16 explicite. C'est ce genre
de recoupement qui évite de tâtonner.

### Le flag n'est pas imprimé directement
Une fois le portail franchi, la fonction `reveal_flag` ne fait pas un simple `puts`. Elle affiche le
flag **à l'envers**, en insérant la chaîne `picoCTF_` tous les 4 caractères. Deux transformations
composées, donc deux opérations à défaire, dans l'ordre inverse de leur application :

1. retirer toutes les occurrences de `picoCTF_` ;
2. inverser la chaîne restante.

L'ordre compte : inverser d'abord produirait `_FTFocip` partout et rendrait le retrait impossible.

## Solution

### Franchir le portail
```bash
chmod +x gatekeeper
echo '3e8' | ./gatekeeper
```

Si le binaire attend une interaction sur un terminal et non sur un pipe, la variante interactive :

```bash
./gatekeeper
# 3e8
```

### Défaire l'obfuscation
```bash
echo '<sortie_brute_du_binaire>' | sed -e 's/picoCTF_//g' | rev
```

Équivalent Python, plus lisible et plus facile à enchaîner :

```python
o = '<sortie_brute_du_binaire>'
print(o.replace('picoCTF_', '')[::-1])
```

Si la sortie contient des retours à la ligne parasites (le binaire peut insérer des sauts de ligne
tous les 4 caractères plutôt que la chaîne `picoCTF_` d'un build à l'autre), il faut aussi les supprimer
avant d'inverser :

```python
import re
clean = re.sub(r'picoCTF_|\s', '', o)
print(clean[::-1])
```

### Pourquoi ça marche
`strtol` est une fonction de conversion **paramétrée par une base**, et elle ne valide pas la
« naturalité » de la chaîne : `3e8` n'est pas un nombre décimal, c'est un nombre hexadécimal dont
l'écriture est légale. Le contrôle de longueur, lui, compte des **caractères** — pas des chiffres
décimaux. Les deux contrôles portent donc sur des espaces différents (longueur de la chaîne vs valeur
numérique) et il suffit d'un format d'écriture plus dense que le décimal pour les satisfaire
simultanément. C'est un cas d'école : valider la longueur d'une entrée avant sa conversion est une
mauvaise pratique, car la longueur de la représentation ne borne pas la valeur.

## Pièges

- **Penser décimal** : la première impasse consiste à chercher un nombre à trois chiffres supérieur à
  999. Il n'en existe pas — c'est le signal qu'il faut changer de base, pas de valeur.
- **`0x3e8`** : avec le préfixe, on dépasse la longueur de 3. Le format doit être nu.
- **`strtol` en base 0** : si le binaire utilisait la détection automatique, `3e8` serait lu comme `3`
  (arrêt sur le `e`) et le contrôle de valeur échouerait. La base 16 est donc explicite côté binaire.
- **Ordre du dé-obfuscation** : retirer les insertions **avant** d'inverser. L'inverse ne donne rien.
- **Sauts de ligne** : si le résultat semble presque lisible mais avec des caractères en trop,
  vérifier la présence de `\n` insérés tous les 4 caractères et les supprimer.
- **Flag incomplet** : la valeur complète n'a pas été conservée de notre côté ; seule la méthode de
  récupération est reproductible.

## Flag

Flag validé sur la plateforme (valeur non conservée).
