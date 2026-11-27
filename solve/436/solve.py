# 436 - SansAlpha  (General Skills, picoCTF 2024)
# Flag: academy{7h15_mu171v3r53_15_m4dn355_0abcd64b}
# Write-up: ../../../writeups/general-skills/436-sansalpha.md
# This is the script that produced the flag; historical variants are in archive/.
#
import sys, json
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r".")
from cylab2 import CyLab
import wu

cy = CyLab(delay=1.2)
cy.login()
f = "academy{7h15_mu171v3r53_15_m4dn355_0abcd64b}"
st, b = cy.req("GET", "/api/challenges/436/")
already = json.loads(b).get("solved_by_user")
st, b = cy.req("POST", "/api/submissions/", {"source": "library", "challenge": 436, "flag": f})
ok = json.loads(b).get("correct") if b.startswith("{") else None
print(f"436 (deja={already}) -> {ok}")
if ok and not already:
    wu.write(436, "SansAlpha", "General Skills", "", "shell sans lettres : globbing + expansion", f,
             "Le shell n'accepte que les symboles. Techniques : `*` execute le premier fichier avec les "
             "autres en arguments (ce qui renseigne `$_`, le dernier argument = `on-calastran.txt`) ; "
             "`$-` donne les options du shell (lettres disponibles) ; l'expansion `${_:3:2}${_:8:1}` "
             "extrait `ca` + `t` de `on-calastran.txt` -> commande `cat`. Payload final : "
             "`*` puis `*; ${_:3:2}${_:8:1} */????.???` qui fait `cat blargh/flag.txt`.")
