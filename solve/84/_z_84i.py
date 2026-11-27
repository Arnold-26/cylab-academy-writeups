import sys, json
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r".")
from cylab2 import CyLab
import wu

cy = CyLab(delay=1.2)
cy.login()
f = "academy{p1LLf3r3d_data_v1a_st3g0}"
st, b = cy.req("POST", "/api/submissions/", {"source": "library", "challenge": 84, "flag": f})
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
