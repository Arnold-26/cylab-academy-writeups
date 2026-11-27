# 766 — Undo

**Événement** : picoCTF 2026 · **Catégorie** : Général Skills

## Énoncé

> Can you reverse a series of Linux text transformations to recover the original flag? Start by
> searching for the flag here.

Un service TCP affiche une chaîne transformée et un indice qui nomme la transformation appliquée.
Il faut saisir la commande Linux qui l'inverse, étape par étape, jusqu'à retrouver le flag.

## Analyse

On se connecte une première fois sans rien envoyer, uniquement pour lire la structure du dialogue :

```bash
nc <HOST> <PORT>
```

Chaque étape se présente sous la forme d'un texte déformé suivi d'une phrase du type « Base64
encoded the string », « Reversed the text », « Replaced underscores with dashes », « Replaced curly
braces with parentheses », « Applied ROT13 to letters ».

Aucune devinette n'est nécessaire : l'indice **nomme** la transformation. Le travail consiste donc
à connaître l'inverse exact de chacune, et à le fournir sous forme d'une commande qui lit la
chaîne sur l'entrée standard et écrit le résultat sur la sortie standard.

Les transformations en jeu sont toutes réversibles sans clé :

| Transformation | Indice | Inverse |
|---|---|---|
| Base64 | « Base64 encoded the string » | `base64 -d` |
| Texte inversé | « Reversed the text » | `rev` |
| Tirets ajoutés à la place des underscores | « Replaced underscores with dashes » | `tr '-' '_'` |
| Accolades remplacées par des parenthèses | « Replaced curly braces with parentheses » | `tr '()' '{}'` |
| ROT13 | « Applied ROT13 to letters » | `tr A-Za-z N-ZA-Mn-za-m` |

Deux propriétés rendent le challenge simple. D'une part ROT13 est une involution : la même commande
chiffre et déchiffre. D'autre part `tr` applique une correspondance caractère par caractère dans
l'ordre des deux ensembles fournis, donc `tr '()' '{}'` transforme bien `(` en `{`.

## Solution

1. Se connecter et relever l'indice de la première étape :

```bash
nc <HOST> <PORT>
```

2. Répondre par la commande inverse, seule sur sa ligne, sans `echo` ni redirection :

```
base64 -d
```

3. Enchaîner les étapes en adaptant la commande à l'indice affiché. Les cinq commandes utiles :

```bash
base64 -d
rev
tr '-' '_'
tr '()' '{}'
tr A-Za-z N-ZA-Mn-za-m
```

4. Quand toutes les transformations ont été annulées, la chaîne obtenue commence par le préfixe du
   flag : le serveur la reconnaît et rend le flag.

5. Pour préparer la session, on peut lister les inverses dans un fichier et les envoyer au fil de
   l'eau avec `nc` :

```bash
printf '%s\n' 'base64 -d' 'rev' "tr '-' '_'" "tr '()' '{}'" \
  'tr A-Za-z N-ZA-Mn-za-m' > /tmp/undo.txt
nc <HOST> <PORT> < /tmp/undo.txt
```

L'ordre des lignes dans ce fichier suit l'ordre d'apparition des indices ; s'il diffère sur
l'instance, on édite le fichier en conséquence.

6. Contrôle local d'une étape, pour vérifier une commande avant de l'envoyer :

```bash
printf 'synt{Grfg}' | tr A-Za-z N-ZA-Mn-za-m
# flag{Test}
```

## Pièges

- **`echo` dans la commande.** Le service attend la commande seule : un `echo <texte> | base64 -d`
  est refusé, la chaîne à traiter étant déjà fournie par le service.
- **Sens des arguments de `tr`.** `tr '-' '_'` est l'inverse de la transformation ; `tr '_' '-'`
  transforme dans le mauvais sens et casse l'étape.
- **Accolades et shell.** Les parenthèses et accolades sont à protéger par des quotes simples,
  sinon le shell les interprète avant l'envoi.
- **`base64 -d` et les sauts de ligne.** L'outil les ignore, ce qui est souhaitable ici ; en
  revanche une chaîne tronquée produit `invalid input` et il faut recommencer l'étape.
- **Ordre des étapes.** Chaque réponse est validée immédiatement : une erreur ne se rattrape pas
  plus loin, elle se corrige à l'étape en cours.

**Pourquoi ça marche.** Le service ne chiffre rien : il applique des transformations de texte
réversibles et en donne le nom. Toute la sécurité repose sur l'ignorance de l'inverse, alors que
l'inverse est une commande Unix standard d'une ligne. Le challenge teste la familiarité avec les
filtres de texte, pas la cryptanalyse.
