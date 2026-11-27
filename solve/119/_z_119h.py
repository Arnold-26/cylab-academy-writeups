import sys, json
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r".")
from cylab2 import CyLab
import wu

cy = CyLab(delay=1.2)
cy.login()
f = "academy{2018highw@y_2_pow3r$hel!}"
st, b = cy.req("GET", "/api/challenges/119/")
already = json.loads(b).get("solved_by_user")
st, b = cy.req("POST", "/api/submissions/", {"source": "library", "challenge": 119, "flag": f})
ok = json.loads(b).get("correct") if b.startswith("{") else None
print(f"119 Powershelly (deja={already}) -> {ok}")
if ok and not already:
    wu.write(119, "Powershelly", "Reverse Engineering", "", "inversion d'une permutation + chaine XOR PowerShell", f,
             "Le script PowerShell lit `input.txt` (9245 octets = **5 lignes** de 264 champs de 6 bits, ce qui "
             "colle exactement a `$numLength = 264*30 + 265*5`), empile les 5 lignes par colonne "
             "(`$blocks[$j]` = les 5 morceaux de 6 bits de la colonne j, soit 30 bits), puis : "
             "`Scramble(bloc, seed)` construit 30 emplacements a `\"10\"`, et pour i=0..29 ecrit `\"11\"` "
             "ou `\"00\"` au premier emplacement libre en partant de `(i*seed) % 30` (une **permutation**, "
             "donc inversible) ; la sortie enchainee est `result_i = fun_i XOR result_{i-1} XOR randoms_i`. "
             "On recupere donc `fun_i = result_i XOR result_{i-1} XOR randoms_i` avec "
             "`randoms[i] = ((i+1)*327 % 681 + 344) % 313`, on verifie que chaque fun (60 bits) ne contient "
             "que des paires 11/00 (0 non conforme -> validation), puis on inverse la permutation avec "
             "`seeds[i] = ((i+1)*127) % 500`. Les 30 lignes resultantes se lisent en ASCII : "
             "`academy{2018highw@y_2_pow3r$hel!}` (les lignes en 0x9e.. sont la meme chaine XOR 0xff).")
