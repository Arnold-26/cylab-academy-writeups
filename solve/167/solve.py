# 167 - Binary Gauntlet 0  (Binary Exploitation, picoCTF 2021)
# Flag: not archived
# Write-up: ../../../writeups/binary-exploitation/167-binary-gauntlet-0.md
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


f = "088d0d0dfed3a7c041027e01d85e0887"
already = json.loads(b).get("solved_by_user")
ok = json.loads(b).get("correct") if b.startswith("{") else None
print(f"167 (deja={already}) -> {ok}")
if ok and not already:
    wu.write(167, "Binary Gauntlet 0", "Binary Exploitation", "", "buffer overflow -> SIGSEGV handler", f,
             "Le programme lit le flag dans un buffer global, installe un **handler SIGSEGV** qui "
             "l'imprime, puis fait `strcpy(dest[128], input)` sans verifier la taille. Il suffit "
             "d'envoyer 144 octets + une adresse invalide pour ecraser l'adresse de retour, provoquer "
             "un segfault et faire afficher le flag.")
