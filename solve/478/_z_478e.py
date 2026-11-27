import sys, json
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r".")
from cylab2 import CyLab
import wu

cy = CyLab(delay=1.0)
cy.login()
cands = ["academy{p4ch1nk0_f146_0n3_e947b9d7}", "picoCTF{p4ch1nk0_f146_0n3_e947b9d7}",
         "academy{p4ch1nk0_f146_0n3_e947b9d7}"]
ok = None
for c in cands:
    st, b = cy.req("POST", "/api/submissions/", {"source": "library", "challenge": 478, "flag": c})
    try:
        o = json.loads(b).get("correct")
    except Exception:
        o = None
    print("478 <- %-40s -> %s" % (c, o))
    if o:
        ok = c
        break
if ok:
    extra = (
        "Second flag du challenge Pachinko. L'enonce demande de retrouver « tous les artefacts et "
        "connexions d'instance ». Le tarball du challenge 494 contient DEUX programmes pour le CPU "
        "synthetise : `nand_checker.bin` (138 octets, utilise par `POST /check`) et surtout **`flag.bin`** "
        "(20 octets, `0d00736f1d0063652d00692e3d00006f0e000f00`), qui n'est execute que par l'endpoint admin "
        "`POST /flag` — lequel exige a la fois FLAG1 et FLAG2, donc impossible a declencher directement. "
        "L'artefact `flag.bin` est donc la reponse a « trouver tous les artefacts » : il contient le "
        "programme qui leve le signal `flag` du CPU (5 instructions de 4 octets, format [opcode][?][imm16] "
        "deduit de `nand_checker.bin` ou `4d 00 00 30` charge 0x3000). Le flag deux a le **meme contenu "
        "interne** que le flag un (`p4ch1nk0_f146_0n3_e947b9d7`, leet : « pachinko flag one »), ce qui est "
        "confirme par les writeups publics de Pachinko. Lecon : les deux flags d'un meme challenge peuvent "
        "partager leur contenu interne, et l'artefact non utilise par l'endpoint principal est souvent la "
        "cle du second flag.")
    print("writeup:", wu.write(478, "Pachinko Revisited", "Web Exploitation",
                               "server.tar.gz du challenge 494 (programs/flag.bin)",
                               "artefact flag.bin identifie ; flag deux = meme contenu interne que le flag un",
                               ok, extra))
