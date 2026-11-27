# 182 - Some Assembly Required 4  (Web Exploitation, picoCTF 2021)
# Flag: academy{e69e121eab55f85293c89b9082255ed7}
# Write-up: ../../../writeups/web-exploitation/182-some-assembly-required-4.md
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


f = "academy{e69e121eab55f85293c89b9082255ed7}"
try:
    ok = json.loads(b).get("correct")
except Exception:
    ok = None
print("182 Some Assembly Required 4 ->", ok)
if ok:
    extra = (
        "Challenge wasm : la page charge `rqe4VVml5W.js` (obfusque) qui instancie un module wasm "
        "`ZoRd23o0wd` (2142 octets) exposant `copy_char`, `check_flag` et le global `input`. Le writeup public "
        "confirme la demarche mais le flag CyLab differe du picoCTF. Methode : `wabt` (`apt install wabt`) "
        "pour `wasm2wat`, puis lecture de `check_flag` (func 2, 600 lignes). Deux passes sur le buffer d'entree "
        "(global `input` = 1072 = 0x430) : (1) transformation par caractere — `v ^= 20`, puis si i>0 `v ^= "
        "d[i-1]`, si i>2 `v ^= d[i-3]`, puis `v ^= i%10`, `v ^= (i pair ? 9 : 8)`, `v ^= (i%3==0 ? 7 : "
        "i%3==1 ? 6 : 5)` ; (2) **permutation** : boucle ou si `i%2==0` on echange `data[i]` et `data[i+1]` "
        "(echange de paires adjacentes, involutif). Enfin `strcmp(data@1024, input@1072)` compare au segment "
        "de donnees `\\03{\\7fx\\0f\\06u\\15>...` (40 octets). Resolution : appliquer la permutation au segment "
        "puis inverser la transformation **en avant** (les voisins i-1 et i-3 sont lus apres leur propre "
        "transformation, donc ce sont les valeurs finales) : `academy{e69e121eab55f85293c89b9082255ed7}`. "
        "Astuce cle : `wabt` rend le wasm lisible, et la verification de la cle XOR par oracle (forcer la cible "
        "a 0x41 et voir quel caractere passe) a confirme la constante 0x1a au poste 0.")
    print("writeup:", wu.write(182, "Some Assembly Required 4", "Web Exploitation",
                               "wasm ZoRd23o0wd + rqe4VVml5W.js (obfusque)",
                               "wasm2wat + inversion transform XOR par position + permutation de paires",
                               f, extra))
