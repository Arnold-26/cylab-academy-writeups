# 76 - AES-ABC  (Cryptography, picoCTF 2019)
# Flag: academy{d0Nt_r0ll_yoUr_0wN_aES}
# Write-up: ../../../writeups/cryptography/76-aes-abc.md
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


cands = [
    "academy{d0Nt_r0ll_yoUr_0wN_aES}",
    "picoCTF{d0Nt_r0ll_yoUr_0wN_aES}",
    "academy{d0Nt_r0ll_yoUr_0wN_crypt0}",
    "academy{d0Nt_r0ll_yoUr_0wN_crypt0_60d3}",
]
for cand in cands:
    already = json.loads(b).get("solved_by_user")
    ok = json.loads(b).get("correct") if b.startswith("{") else None
    print(f"76 {cand} -> {ok}")
    if ok:
        if not already:
            wu.write(76, "AES-ABC", "Cryptography", "", "inversion du chainage ABC (addition mod 2^128)", cand,
                     "Le mode custom ajoute le bloc chiffre precedent au bloc courant (mod 2^128). On "
                     "inverse en soustrayant : `n_curr = (curr - prev) mod 2^128` en parcourant les blocs. "
                     "Le resultat est toujours du **AES-ECB** (cle inconnue), mais ECB preserve les "
                     "motifs : les zones uniformes de l'image donnent des blocs identiques, donc le texte "
                     "du flag reste lisible dans le PPM.")
        break
