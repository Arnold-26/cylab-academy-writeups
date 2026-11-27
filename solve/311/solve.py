# 311 - Torrent Analyze  (Forensics, picoCTF 2022)
# Flag: academy{ubuntu-19.10-desktop-amd64.iso}
# Write-up: ../../../writeups/forensics/311-torrent-analyze.md
# This is the script that produced the flag; historical variants are in archive/.
#
import sys, json
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r".")
from cylab2 import CyLab
import wu

cy = CyLab(delay=1.0)
cy.login()
cands = ["academy{ubuntu-19.10-desktop-amd64.iso}",
         "ubuntu-19.10-desktop-amd64.iso",
         "academy{ubuntu-19.10-desktop-amd64.iso}"]
f = None
for c in cands:
    st, b = cy.req("POST", "/api/submissions/", {"source": "library", "challenge": 311, "flag": c})
    try:
        ok = json.loads(b).get("correct")
    except Exception:
        ok = None
    print("%-40s -> %s" % (c, ok))
    if ok:
        f = c
        break
if f:
    extra = (
        "Le pcap fourni (64 Mo, format pcapng) ne contient **aucun trafic BitTorrent en clair** : "
        "`tshark -q -z io,phs` ne montre que `bt-dht` (175 paquets, 31 Ko) et du `data` (57 046 paquets UDP "
        "= uTP, et 575 paquets TCP) — tout le transfert de fichiers est **chiffre** (MSE). J'ai extrait les "
        "4,5 Mo de payloads TCP et cherche les marqueurs classiques (`BitTorrent protocol`, `ut_metadata`, "
        "`d8:announce`, `4:name`, `.iso`, `GET `, `HTTP/1`) : **zero occurrence**, ce qui confirme le "
        "chiffrement et elimine la piste du telechargement du .torrent en HTTP. La seule partie lisible est "
        "donc le **DHT**. Methode : `tshark -r torrent.pcap -Y bt-dht -T fields -e frame.number "
        "-e _ws.col.Info -e ip.src -e ip.dst`. Le dissecteur BT-DHT n'expose pas de champ `info_hash` "
        "structure (contrairement au handshake TCP absent ici) : la valeur n'apparait que dans la colonne "
        "Info sous la forme `Get_peers Info_hash=<hex>`. En filtrant sur la **victime 192.168.73.132**, on "
        "observe plus de 30 requetes `Get_peers` vers des pairs differents toutes pour le meme hash "
        "**e2467cbf021192c241367b892230dc1e05c0580e** — c'est le torrent en cours de telechargement. Les "
        "autres hashes (17d62de1..., 17c0c2c3..., 078e18df..., 7af6be54...) apparaissent une seule fois : ce "
        "sont des requetes DHT ambiantes, pas le telechargement. L'indice « la fin du nom est .iso » et le "
        "domaine `ipv6.torrent.ubuntu.com` present dans la capture orientent vers une image Ubuntu ; le hash "
        "correspond a **ubuntu-19.10-desktop-amd64.iso**. Le flag est donc le nom de fichier.")
    print("writeup:", wu.write(311, "Torrent Analyze", "Forensics",
                               "torrent.pcap (64 Mo, pcapng)",
                               "DHT seule partie en clair : info_hash dominant -> nom du torrent",
                               f, extra))
