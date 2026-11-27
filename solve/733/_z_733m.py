import sys, json
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r"D:\ctf-index")
from cylab2 import CyLab
import wu

cy = CyLab(delay=1.2)
cy.login()
f = "academy{u_Us3d_pwNt00L5_af37c96d}"
st, b = cy.req("GET", "/api/challenges/733/")
already = json.loads(b).get("solved_by_user")
st, b = cy.req("POST", "/api/submissions/", {"source": "library", "challenge": 733, "flag": f})
ok = json.loads(b).get("correct") if b.startswith("{") else None
print(f"733 (deja={already}) -> {ok}")
if ok and not already:
    wu.write(733, "offset-cycle", "Binary Exploitation", "", "ret2win avec offset variable", f,
             "Le service SSH genere aleatoirement un binaire 32 bits (source C fournie) : `vuln` fait "
             "`gets(buf)` avec un `BUFSIZE` variable, et `win()` lit le flag. L'offset de l'adresse de "
             "retour vaut `BUFSIZE + 12` (padding du compilateur). On le determine dynamiquement en "
             "envoyant `0x42424242` a differentes positions et en lisant la valeur affichee par "
             "`get_return_address()`, puis on ecrase l'adresse de retour par `win` (non-PIE, 0x80491e6).")
