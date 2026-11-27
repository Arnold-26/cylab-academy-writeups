# 740 — Piece by Piece

**Événement** : picoCTF 2026 · **Catégorie** : General Skills

> Synthèse rédigée à partir des sources publiques listées en fin de fiche : ce challenge a été
> résolu côté CyLab Academy, mais le writeup d'origine n'a pas été conservé.

## Énoncé
« After logging in, you will find multiple file parts in your home directory. These parts need to be
combined and extracted to reveal the flag. » Accès SSH à la machine du challenge.

## Analyse
Le répertoire personnel contient un fichier d'instructions et plusieurs **morceaux** d'une même
archive. `instructions.txt` donne tout le nécessaire : le flag est découpé dans un ZIP, il faut
recombiner les morceaux avec les commandes Linux, et le ZIP est protégé par le mot de passe
`supersecret`.

La recombination se fait avec `cat` (dont le nom vient de *concatenate*) : `cat part_* > combined.zip`.
Le point d'attention est l'**ordre** : le shell développe le glob par ordre alphabétique, ce qui est
correct pour un découpage `part_aa`, `part_ab`, … ou `part_01`, `part_02`, … mais peut casser avec une
numérotation non nulle-paddée (`part_10` avant `part_2`). Il faut donc toujours vérifier le glob
(`ls -v *part*`) avant de concaténer, puis `file` sur le résultat pour confirmer qu'on obtient bien un
ZIP.

## Solution
```bash
ssh ctf-player@<HOST> -p <PORT>
ls -la
cat instructions.txt
ls -v *part*
cat part_* > combined.zip
file combined.zip
unzip -P supersecret combined.zip
cat flag.txt
```
Le flag apparaît dans le fichier texte extrait.

## Flag
```
picoCTF{z1p_and_spl1t_f1l3s_4r3_fun_27804340}
```

## Sources
- https://picoctfsolutions.com/picoctf-2026-piece-by-piece — page de solution picoCTF 2026 (concaténation, ordre du glob, mot de passe du ZIP)
- https://qiita.com/8omp/items/8e1aa38aeda96fa0ecb6 — writeup picoCTF 2026 General Skills (contenu de `instructions.txt`, flag complet)
