# 737 — JITFP

**Événement** : picoCTF 2026 · **Catégorie** : Reverse Engineering

## Énoncé

« If we can crack the password checker on this remote host, we will be able to infiltrate deeper
into this criminal organization. The catch is it only functions properly on the host on which we
found it. »

Le binaire n'est pas fourni en local : il faut l'analyser **sur la machine distante**, sous debugger.

## Analyse

L'énoncé et le nom portent toute l'information. « only works on this host » signifie que le
comportement dépend de l'environnement d'exécution — un binaire qui se comporte différemment ailleurs
ne stocke pas sa logique en dur, il la **construit à l'exécution**. Et **JITFP** se lit *JIT* +
*FP* : logique recousue au démarrage, à base de **pointeurs de fonction**.

Conséquence : l'analyse statique sur une copie du fichier ne suffit pas, il faut observer l'état
mémoire du processus pendant qu'il tourne.

Une fois sur l'hôte, la structure apparaît :

- **64 bits, PIE** — adresses randomisées à chaque exécution, offsets relatifs à la base stables ;
- un seul processus, pas de fork : pas de suivi d'enfant à gérer ;
- validation d'un mot de passe de **33 caractères** ;
- **65 petites fonctions de comparaison** dans `.text`, une par caractère possible de l'alphabet
  (`a-z`, `A-Z`, `0-9`, `_`, `{`, `}`), chacune comparant l'octet d'entrée à une constante codée en
  dur ;
- une **table de 33 pointeurs de fonction** décide quel comparateur vérifie quelle position.

C'est ce dernier point qui rend le binaire intraduisible hors de son hôte : la table est **établie
dynamiquement**, vraisemblablement à partir d'éléments de l'environnement. Une copie exécutée ailleurs
reconstruirait une table différente.

## Solution

### Se placer sur l'hôte
```bash
ssh <user>@<HOST> -p <PORT>
ls -la
file ./jitfp
```

### Casser sur l'appel indirect
Le dispatcher est un appel indirect — `call rdx` ou `call *reg` dans la forme compilée. C'est le
point d'observation idéal : à chaque hit, on sait **quelle** fonction va être appelée pour la position
courante.

```gdb
set pagination off
set disassembly-flavor intel
disassemble /r main

break *main+0x0        # à ajuster : l'instruction call *reg du dispatcher
commands
  silent
  printf "target=%p\n", $rdx
  continue
end
run
```

### Décoder chaque comparateur
Pour chaque hit : lire le **pointeur de fonction cible** dans le registre, soustraire la **base PIE**
pour obtenir un offset stable (base lue dans `/proc/<pid>/maps`, ou `info proc mappings` sous gdb),
puis lire l'**immédiat du `cmpb`** à `offset + 12` — l'octet juste après le motif `80 7d fc`
(`cmp byte ptr [rbp-4], imm8`).

```gdb
set $off = $rdx - $base
x/1xb $rdx + 12
```

L'offset `+12` se justifie ainsi : `80 7d fc XX` occupe 4 octets, précédé de la séquence de prologue
standard du comparateur. Après vérification sur un ou deux comparateurs, l'immédiat tombe
systématiquement à `+12` et la lecture peut être scriptée.

### Reconstituer l'ordre
Chaque hit donne un caractère pour une **position**, mais la table de pointeurs applique une
**permutation** : l'ordre d'appel des comparateurs n'est pas l'ordre de saisie. Il faut inverser la
permutation pour remettre les 33 caractères dans l'ordre attendu.

```python
pw = ''.join(char_at_pos[i] for i in range(33))
print(pw)
```

Le retour du programme (valide / invalide) sert de vérification immédiate : s'il refuse, l'ordre est
faux et il faut appliquer la permutation inverse.

```bash
echo '<MOT_DE_PASSE_33_CARACTERES>' | ./jitfp
```

Variante : cartographier **tous** les comparateurs en scannant `.text` à la recherche du motif
`80 7d fc`, puis suivre la table à l'exécution pour établir la correspondance position → caractère.

### Pourquoi ça marche
Le binaire cache la **correspondance** entre positions et caractères, pas les caractères eux-mêmes.
Chaque comparateur contient son octet attendu en clair, dans une instruction `cmp` : aucune
obfuscation, aucun chiffrement. La protection repose sur le fait qu'on ne sait pas *où* regarder — la
table étant construite à l'exécution, elle est illisible statiquement. Dès qu'on observe l'appel
indirect, on obtient la réponse à « lequel ? » au moment où elle est posée. Face à un dispatch
dynamique, on ne reconstruit pas la table : on l'observe.

## Pièges

- **Analyser en local** : le binaire ne se comporte pas pareil ailleurs ; c'est l'énoncé qui le dit.
- **Oublier la base PIE** : les pointeurs lus sont absolus et randomisés à chaque run ; les offsets se
  calculent par soustraction de la base.
- **Mauvais offset du `cmp`** : si la lecture donne autre chose qu'un caractère imprimable,
  désassembler un comparateur et recalculer.
- **Ordre des positions** : la permutation est le vrai travail restant ; ne pas soumettre la
  concaténation dans l'ordre des hits sans vérifier.
- **Longueur** : 33 caractères, un octet de trop (retour à la ligne) fait échouer la validation.
