# 220 - breadth  (Reverse Engineering, picoMini by redpwn)
# Flag: picoCTF{...}
# Write-up: ../../../writeups/reverse-engineering/220-breadth.md
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


cands = ["picoCTF{VnDB2LUf1VFJkdfDJtdYtFlMexPxXS6X}",
         "picoCTF{4bcrDtoAzV2WHUgoZ10iearXvtMKNr6u}"]
for f in cands:
    already = json.loads(b).get("solved_by_user")
    ok = json.loads(b).get("correct") if b.startswith("{") else None
    print(f"220 {f} -> {ok}")
    if ok:
        if not already:
            wu.write(220, "breadth", "Reverse Engineering", "", "diff de deux binaires (v1/v2)", f,
                     "`breadth.v1` et `breadth.v2` font 2605312 octets et ne different que de **36 octets**. "
                     "Un build-id, un octet dans une chaine de version, et surtout 14 octets de code dans "
                     "`fcnkKTQpF` (0x95040) : v1 fait `mov eax,0xd037803a; cmp rdx,rax` (comparaison "
                     "toujours fausse) alors que v2 fait `cmp rax,0x41bc73e`, la valeur qu'il vient de "
                     "stocker. La version `v2` passe donc le test et `puts` affiche le flag. Le binaire "
                     "contient des centaines de faux flags `picoCTF{...}` : il faut lire celui reference "
                     "par le `puts` de la fonction corrigee (offset fichier 0x155ef8), pas chercher avec "
                     "`strings`.")
        break
