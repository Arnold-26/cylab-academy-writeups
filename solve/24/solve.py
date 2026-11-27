# 24 - Forky  (Reverse Engineering, picoCTF 2019)
# Flag: academy{-721750240}
# Write-up: ../../../writeups/reverse-engineering/24-forky.md
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


cands = ["academy{3573217056}", "3573217056", "academy{-721750240}", "-721750240"]
for cand in cands:
    already = json.loads(b).get("solved_by_user")
    ok = json.loads(b).get("correct") if b.startswith("{") else None
    print(f"24 {cand} -> {ok}")
    if ok:
        if not already:
            wu.write(24, "Forky", "Reverse Engineering", "", "analyse de fork + mmap partage", cand,
                     "Le programme `mmap` une zone **partagee** initialisee a 0x3B9ACA00 (1000000000), "
                     "puis `fork()` 4 fois (16 processus). Chaque processus ajoute 0x499602D2 "
                     "(1234567890) a la valeur partagee et passe le resultat a `doNothing`. Le dernier "
                     "appel recoit la valeur apres les 16 additions : 1000000000 + 16*1234567890 "
                     "mod 2^32 = 3573217056.")
        break
