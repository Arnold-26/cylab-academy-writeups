# 219 - riscy business  (Reverse Engineering, picoMini by redpwn)
# Flag: picoCTF{4ny0n3_g0t_r1scv_h4rdw4r3?_LGUfwl8xyMUlpgvz}
# Write-up: ../../../writeups/reverse-engineering/219-riscy-business.md
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


f = "picoCTF{4ny0n3_g0t_r1scv_h4rdw4r3?_LGUfwl8xyMUlpgvz}"
already = json.loads(b).get("solved_by_user")
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
