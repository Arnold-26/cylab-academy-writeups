import sys, json
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r"D:\ctf-index")
from cylab2 import CyLab
import wu

cy = CyLab(delay=1.2)
cy.login()
f = "picoCTF{4ny0n3_g0t_r1scv_h4rdw4r3?_LGUfwl8xyMUlpgvz}"
st, b = cy.req("GET", "/api/challenges/219/")
already = json.loads(b).get("solved_by_user")
st, b = cy.req("POST", "/api/submissions/", {"source": "library", "challenge": 219, "flag": f})
ok = json.loads(b).get("correct") if b.startswith("{") else None
print(f"219 riscy (deja={already}) -> {ok}")
if ok and not already:
    wu.write(219, "riscy business", "Reverse Engineering", "", "RC4 avec cle = les 8 premiers octets de l'entree", f,
             "Binaire **RISC-V** statique stripped, execute avec `qemu-riscv64`. Le desassemblage montre une "
             "implementation **RC4** : KSA a 0x10086 (table de 256 octets, `remu`, swaps) puis PRGA a "
             "0x100d2. Le `main` appelle la KSA avec `a1 = entree`, `a2 = 8` : **la cle RC4 est les 8 "
             "premiers octets de l'entree**, donc `picoCTF{` puisque le flag commence par la. Le chiffre "
             "attendu est en `.rodata` a 0x10210 (52 octets, compare jusqu'a 0x10244). Dechiffrer avec la "
             "cle `picoCTF{` donne directement le flag.")
