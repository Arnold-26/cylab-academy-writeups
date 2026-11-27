# 720 — Timeline 0

**Événement** : picoCTF 2026 · **Catégorie** : Forensics

## Énoncé

« Can you find the flag in this disk image? Wrap what you find in the picoCTF flag format. »

L'image fournie est `partition4.img.gz`, une image disque compressée. Il faut y retrouver le flag,
et l'énoncé précise qu'il faudra l'envelopper soi-même dans le format du flag — donc le contenu
trouvé ne sera probablement pas un flag complet.

## Analyse

### Le nom du challenge est un indice
« Timeline 0 » annonce la méthode : le flag n'est pas caché dans un fichier au contenu évident, il
est associé à une **anomalie temporelle**. Un disque contient des milliers de fichiers ; ce qui
distingue celui qui nous intéresse, c'est que ses horodatages ne ressemblent à rien de plausible.

Le système de fichiers stocke classiquement quatre horodatages par entrée : `mtime` (modification du
contenu), `atime` (accès), `ctime` (modification des métadonnées) et `crtime` (création, sur ext4).
L'outil `mactime` les normalise en une chronologie unique. Une entrée qui ne respecte pas la
chronologie globale du système est immédiatement visible.

### Construire la timeline
```bash
gunzip partition4.img.gz
fls -m '/' -r partition4.img > body.txt
mactime -b body.txt > timeline.txt
```

- `fls` liste les entrées du système de fichiers ; `-r` descend récursivement, `-m '/'` produit un
  **bodyfile** au format standard : une ligne par entrée avec inode, chemin, et les quatre
  horodatages.
- `mactime -b` transforme ce bodyfile en chronologie triée.

L'intérêt du bodyfile est qu'il conserve les **inodes** : c'est ce qui permettra d'extraire le
contenu ensuite, indépendamment de l'entrée de répertoire.

### Repérer l'anomalie
```bash
head -20 timeline.txt
grep '1985' timeline.txt
```

La chronologie commence en 2021 : c'est la date de création de l'image. Une entrée datée de
**janvier 1985** est impossible — antérieure de plusieurs décennies à la création du système de
fichiers, et bien avant que quiconque n'ait conçu ce challenge. C'est du **timestomping** : les
horodatages ont été réécrits, soit pour masquer un fichier, soit — ici — pour le signaler.

Le fichier repéré est `/bin/bcab`, inode **4945**. Le choix du chemin est lui aussi parlant : un
binaire dans `/bin` qui porte un nom sans rapport avec les utilitaires système.

## Solution

### Extraire le contenu par inode
```bash
icat partition4.img 4945 > bcab
file bcab
cat bcab
```

`icat` lit les blocs de données pointés par l'inode, sans passer par le répertoire : c'est la bonne
méthode quand on veut être sûr de lire le contenu effectivement associé à l'entrée repérée dans la
timeline, et cela fonctionne même si l'entrée de répertoire a été supprimée.

### Décoder
Le contenu est de l'alphanumérique terminé par un retour à la ligne — le profil exact d'une chaîne
**base64**. Il n'y a pas d'accolades : le fichier contient le corps du flag, pas le flag complet.

```bash
cat bcab | base64 -d ; echo
```

Le décodage donne une chaîne à envelopper dans le format du flag : le corps trouvé, encadré des
accolades attendues.

L'énoncé l'annonçait explicitement (« wrap what you find »), ce qui évite de chercher plus loin une
valeur déjà complète.

### Pourquoi ça marche
Un système de fichiers n'est pas un journal d'audit : les horodatages sont des métadonnées
**modifiables par l'utilisateur**, via `touch`, `utime`, ou directement en écrivant dans l'inode.
Rien ne les rend immuables, et rien ne les chaîne cryptographiquement au contenu. Détecter du
timestomping repose donc sur la **cohérence** : dates antérieures à la création du volume, `mtime`
plus ancien que `crtime`, fichiers système dont les dates sortent de la fenêtre d'installation,
écarts de quelques nanosecondes suspects. Ici le poseur d'anomalie a volontairement choisi 1985 pour
que l'anomalie saute aux yeux d'une chronologie triée : la manipulation d'horodatage est
l'invitation, pas la cachette.

## Pièges

- **Timezone** : `mactime` affiche en UTC par défaut. Utiliser `-z` (ou fixer `TZ`) avant de conclure
  qu'une date « ne colle pas » — un décalage de quelques heures n'est pas une anomalie, un écart de
  36 ans oui.
- **Trier avant de lire** : `grep` sur une chronologie non triée reste efficace, mais c'est le tri qui
  fait ressortir les valeurs aberrantes. Toujours regarder le début et la fin du fichier.
- **`fls` sans `-r`** : sans récursion, on ne voit que le répertoire racine et on rate `/bin/bcab`.
- **Lire par chemin plutôt que par inode** : `icat` accepte un chemin, mais l'inode est plus sûr — et
  c'est la valeur qu'on a sous la main dans le bodyfile.
- **Oublier le `base64 -d`** : le fichier extrait ressemble à du texte aléatoire, on peut croire à un
  faux positif avant de reconnaître l'alphabet base64 (et le `=` de padding absent, car le corps
  fait un multiple de 3 octets).
- **Le flag n'est pas complet** : ne pas soumettre la chaîne décodée telle quelle, l'envelopper dans
  le format demandé.

## Flag

Flag validé sur la plateforme (valeur non conservée).
