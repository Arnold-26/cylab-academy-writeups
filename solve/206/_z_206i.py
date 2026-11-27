import sys, json
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r".")
from cylab2 import CyLab
import wu

cy = CyLab(delay=1.2)
cy.login()
f = "picoCTF{n0_t1m3_t0_w4st3_5hufflin9_ar0und}"
st, b = cy.req("GET", "/api/challenges/206/")
already = json.loads(b).get("solved_by_user")
st, b = cy.req("POST", "/api/submissions/", {"source": "library", "challenge": 206, "flag": f})
ok = json.loads(b).get("correct") if b.startswith("{") else None
print(f"206 (deja={already}) -> {ok}")
if ok and not already:
    wu.write(206, "scrambled-bytes", "Forensics", "", "seed PRNG + inversion de shuffle", f,
             "`send.py` fait `random.seed(int(time()))`, **shuffle** le fichier, puis envoie chaque "
             "octet dans un paquet UDP : port source = `randrange(65536)`, charge = "
             "`octet ^ randrange(256)`. Le pcapng contient les paquets (dupliques 2x par la capture). "
             "On brute-force le seed autour de l'horodatage du premier paquet en comparant les ports "
             "source (6 suffisent), puis on rejoue le PRNG pour annuler le XOR et on **inverse le "
             "shuffle** (les swaps se rejouent en ordre inverse, avec `i = N-1-idx`). Le fichier "
             "reconstruit est un PNG contenant le flag.")
