import sys, json
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r"D:\ctf-index")
from cylab2 import CyLab
import wu

cy = CyLab(delay=1.2)
cy.login()
f = "8fc275985377ab6a0d9aa40eeaa7dd29"
st, b = cy.req("POST", "/api/submissions/", {"source": "library", "challenge": 114, "flag": f})
try:
    ok = json.loads(b).get("correct")
except Exception:
    ok = None
print("114 Play Nice ->", ok)
if ok:
    wu.write(114, "Play Nice", "Cryptography", "nc chatelaine.cylabacademy.net <port>",
             "chiffre de Playfair 6x6 : dechiffrement avec la cle publiee en clair", f,
             "Le service imprime en clair l'**alphabet** (36 caracteres, carre 6x6) qui sert de cle, "
             "puis le **message chiffre**, et demande le clair. Le code `playfair.py` fourni montre "
             "l'algorithme exact : carre 6x6 construit dans l'ordre de l'alphabet, et `encrypt_pair` "
             "decale de +1 en ligne si meme ligne, de +1 en colonne si meme colonne, sinon echange les "
             "colonnes. Le dechiffrement est donc le meme algorithme avec **-1** a la place de +1 "
             "(et l'echange de colonnes inchange). Detail utile : si la longueur du message est impaire, "
             "le chiffrement ajoute `{` en fin de texte — il faut donc retirer ce caractere du clair "
             "reconstruit avant de repondre. Le service repond « Congratulations! Here's the flag: ... » "
             "avec un flag **sans format standard** (une simple chaine hexadecimale), conformement a "
             "l'enonce.")
