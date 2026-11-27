# 748 — ABSOLUTE NANO

**Événement** : picoCTF 2026 · **Catégorie** : Général Skills

## Énoncé

> You have complete power with nano. Think you can get the flag?

Un accès SSH à la machine du challenge est fourni. L'utilisateur doit élever ses privilèges pour lire `/flag`.

## Analyse

Premier réflexe sur une machine Linux dont on veut lire un fichier racine : énumérer les droits sudo.

```bash
sudo -l
```

La sortie révèle une règle `NOPASSWD` très étroite : `nano` est autorisé, mais **uniquement** sur `/etc/sudoers`.

```text
User picoplayer may run the following commands on ...:
    (root) NOPASSWD: /usr/bin/nano /etc/sudoers
```

Cette règle est censée être prudente : elle limite l'éditeur à un fichier précis, et ce fichier est précisément celui qui contient la politique de sudo. Le raisonnement qui la casse est simple : un éditeur lancé en root sur le fichier de politique, c'est déjà root. `sudo` autorise une **commande**, pas un contenu ; il ne restreint pas ce qui sera écrit dans le fichier ouvert. Il suffit donc d'ajouter une règle permissive pour son propre compte.

C'est le cas d'école des éditeurs autorisés par `sudo` : l'outil est légitime, son usage ne l'est pas.

## Solution

### 1. Énumérer les droits

```bash
id
sudo -l
ls -l /flag
```

`ls -l /flag` échoue en `Permission denied`, ce qui confirme l'objectif.

### 2. Ouvrir le fichier avec le droit accordé

```bash
sudo nano /etc/sudoers
```

`nano` s'ouvre en root sur le fichier de politique. Le contenu ressemble à :

```text
Defaults        env_reset
root    ALL=(ALL:ALL) ALL
%sudo   ALL=(ALL:ALL) ALL
@includedir /etc/sudoers.d
```

### 3. Ajouter la règle pour son compte

On descend en fin de fichier (`Alt+/` puis `Ctrl+W` si besoin de chercher) et on ajoute une ligne, en s'assurant qu'elle commence bien sur une nouvelle ligne :

```text
picoplayer ALL=(ALL) NOPASSWD: ALL
```

Puis on sauve et on quitte :

- `Ctrl+O` — écriture, `nano` propose le nom du fichier, on valide par `Entrée` ;
- `Ctrl+X` — sortie.

La ligne doit se terminer par un saut de ligne : un fichier `sudoers` sans `\n` final peut être refusé au parsing.

### 4. Vérifier et lire le flag

```bash
sudo -l          # la nouvelle règle apparaît
sudo -i          # ou simplement :
sudo cat /flag
```

La règle prend effet immédiatement, sans redémarrage ni reconnexion : `sudo` relit le fichier à chaque invocation.

### Pourquoi ça marche

`sudo` filtre les commandes autorisées, pas les actions qu'elles permettent. Ici, la commande autorisée est un éditeur, et le fichier ouvert est celui qui définit les autorisations. Root écrit donc lui-même la règle qui nous donne root. Le contrôle d'accès est cohérent au moment de la vérification — `nano /etc/sudoers` est bien dans la liste — et inopérant sur l'effet : c'est un privilège qui se réécrit lui-même.

## Pièges

- **Corrompre `/etc/sudoers`.** Une faute de syntaxe rend `sudo` inutilisable pour tout le monde, y compris pour corriger : on relit la ligne ajoutée avant de sauver. C'est la raison pour laquelle un administrateur utilise `visudo`, qui valide le fichier avant écriture — ici, ce garde-fou n'existe pas.
- **Le nom d'utilisateur.** Utiliser le compte réel (`whoami`), pas un nom supposé : une règle sur un compte inexistant n'accorde rien.
- **`Ctrl+O` sans valider le nom.** `nano` demande confirmation du fichier ; valider par `Entrée`, sinon rien n'est écrit.
- **Le terminal.** Avec un `TERM` inconnu, `nano` peut refuser de démarrer (`Error opening terminal`) ; `export TERM=xterm` corrige.
- **Croire que la règle est immédiate mais pas globale.** La règle s'applique au compte courant ; une session `sudo -i` ouverte avant l'édition peut conserver l'ancienne politique en cache, d'où l'intérêt de relancer `sudo -l`.
