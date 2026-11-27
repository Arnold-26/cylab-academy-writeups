import sys, json, pathlib
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r"D:\ctf-index")
from cylab2 import CyLab
import wu

cy = CyLab(delay=1.2)
cy.login()
f = "academy{b1g_numb3rs_f5b03a75}"
st, b = cy.req("GET", "/api/challenges/297/")
already = json.loads(b).get("solved_by_user")
st, b = cy.req("POST", "/api/submissions/", {"source": "library", "challenge": 297, "flag": f})
ok = json.loads(b).get("correct") if b.startswith("{") else None
print(f"297 (deja={already}) -> {ok}")
if ok and not already:
    wu.write(297, "Sequences", "Cryptography", "", "exponentiation matricielle", f,
             "La fonction est une **recurrence lineaire d'ordre 4** ; calculer m(2e7) par "
             "memoisation explose la pile. On utilise la matrice compagnon 4x4 et l'exponentiation "
             "rapide modulo 10^10000 (O(log n) multiplications). Le MD5 du resultat valide la reponse, "
             "puis la cle SHA-256 dechiffre le flag.")
# afficher le script 148
p = pathlib.Path(r"C:\Users\arnol\AppData\Local\Temp\cylab_cr\new_vignere.py")
if p.exists():
    print("\n=== 148 new_vignere.py ===")
    print(p.read_text(encoding="utf-8", errors="replace")[:1500])
