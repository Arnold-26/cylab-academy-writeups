# 756 — Failure Failure

**Événement** : picoCTF 2026 · **Catégorie** : General Skills

> Synthèse rédigée à partir des sources publiques listées en fin de fiche : ce challenge a été
> résolu côté CyLab Academy, mais le writeup d'origine n'a pas été conservé.

## Énoncé

> Welcome to Failure Failure - a high-availability system challenge. It simulates a real-world
> failover scenario where one server is prioritized over the other. A load balancer stands between
> you and the flag - it won't hand over the flag until you force its hand.

La configuration HAProxy et le code applicatif sont fournis.

## Analyse

En visitant l'URL, le serveur primaire répond « No flag in this service ». La lecture des fichiers
fournis montre le mécanisme : le primaire applique une limite de **300 requêtes par minute** et
renvoie un `503` au-delà ; HAProxy bascule vers le serveur de secours dès qu'il voit une réponse
non-200 ; c'est ce serveur de secours qui rend le flag. La sécurité du montage repose donc sur la
santé du primaire : il suffit de saturer volontairement son quota pour déclencher le basculement.

## Solution

1. Lire `haproxy.cfg` et le code applicatif pour confirmer le seuil (300/min) et la condition de
   bascule (non-200).
2. Inonder le primaire en parallèle pour dépasser le quota en moins d'une minute :

```bash
seq 1 500 | xargs -P50 -I {} curl -s http://<HOST>:<PORT>/ -o /dev/null
sleep 2          # laisser HAProxy détecter l'échec
curl http://<HOST>:<PORT>/     # sert désormais le backup → flag
```

3. La dernière requête est servie par le serveur de secours et contient le flag.

## Flag

```
picoCTF{f4il0v3r_f0r_7h3_w1n_...}
```

Préfixe publié par picoCTF Solutions (suffixe masqué à la source) : le flag complet n'est pas
recopié ici.

## Sources

- [picoCTF Solutions — Failure Failure (picoCTF 2026)](https://picoctfsolutions.com/picoctf-2026-failure-failure)
