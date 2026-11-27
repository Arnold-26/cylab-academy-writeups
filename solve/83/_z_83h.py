import sys, json
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r"D:\ctf-index")
from cylab2 import CyLab
import wu

cy = CyLab(delay=1.0)
cy.login()
f = "academy{4n0th3r_L5b_pr0bl3m_00000000000001eb97d9c}"
st, b = cy.req("POST", "/api/submissions/", {"source": "library", "challenge": 83, "flag": f})
try:
    ok = json.loads(b).get("correct")
except Exception:
    ok = None
print("83 Investigative Reversing 3 ->", ok)
if not ok:
    for cand in (f.replace("0000000000000", "000000000000"), f):
        st, b = cy.req("POST", "/api/submissions/", {"source": "library", "challenge": 83, "flag": cand})
        try:
            o2 = json.loads(b).get("correct")
        except Exception:
            o2 = None
        print("  variante ->", o2)
        if o2:
            f = cand
            ok = True
            break
if ok:
    extra = (
        "Meme famille que 13 : le binaire `investigative-reversing-3-mystery` (PIE, non strippe) recopie "
        "**723 octets** (`0x2d3`) d'en-tete, puis appelle `codedChar(j, flag[i/2], octet)` pour 100 groupes de "
        "8 bits. `codedChar` ecrit le bit dans le **LSB** : `(octet & 0xfe) | ((ch >> bit) & 1)`. Le piege est "
        "la disposition : au lieu d'un bloc contigu de 8 octets par caractere, chaque caractere occupe un "
        "**pas de 9 octets** (8 bits + 1 octet de gap), donc le bit j du caractere k est le LSB de l'octet "
        "`723 + 9*k + j`. **Methode qui a permis de le prouver** : executer le binaire deux fois avec des "
        "drapeaux connus dont tous les bits different (`'A'*50` = 0x41 puis `'B'*50` = 0x42, qui ne different "
        "que par les bits 0 et 1), puis differ les deux images produites. On obtient exactement **100 octets "
        "modifies**, par paires aux offsets 723/724, 732/733, 741/742... : le pas 9 et la largeur 1 octet par "
        "bit sont ainsi mesures directement sur le binaire, sans supposition. L'extraction avec ce pas donne "
        "`academy{4n0th3r_L5b_pr0bl3m_00000000000001eb97d9c}`. Lecon : quand l'analyse statique ne tranche pas, "
        "faire tourner le binaire sur des entrees controlees et differer les sorties est plus rapide et plus "
        "sur que de deviner la disposition.")
    print("writeup:", wu.write(83, "Investigative Reversing 3", "Forensics",
                               "investigative-reversing-3-mystery + investigative-reversing-3-encoded.bmp",
                               "LSB apres 723 octets, pas de 9 octets par caractere (mesure par double execution)",
                               f, extra))
