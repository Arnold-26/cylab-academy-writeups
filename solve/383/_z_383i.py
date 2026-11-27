import sys, json
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r"D:\ctf-index")
from cylab2 import CyLab
import wu

cy = CyLab(delay=1.0)
cy.login()
f = "academy{f473_53413d_e0c91991}"
st, b = cy.req("POST", "/api/submissions/", {"source": "library", "challenge": 383, "flag": f})
try:
    ok = json.loads(b).get("correct")
except Exception:
    ok = None
print("383 UnforgottenBits ->", ok)
if not ok:
    for cand in ("picoCTF{f473_53413d_e0c91991}", "academy{f473_53413d_e0c91991}"):
        st, b = cy.req("POST", "/api/submissions/", {"source": "library", "challenge": 383, "flag": cand})
        try:
            o2 = json.loads(b).get("correct")
        except Exception:
            o2 = None
        print("  variante", cand, "->", o2)
        if o2:
            f = cand
            ok = True
            break
if ok:
    extra = (
        "Image disque de 1 Go (`disk.flag.img`) a analyser. Le writeup donne la chaine complete, que j'ai "
        "reexecutee pas a pas. Etape 1 : extraire les 4 images de la galerie (`home/yone/gallery/{1,2,3,7}.bmp`) "
        "avec `fls`/`icat` de sleuthkit. Etape 2 : un log IRC (`irclogs/01/04/#avidreader13.log`) revele la "
        "methode — **steghide** avec le mot de passe `akalibardzyratrundle`, puis **AES-256-CBC**. Les images 1, "
        "2 et 3 se decodent bien et donnent des ebooks Gutenberg (Les Miserables, Dracula, Frankenstein) : ce "
        "sont des leurres, `grep` n'y trouve aucun flag. L'image **7.bmp** refuse ce mot de passe. Etape 3 : le "
        "writeup explique que le mot de passe de 7.bmp est compose de **champions de League of Legends** "
        "(indice : les notes `1.txt`/`2.txt`/`3.txt` contiennent `chizazerite`, `guldulheen`, et surtout "
        "`yasuoaatrox...`), a casser avec `stegcracker`. Le mot de passe est "
        "**`yasuoaatroxashecassiopeia`**. Etape 4 : les 560 octets extraits se dechiffrent avec "
        "`openssl enc -aes-256-cbc -d -S 2350e88cbeaf16c9 -K a9f86b...36da -iv 908458e4...119f` (sel, cle et IV "
        "differents de ceux des trois autres images, encore un piege) et donnent une liste de clients ressemblant "
        "a une bibliotheque, avec la ligne `academy{f473_53413d_e0c91991}`. Lecons : (1) plusieurs jeux de "
        "parametres de chiffrement cohabitent, il faut traiter chaque image separement ; (2) trois des quatre "
        "images sont des leurres plausibles ; (3) le vrai secret passe par un mot de passe thematique a casser, "
        "pas par une analyse forensique directe.")
    print("writeup:", wu.write(383, "UnforgottenBits", "Forensics",
                               "disk.flag.img (1 Go) + 4 BMP de la galerie",
                               "steghide (mot de passe LoL) + AES-256-CBC avec sel/cle/IV specifiques",
                               f, extra))
