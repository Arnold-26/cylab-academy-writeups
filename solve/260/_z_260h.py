import sys, json
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r"D:\ctf-index")
from cylab2 import CyLab
import wu

cy = CyLab(delay=1.2)
cy.login()
f = "academy{Stat1C_c4n4r13s_4R3_b4D_b379746b}"
st, b = cy.req("GET", "/api/challenges/260/")
d = json.loads(b)
print("nom:", d.get("name"), "| deja:", d.get("solved_by_user"))
st, b = cy.req("POST", "/api/submissions/", {"source": "library", "challenge": 260, "flag": f})
ok = json.loads(b).get("correct") if b.startswith("{") else None
print(f"260 buffer overflow 3 -> {ok}")
if ok and not d.get("solved_by_user"):
    wu.write(260, "buffer overflow 3", "Binary Exploitation", "nc xebec.cylabacademy.net <port>",
             "brute force du canary octet par octet + return-to-win", f,
             "Binaire 32 bits non-PIE avec **canary de 4 octets** copie depuis un fichier "
             "(`memcpy(canary, global_canary, 4)`), donc sa valeur est CONSTANTE pour toute l'instance "
             "— c'est ce qui rend le brute force possible. Le programme demande d'abord le nombre "
             "d'octets a ecrire (lu octet par octet jusqu'a newline), puis fait `read(0, buf, count)` "
             "sans borne. Oracle : si le canary est intact, on lit « Ok... Now Where's the Flag? », "
             "sinon « Stack Smashing Detected ». On teste donc les 4 octets un par un : envoyer "
             "64 octets + les octets deja trouves + le candidat, et garder celui qui evite le message "
             "d'erreur (trouve : 42 69 52 64 = « BiRd »). Disposition exacte (issue du desassemblage) : "
             "buf a ebp-0x50, canary a ebp-0x10, x a ebp-0xc, puis padding, puis **[ebp-0x4] = ebx "
             "sauvegarde par le prologue `push ebx`**, saved ebp et enfin l'adresse de retour — d'ou un "
             "offset de **84** (et non 76) depuis buf. Payload final de 88 octets terminé par "
             "p32(0x08049236 = win). Deux pieges rencontres : (1) `read()` fait des lectures "
             "PARTIELLES, donc il faut envoyer le nombre et le payload dans le MEME envoi pour que les "
             "88 octets soient deja en tampon quand `read` s'execute ; (2) oublier le `push ebx` "
             "decale l'adresse de retour et l'exploit affiche seulement « Ok... » sans le flag.")
