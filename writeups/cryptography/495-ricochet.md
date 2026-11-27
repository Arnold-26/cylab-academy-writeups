# 495 — Ricochet (Crypto / Radio)

**Catégorie** : Cryptography · **Challenge** : #495 · **Événement** : picoCTF 2025

## Énoncé

> I bought this robot to help me locate flags, but the controller is stuck in a demo loop where the robot just goes in circles. Can you exploit the encryption between the controller to navigate the robot to the flag?

## Flag

```
academy{r1gh7_84ck_47_y4_38227532}
```

(soumis, `correct=True`)

Instance : `PUT /api/challenges/495/instance/` donne une URL HTTP avec `/radio_rx` (GET,
**consomme** les messages), `/radio_tx` (POST), `/start`, `/stop`, `/state`.
Sources : `robot.py` (addr 0x20), `robotcontroller.py` (addr 0x10), `crypto.py`,
`radio_interface.py` (pas de `keys.py` : `keys["authenticity_key"]` et
`keys["shared_hmac_key"]` sont côté serveur).

## 1. Le décor

* `/state` → `pos` = **[row, col]** (vérifié : 2 commandes `east`+`south` depuis (0,0) donnent
  `[9,3]`), `map[10][10]`, `log`, `flag`. Le flag est `map[4][8]` = (row 4, col 8).
* Le robot **glisse** jusqu'à l'obstacle suivant ; il ne ramasse le flag que s'il **s'arrête**
  dessus. Boucle de démo du controller : `east, south, west, north` → rectangle
  (0,0)→(0,3)→(9,3)→(9,0)→(0,0), inutile.
* Chemin gagnant (BFS sur les glissades) : `E S E N W S E N E S` →
  (0,3)(9,3)(9,9)(4,9)(4,2)(7,2)(7,6)(0,6)(0,8) puis `south` s'arrête sur (4,8)
  (obstacle `map[5][8]=1`).

Protocole : le robot envoie `validate` (challenge aléatoire) et attend `ack_validate` =
`compute_hmac(challenge, 0, authenticity_key)` ; puis `key_exchange`/`ack_key_exchange`
(X25519) ; puis 20 × (`send_secure_data("get_movement")` + `recv_secure_data()`),
appliqué par `robot_low_level.move(cmd)`.

`secure_*` = JSON `{"message","nonce","hmac"}` chiffré en XChaCha20-Poly1305 avec
`blake2b(dh_shared)[:32]`, MAC = `compute_hmac(message, nonce, shared_hmac_key)`.
Les nonces du robot et du controller avancent en lockstep (+1 par message traité).

## 2. Ce qui ne marche pas

1. **Oracle `validate` = oracle de signature avec `authenticity_key`**, pas avec
   `shared_hmac_key`. Mesuré : on déchiffre `("get_movement",0)` du robot
   (`b8cd2dd9…`) et `oracle("get_movement")` (`c1af686a…`) → **clés différentes**.
   Idem `set_addr` (non authentifié) : ne donne aucune clé.
2. Même avec une clé, `compute_hmac(M,n) == compute_hmac(C,0)` exige que `str(n)` finisse
   par `0` → seuls n ≡ 0 (mod 10) sont forgeables, alors que le robot utilise 0,1,2,…
   Donc on ne peut PAS forger librement.

## 3. L'attaque (2 idées qui se combinent)

### (a) Point DH d'ordre faible → clé partagée connue

`ack_key_exchange` n'est pas authentifié et le robot ne vérifie pas `src`.
On déplace le controller (`set_addr` → 0x99, non authentifié), on relaie
`validate`→`ack_validate` via l'oracle, puis on répond au `key_exchange` du robot avec la
**clé publique nulle** : `X25519(priv, 0) = 0^32` (vérifié avec `pymonocypher` 4.0.3.5,
identique au serveur : `monocypher.key_exchange` renvoie 0 sans erreur pour u = 0, 1, p-1).
Le robot calcule donc `dh_key_shared = 0^32`, clé de chiffrement
`blake2b(0^32)[:32]` → **on déchiffre et chiffre tout**. En re-keyant aussi le controller
(`key_exchange` avec la même clé nulle, il est à 0x99), les deux côtés retombent sur la
même clé connue et le trafic légitime continue.

### (b) Le controller est un **oracle de MAC** pour ses chaînes fixes

Le controller ne signe que `""`, `"east"`, `"south"`, `"west"`, `"north"`, mais **au nonce
de son choix** : il signe le contenu de `send_buffer_secure` avec son nonce courant.
`send_buffer_secure` est fixé par un `get_movement` traité (compteur `movement_counter % 4`)
→ en bourrant le controller de `secure_data`/`secure_data_request` valides (MACs déjà
capturés), on choisit `(direction, nonce)` : `G_{2i}` = nombre de `get_movement` traités
avant le nonce `2i`, et la réponse au nonce `2i+1` vaut `MAC(cycle[G-1 mod 4], 2i+1)`.
On fabrique ainsi, en quelques passes, `MAC(east,5)`, `MAC(east,13)`, `MAC(west,9)` — les
trois signatures manquantes pour le chemin gagnant (les autres venaient du run légitime :
`MAC("",n)` pour tout n, `MAC("get_movement",n)`, et le cycle naturel aux nonces impairs).

### (c) Exécution

On joue le controller : `wait_message` ne vérifie pas `src` et **ne vide pas** le buffer
entre les runs (`receive_buffer` n'est jamais reset), donc on peut **pré-charger tout le
dialogue** dans le buffer du robot : `ack("",0), resp(cmd0,1), ack("",2), resp(cmd1,3), …`
en réutilisant les MACs collectés (clé HMAC statique = valable pour toute instance).
Le robot consomme la file dans l'ordre, glisse de case en case et s'arrête sur (4,8) :

```
[2026-11-27 02:00:18.416] Robot found a FLAG: academy{r1gh7_84ck_47_y4_38227532}
```

## 4. Scripts

* `_z_495src\` — sources copiées de `/tmp/r495`.
* `_z_495_lib.py` — API radio + crypto exacte (`pymonocypher`), `Z = bytes(32)`.
* `_z_495_atk.py` — `phaseA` (MITM + capture du run légitime → table de MACs),
  `phaseB` (passes d'oracle), `phaseC` (exécution), `launch()` (démarre l'instance).
* `_z_495_final.py` / `_z_495_fin2.py` — one-shot : passes + blast du dialogue.
* `_z_495_path.py` / `_z_495_path2.py` — BFS des glissades et des directions atteignables.
* `_z_495_macs.json` — table `(message, nonce) → hmac` (80 entrées + extras), statique,
  réutilisable sur toute instance (les clés de `keys.py` ne changent pas).

## 5. Notes

* Les `monocypher.lock` de pymonocypher renvoient `(tag, ciphertext)` ;
  `crypto.encrypt` écrit `ciphertext;tag;nonce`. HMAC = BLAKE2b-512, itéré 32 fois.
* Instances très courtes (~1–2 min) et ~0,5 s par requête HTTP → tout faire en un run
  (passes + exécution ≈ 40 s), la table de MACs étant sauvée sur disque entre les essais.
* `/stop` + `/start` réinitialise les nonces des DEUX appareils (vérifié : la boucle de
  démo rejoue à l'identique).

## Scripts

- [`solve.py`](../../solve/495/solve.py)
- [`_z_495_atk.py`](../../solve/495/_z_495_atk.py)
- [`_z_495_lib.py`](../../solve/495/_z_495_lib.py)
- [`_z_495_macs.json`](../../solve/495/_z_495_macs.json)
