import sys, json, time
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r"D:\ctf-index")
from cylab2 import CyLab
import wu

cy = CyLab(delay=1.5)
cy.login()
f = "academy{f0und_1t_54c420aa}"
for i in range(10):
    st, b = cy.req("POST", "/api/submissions/", {"source": "library", "challenge": 70, "flag": f})
    if st == 503 or not b.startswith("{"):
        print("essai %d : plateforme indisponible (status %s)" % (i + 1, st), flush=True)
        time.sleep(30)
        continue
    ok = json.loads(b).get("correct")
    print("70 ->", ok)
    if ok:
        wu.write(70, "Investigative Reversing 0", "Forensics",
                 "binary + investigative-reversing-0-mystery.png",
                 "donnees apres IEND + inversion des decalages du binaire", f,
                 "Image PNG affichant « WHERE'D THE FLAG GO! » + binaire leurre (« No flag found. You "
                 "don't need to run this to solve it. »). Le desassemblage de `main` revele malgre "
                 "tout le procede : lecture de 26 octets et ecriture par `fputc` avec des decalages — "
                 "octets 0..5 inchanges, octets 6..14 **+5**, octet 15 **-3**, octets 16..25 "
                 "inchanges. Le PNG contient **26 octets apres le chunk IEND** : "
                 "`academ~\\x80k5zsid6q_54c420aa}` ; en inversant (-5 puis +3) on obtient le drapeau. "
                 "Les scans LSB exhaustifs (6 ordres x 8 bits x 5 pas) ne donnaient rien, ce qui "
                 "prouvait que le flag etait hors des pixels. Les octets non imprimables `~` et "
                 "`\\x80` trahissaient le decalage. Toujours verifier `len(fichier) - position_IEND`.")
        break
    break
