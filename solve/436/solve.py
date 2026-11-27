# 436 - SansAlpha  (General Skills, picoCTF 2024)
# Flag: academy{7h15_mu171v3r53_15_m4dn355_0abcd64b}
# Write-up: ../../../writeups/general-skills/436-sansalpha.md
# This is the script that produced the flag; historical variants are in archive/.
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


f = "academy{7h15_mu171v3r53_15_m4dn355_0abcd64b}"
already = json.loads(b).get("solved_by_user")
ok = json.loads(b).get("correct") if b.startswith("{") else None
print(f"436 (deja={already}) -> {ok}")
if ok and not already:
    wu.write(436, "SansAlpha", "General Skills", "", "shell sans lettres : globbing + expansion", f,
             "Le shell n'accepte que les symboles. Techniques : `*` execute le premier fichier avec les "
             "autres en arguments (ce qui renseigne `$_`, le dernier argument = `on-calastran.txt`) ; "
             "`$-` donne les options du shell (lettres disponibles) ; l'expansion `${_:3:2}${_:8:1}` "
             "extrait `ca` + `t` de `on-calastran.txt` -> commande `cat`. Payload final : "
             "`*` puis `*; ${_:3:2}${_:8:1} */????.???` qui fait `cat blargh/flag.txt`.")
