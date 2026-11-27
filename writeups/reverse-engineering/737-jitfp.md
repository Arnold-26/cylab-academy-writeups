# 737 — JITFP

**Événement** : picoCTF 2026 · **Catégorie** : Reverse Engineering

> Synthèse rédigée à partir des sources publiques listées en fin de fiche : ce challenge a été
> résolu côté CyLab Academy, mais le writeup d'origine n'a pas été conservé.

## Énoncé
« If we can crack the password checker on this remote host, we will be able to infiltrate deeper
into this criminal organization. The catch is it only functions properly on the host on which we
found it. » Il faut donc analyser le binaire **sur la machine distante**, sous debugger.

## Analyse
L'indice « only works on this host » et le nom (`JIT` + `FP`, function pointers) disent l'essentiel :
le mot de passe n'est pas stocké en clair dans le binaire, il est **recousu à l'exécution**.

Structure décrite par la page de solution :
- binaire 64 bits **PIE**, un seul processus ;
- validation d'un mot de passe de **33 caractères** ;
- **65 petites fonctions de comparaison** dans `.text`, une par caractère possible (`a-z`, `A-Z`,
  `0-9`, `_`, `{`, `}`), chacune comparant l'octet d'entrée à une constante codée en dur ;
- une **table de 33 pointeurs de fonction** décide quel comparateur vérifie quelle position, et cette
  table est établie dynamiquement — d'où l'impossibilité de résoudre hors de l'hôte.

Méthode : casser sur l'appel indirect (`call rdx` / `call *reg`) qui dispatche le comparateur, lire
la cible dans le registre, soustraire la base PIE pour obtenir l'offset de la fonction, puis lire
l'immédiat du `cmpb` à `offset + 12` (l'octet qui suit le motif `80 7d fc`) : c'est le caractère
attendu pour la position en cours. Il reste à inverser la permutation pour remettre les caractères
dans l'ordre de saisie, puis à envoyer la chaîne au binaire, qui affiche le flag.

## Solution
```bash
ssh <user>@<HOST> -p <PORT>
# localiser le binaire, l'ouvrir dans gdb
# break sur l'appel indirect ; à chaque hit :
#   - lire le pointeur de fonction cible
#   - offset = cible - base PIE (base lue dans /proc/<pid>/maps)
#   - caractère = octet à offset+12 (immédiat du cmpb)
# reconstituer les 33 caractères dans l'ordre des positions, puis :
echo '<MOT_DE_PASSE_33_CARACTERES>' | ./jitfp
```
Variante : scanner `.text` pour cartographier tous les comparateurs, puis suivre la table de
pointeurs à l'exécution.

## Flag
```
flag non conservé
```
Les writeups publics ne publient pas la valeur du flag (la page de solution l'affiche comme
`picoCTF{...}`) ; seule la méthode de récupération du mot de passe est documentée.

## Sources
- https://picoctfsolutions.com/picoctf-2026-jitfp — page de solution picoCTF 2026 (65 comparateurs, table JIT, lecture du `cmpb` à +12)
