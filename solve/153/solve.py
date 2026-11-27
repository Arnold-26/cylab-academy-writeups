# 153 - Some Assembly Required 3  (Web Exploitation, picoCTF 2021)
# Flag: academy{033f77ed87dcdbcf212e352bde117d44}
# Write-up: ../../../writeups/web-exploitation/153-some-assembly-required-3.md
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


f = "academy{033f77ed87dcdbcf212e352bde117d44}"
try:
    ok = json.loads(b).get("correct")
except Exception:
    ok = None
print("153 Some Assembly Required 3 ->", ok)
if ok:
    extra = ("La page charge un JS obfusque qui `fetch('./qCCYI0ajpD')` (nom aleatoire, donc **par instance**) et "
             "instancie le WebAssembly. Les exports sont revelateurs : `memory, strcmp, check_flag, input, "
             "copy_char, key`. Le flux du site est : pour chaque caractere `copy_char(charCodeAt(i), i)`, puis "
             "`copy_char(0, len)`, puis `check_flag()` qui renvoie 1 si correct. En instanciant le wasm avec "
             "Node (`WebAssembly.instantiate`), on lit directement la memoire : la **valeur attendue est a "
             "l'offset 0x400** (43 octets) et la **transformation de l'entree est ecrite a 0x430** apres "
             "`check_flag`. La transformation depend de la **position** (le meme caractere donne des octets "
             "differents selon l'indice), donc on ne peut pas inverser caractere par caractere isolement : il "
             "faut construire le prefixe de gauche a droite et verifier l'octet transforme a la position "
             "courante. En testant l'alphabet `a-z 0-9 _ { } ! A-Z -` a chaque position et en comparant "
             "`transformed[i]` a `EXPECTED[i]`, on reconstruit le drapeau entier : "
             "`academy{033f77ed87dcdbcf212e352bde117d44}`. Verification prealable utile : `academy{` produit "
             "bien les 8 premiers octets attendus, ce qui confirme que la transformation est deterministe et "
             "que la constante 0x400 est bien la cible.")
    print("writeup:", wu.write(153, "Some Assembly Required 3", "Web Exploitation",
                               "wasm qCCYI0ajpD (942 octets) + JS obfusque",
                               "instanciation Node du wasm, comparaison de la zone transformee 0x430 avec l'attendu 0x400",
                               f, extra))
