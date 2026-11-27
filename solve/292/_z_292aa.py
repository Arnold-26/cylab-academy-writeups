import sys, json
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r"D:\ctf-index")
from cylab2 import CyLab
import wu

cy = CyLab(delay=1.2)
cy.login()
f = "academy{5n47ch_7h3_5h311_ddd0ca99}"
st, b = cy.req("GET", "/api/challenges/292/")
d = json.loads(b)
print("nom:", d.get("name"), "| deja:", d.get("solved_by_user"))
st, b = cy.req("POST", "/api/submissions/", {"source": "library", "challenge": 292, "flag": f})
ok = json.loads(b).get("correct") if b.startswith("{") else None
print(f"292 ropfu -> {ok}")
if ok and not d.get("solved_by_user"):
    wu.write(292, "ropfu", "Binary Exploitation", "nc xebec.cylabacademy.net <port>",
             "ROP 32 bits statique : read(/bin/sh) puis execve via int 0x80", f,
             "Binaire **32 bits statiquement lie** et non-PIE, avec `gets(buf)` sur un buffer de 16 "
             "octets et AUCUNE fonction win : il faut un ROP syscall. Contraintes reelles rencontrees : "
             "(1) `gets` s'arrete au octet 0x0a, donc tous les gadgets dont l'adresse contient 0x0a "
             "sont interdits — `pop eax; ret` n'existait qu'en 0x080ab50d et 0x080ad37c, tous deux "
             "inutilisables ; j'ai contourne avec `mov eax,3; ret` (0x0809dae0) puis `add eax,2/3; ret` "
             "pour atteindre eax=11. (2) Aucun `pop edx; ret` : utilise "
             "`pop edx; pop ebx; pop esi; ret` (0x0805848e) pour edx=8, et "
             "`xor edx,edx; pop ebx; mov eax,edx; pop esi; pop edi; pop ebp; ret` (0x0804c325) pour "
             "edx=0. (3) Piege de scan : un motif `... c3` n'est pas forcement un `ret` — a "
             "0x08093fd3 le c3 appartenait a `mov ebx,eax` et le gadget finissait par `div`, provoquant "
             "un SIGFPE ; il faut toujours desassembler le gadget avant usage. (4) `int 0x80; ret` "
             "n'existe qu'a 0x0805e4b0 (l'autre est suivi d'un `jmp`). (5) Piege d'I/O majeur : `gets` "
             "passe par stdio BUFFERISE, donc envoyer le payload et `/bin/sh` d'un coup fait avaler la "
             "suite par le buffer de stdio et le `read()` brut ne recoit RIEN ; il faut envoyer "
             "`/bin/sh\\0` APRES un delai (verifie en local sous gdb : le registre ebx pointait bien sur "
             "0x80e5000 mais la chaine etait vide). Chaine finale : read(0, .bss, 8) puis "
             "execve(.bss, 0, 0), offset de retour 28 (buf a ebp-0x18, plus `push ebx`).")
