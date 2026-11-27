import sys, json, time
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r"D:\ctf-index")
from cylab2 import CyLab
import wu

cy = CyLab(delay=1.5)
cy.login()
f = "academy{f0und_1t_54c420aa}"
for attempt in range(4):
    st, b = cy.req("POST", "/api/submissions/", {"source": "library", "challenge": 70, "flag": f})
    try:
        ok = json.loads(b).get("correct")
    except Exception:
        print("reponse non JSON (essai %d): %r" % (attempt + 1, b[:120]))
        time.sleep(2)
        continue
    print("70 Investigative Reversing 0 ->", ok)
    if ok:
        wu.write(70, "Investigative Reversing 0", "Forensics",
                 "binary + investigative-reversing-0-mystery.png",
                 "donnees apres IEND + inversion des decalages du binaire", f,
                 "Deux fichiers : un binaire ELF PIE et une image PNG. L'image affiche « WHERE'D THE "
                 "FLAG GO! » et le binaire est un **leurre** (« No flag found. You don't need to run "
                 "this to solve it. »). Le desassemblage de `main` montre pourtant le procede : il lit "
                 "26 octets dans flag.txt et les ecrit avec `fputc` en appliquant des decalages — "
                 "octets 0..5 inchanges, octets 6..14 **+5**, octet 15 **-3**, octets 16..25 "
                 "inchanges. L'image PNG contient **26 octets APRES le chunk IEND** : "
                 "`academ~\\x80k5zsid6q_54c420aa}`. En inversant les decalages (-5 sur 6..14, +3 sur "
                 "l'octet 15) on retrouve `academy{f0und_1t_54c420aa}`. Les scans LSB exhaustifs "
                 "(6 ordres de canaux x 8 bits x 5 pas) ne donnaient RIEN, ce qui confirmait que le "
                 "flag n'etait pas dans les pixels mais **apres la fin du fichier** ; les octets `~` et "
                 "`\\x80` non imprimables trahissaient le decalage. Morale : toujours verifier "
                 "`len(fichier) - position_IEND`.")
        break
    time.sleep(1)
