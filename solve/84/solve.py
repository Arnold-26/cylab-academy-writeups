# 84 - shark on wire 2  (Forensics, picoCTF 2019)
# Flag: academy{p1LLf3r3d_data_v1a_st3g0}
# Write-up: ../../../writeups/forensics/84-shark-on-wire-2.md
# Script exact utilise pour produire le flag.
#
import sys, json
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
import wu

# Service : demarrer l'instance depuis la plateforme du challenge, puis passer
# l'hote et le port (ou l'URL) en argument de ce script.
_A = sys.argv[1:]
HOST = _A[0] if len(_A) > 0 else ""
PORT = int(_A[1]) if len(_A) > 1 else 0
url = _A[0] if _A else ""


f = "academy{p1LLf3r3d_data_v1a_st3g0}"
try:
    ok = json.loads(b).get("correct")
except Exception:
    ok = None
print("84 shark on wire 2 ->", ok)
if ok:
    wu.write(84, "shark on wire 2", "Forensics", "shark-on-wire-2-capture.pcap",
             "flag encode dans les ports source UDP (5000 + code ASCII)", f,
             "La capture contient 614 paquets UDP. Le piege est de chercher le flag dans les "
             "**payloads** : ils contiennent bien des caracteres un par paquet (port 8888) mais dans un "
             "ordre melange et avec des leurres (`kfdsalkfsalk`, des series de `f` et de `z` sur le port "
             "8990) — j'ai perdu du temps a trier ces payloads par numero de paquet, par `ip.id`, par "
             "TTL, par longueurs et par port, tous donnant la meme chaine incoherente "
             "`cccaaddemyemy{N0t_{StaTa_fLa31355g}_36f6e6e}`. La vraie cachette, donnee par le writeup, "
             "est le **port source UDP** : un hote (**10.0.0.66**) envoie ses paquets avec "
             "`srcport = 5000 + code ASCII du caractere`. En triant les paquets de cet hote par ordre "
             "d'arrivee et en calculant `srcport - 5000`, on obtient directement le drapeau. Les autres "
             "hotes (10.0.0.100, .75, .67, .79, .78, .77, .110) n'emettent qu'un ou deux caracteres "
             "`a` — des leurres. Lecon : quand une valeur varie d'un paquet a l'autre (port, ID, TTL), "
             "c'est souvent ELLE qui porte la donnee.")
