import sys, json
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r".")
from cylab2 import CyLab
import wu

cy = CyLab(delay=1.0)
cy.login()
f = "academy{p1kap1ka_p1c018269cc6}"
st, b = cy.req("POST", "/api/submissions/", {"source": "library", "challenge": 171, "flag": f})
try:
    ok = json.loads(b).get("correct")
except Exception:
    ok = None
print("171 gogo ->", ok)
if ok:
    extra = (
        "Binaire **Go statique 32 bits** avec ses symboles : `main.main`, `main.checkPassword`, `main.ambush`, "
        "`main.get_flag`. Etape 1 — `checkPassword` construit deux tableaux de 32 octets sur la pile puis les XOR : "
        "le premier est ecrit en `mov BYTE [esp+8+n]` (ASCII `861836f13e3d627dfa375bdb8389214e`), le second en "
        "**dwords little-endian** (`0x5d47534a`, `0x54034541`, `0x0a5a025d`, `0x0d455753`, `0x555d0005`, "
        "`0x0e011054`, `0x4b575541`, `0x01465045`). Le XOR des deux donne le mot de passe "
        "**`reverseengineericanbarelyforward`**. Piege important : recopier le second tableau a la main conduit a "
        "des erreurs — il faut convertir chaque dword avec `to_bytes(4, 'little')`. Etape 2 — le binaire ne va pas "
        "directement au flag : `main.main` appelle `main.ambush`, qui affiche « This challenge is interrupted by "
        "psociety / What is the unhashed key? ». Le desassemblage d'`ambush` montre un appel a `crypto/md5.Sum` "
        "suivi de la comparaison avec la meme chaine `861836f13e3d627dfa375bdb8389214e` : c'est donc un **MD5 a "
        "casser**. `john --format=raw-md5 --wordlist=rockyou.txt` le resout immediatement en **`goldfish`**. "
        "Verification locale avant d'attaquer le service : `printf 'reverseengineericanbarelyforward\\ngoldfish\\n' "
        "| ./enter_password` affiche `Flag is: academy{LOCAL_TEST_213}`, ce qui valide les deux entrees. `get_flag` "
        "lit alors `flag.txt` (visible dans les chaines du binaire) et imprime le drapeau. Sur le service, le format "
        "de l'adresse dans l'enonce est `host:port` sans `nc`, d'ou une regex adaptee.")
    print("writeup:", wu.write(171, "gogo", "Reverse Engineering",
                               "enter_password (Go statique 32 bits) + service host:port",
                               "XOR de deux tableaux 32 octets + cassage MD5 de la seconde etape (ambush)",
                               f, extra))
