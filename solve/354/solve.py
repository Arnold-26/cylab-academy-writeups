# 354 - Invisible WORDs  (Forensics, picoCTF 2023)
# Flag: academy{w0rd_d4wg_y0u_f0und_5h3113ys_m4573rp13c3_2a058da1}
# Write-up: ../../../writeups/forensics/354-invisible-words.md
# This is the script that produced the flag; historical variants are in archive/.
#
import sys, json
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r".")
from cylab2 import CyLab
import wu

cy = CyLab(delay=1.2)
cy.login()
f = "academy{w0rd_d4wg_y0u_f0und_5h3113ys_m4573rp13c3_2a058da1}"
st, b = cy.req("GET", "/api/challenges/354/")
already = json.loads(b).get("solved_by_user")
st, b = cy.req("POST", "/api/submissions/", {"source": "library", "challenge": 354, "flag": f})
ok = json.loads(b).get("correct") if b.startswith("{") else None
print(f"354 (deja={already}) -> {ok}")
if ok and not already:
    wu.write(354, "Invisible WORDs", "Forensics", "", "ZIP cache dans un BMP (2 octets sur 4)", f,
             "Le BMP 960x540 32bpp contient un **ZIP** a l'offset 0x8c, mais chaque groupe de 4 octets "
             "n'en garde que 2 (les 2 autres sont du remplissage). On lit `data[i:i+2]` en sautant de 4 "
             "en 4 depuis 0x8c jusqu'a tomber sur `\\xff\\x00`, on ecrit le ZIP, on l'ouvre : il contient "
             "`ZnJhbmtlbnN0ZWluLXRlc3QudHh0` (= base64 de `frankenstein-test.txt`, le texte de "
             "Frankenstein) qui contient le flag.")
