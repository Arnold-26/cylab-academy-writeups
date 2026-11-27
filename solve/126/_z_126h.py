import sys, json
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r"D:\ctf-index")
from cylab2 import CyLab
import wu

cy = CyLab(delay=1.2)
cy.login()
f = "fa9a2d95e569c1fff8525782765f2a13"
st, b = cy.req("POST", "/api/submissions/", {"source": "library", "challenge": 126, "flag": f})
try:
    ok = json.loads(b).get("correct")
except Exception:
    ok = None
print("126 Binary Gauntlet 1 ->", ok)
if ok:
    wu.write(126, "Binary Gauntlet 1", "Binary Exploitation", "nc chatelaine.cylabacademy.net <port>",
             "shellcode sur pile executable, adresse fuitee par printf(\"%p\")", f,
             "Binaire **64 bits non-PIE avec NX DESACTIVE** (`GNU_STACK ... RWE`) : la pile est "
             "executable, donc pas besoin de ROP. Le programme fait `malloc(1000)`, puis "
             "`printf(\"%p\\n\", &stack_buf)` qui **fuite l'adresse du buffer de pile** (rbp-0x70), puis "
             "DEUX `fgets` successifs dans le tas, puis `strcpy(stack_buf, heap_buf)` — le debordement "
             "vient donc du **second** `fgets`, pas du premier (erreur qui m'a coute 6 essais : le "
             "payload etait consomme par le premier). Le buffer fait 0x70 octets, suivi de rbp (8) donc "
             "l'adresse de retour est a **l'offset 120**. Exploit : envoyer une ligne bidon, puis "
             "`shellcode + '\\x90'*(0x70-23) + 'B'*8 + p64(adresse_fuite)`. Shellcode execve(\"/bin/sh\") "
             "de 23 octets, choisi **sans 0x00 ni 0x0a** (fgets s'arrete au newline et strcpy au NUL ; "
             "l'adresse de pile n'a que 6 octets significatifs, donc la troncature par strcpy est "
             "inoffensive). On obtient un shell : `cat flag.txt` donne un flag SANS wrapper "
             "`academy{}`, conformement a l'enonce.")
