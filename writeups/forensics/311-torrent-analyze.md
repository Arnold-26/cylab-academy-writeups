# Torrent Analyze

**Catégorie** : Forensics · **Challenge** : #311 · **Résolu le** : 2026-11-25

## Énoncé

> torrent.pcap (64 Mo, pcapng)

## Résolution

Méthode : **DHT seule partie en clair : info_hash dominant -> nom du torrent**.

Le pcap fourni (64 Mo, format pcapng) ne contient **aucun trafic BitTorrent en clair** : `tshark -q -z io,phs` ne montre que `bt-dht` (175 paquets, 31 Ko) et du `data` (57 046 paquets UDP = uTP, et 575 paquets TCP) — tout le transfert de fichiers est **chiffre** (MSE). J'ai extrait les 4,5 Mo de payloads TCP et cherche les marqueurs classiques (`BitTorrent protocol`, `ut_metadata`, `d8:announce`, `4:name`, `.iso`, `GET `, `HTTP/1`) : **zero occurrence**, ce qui confirme le chiffrement et elimine la piste du telechargement du .torrent en HTTP. La seule partie lisible est donc le **DHT**. Methode : `tshark -r torrent.pcap -Y bt-dht -T fields -e frame.number -e _ws.col.Info -e ip.src -e ip.dst`. Le dissecteur BT-DHT n'expose pas de champ `info_hash` structure (contrairement au handshake TCP absent ici) : la valeur n'apparait que dans la colonne Info sous la forme `Get_peers Info_hash=<hex>`. En filtrant sur la **victime 192.168.73.132**, on observe plus de 30 requetes `Get_peers` vers des pairs differents toutes pour le meme hash **e2467cbf021192c241367b892230dc1e05c0580e** — c'est le torrent en cours de telechargement. Les autres hashes (17d62de1..., 17c0c2c3..., 078e18df..., 7af6be54...) apparaissent une seule fois : ce sont des requetes DHT ambiantes, pas le telechargement. L'indice « la fin du nom est .iso » et le domaine `ipv6.torrent.ubuntu.com` present dans la capture orientent vers une image Ubuntu ; le hash correspond a **ubuntu-19.10-desktop-amd64.iso**. Le flag est donc le nom de fichier.

## Flag

```
academy{ubuntu-19.10-desktop-amd64.iso}
```

## Ce qu'il faut retenir

—

## Scripts

- [`_z_311a.py`](../../solve/311/_z_311a.py)
- [`_z_311a.sh`](../../solve/311/_z_311a.sh)
- [`_z_311b.py`](../../solve/311/_z_311b.py)
- [`_z_311b.sh`](../../solve/311/_z_311b.sh)
- [`_z_311c.py`](../../solve/311/_z_311c.py)
- [`_z_311c.sh`](../../solve/311/_z_311c.sh)
- [`_z_311d.py`](../../solve/311/_z_311d.py)
- [`_z_311d.sh`](../../solve/311/_z_311d.sh)
- [`_z_311e.py`](../../solve/311/_z_311e.py)
- [`_z_311e.sh`](../../solve/311/_z_311e.sh)
- [`_z_311f.py`](../../solve/311/_z_311f.py)
- [`_z_311f.sh`](../../solve/311/_z_311f.sh)
- [`_z_311g.sh`](../../solve/311/_z_311g.sh)
- [`_z_311h.py`](../../solve/311/_z_311h.py)
- [`_z_311h.sh`](../../solve/311/_z_311h.sh)
- [`_z_311i.py`](../../solve/311/_z_311i.py)
- [`_z_311i.sh`](../../solve/311/_z_311i.sh)
- [`_z_311j.sh`](../../solve/311/_z_311j.sh)
- [`_z_311k.sh`](../../solve/311/_z_311k.sh)
- [`_z_311l.sh`](../../solve/311/_z_311l.sh)
- [`_z_311m.sh`](../../solve/311/_z_311m.sh)
