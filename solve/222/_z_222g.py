import sys, json
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r"D:\ctf-index")
from cylab2 import CyLab
import wu

cy = CyLab(delay=1.2)
cy.login()
f = "picoCTF{c0mp1l3r_0pt1m1z4t10n_15_pur3_w1z4rdry_but_n0_pr0bl3m?}"
st, b = cy.req("GET", "/api/challenges/222/")
already = json.loads(b).get("solved_by_user")
st, b = cy.req("POST", "/api/submissions/", {"source": "library", "challenge": 222, "flag": f})
ok = json.loads(b).get("correct") if b.startswith("{") else None
print(f"222 (deja={already}) -> {ok}")
if ok and not already:
    wu.write(222, "not crypto", "Reverse Engineering", "", "hook LD_PRELOAD sur memcmp", f,
             "Le binaire chiffre l'input (AES) puis compare avec `memcmp` au flag dechiffre present en "
             "memoire. Pas besoin de casser l'AES : on intercepte `memcmp` avec un `LD_PRELOAD` qui logue "
             "les deux buffers. `n=64` et le premier argument est le flag en clair. "
             "`gdb -nx` seul tombait sur les memcmp du loader dynamique (comparaisons de version "
             "`GLIBC_2.2.5`), d'ou l'interet du hook qui ne filtre que les comparaisons >= 16 octets.")
