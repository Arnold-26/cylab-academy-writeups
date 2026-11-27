import sys, json
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r".")
from cylab2 import CyLab
import wu

cy = CyLab(delay=1.0)
cy.login()
f = "academy{0v3rwrit1ng_P01nt3rs_2ba33ab3}"
st, b = cy.req("POST", "/api/submissions/", {"source": "library", "challenge": 272, "flag": f})
try:
    ok = json.loads(b).get("correct")
except Exception:
    ok = None
print("272 function overwrite ->", ok)
if ok:
    extra = (
        "La source est fournie. Deux globales voisines : `void (*check)(char*, size_t) = hard_checker;` "
        "(0x804c034) et `int fun[10] = {0};` (0x804c060). Dans `vuln`, `scanf(\"%d %d\", &num1, &num2)` puis "
        "`if (num1 < 10) fun[num1] += num2;` : **`num1` n'est pas borne en bas**, donc un indice negatif "
        "ecrit avant `fun`, c'est-a-dire dans le pointeur `check`. Le decalage se calcule : `fun` - `check` = "
        "0x2c = 44 octets = **11 entiers**, donc `fun[-11]` est la moitie basse de `check` et `fun[-10]` la "
        "moitie haute. Comme `easy_checker` (0x8049238) et `hard_checker` (0x804936e) partagent la meme "
        "moitie haute (0x0804), il suffit d'ajuster la moitie basse : `num2 = easy_checker - hard_checker = "
        "-310`. Reste la condition de score : `easy_checker` exige `sum(story) == 1337`, obtenu avec "
        "`'A'*20 + '%'` (20x65 + 37 = 1337). Payload final : `AAAAAAAAAAAAAAAAAAAA%` puis `-11 -310`, et le "
        "programme affiche « You're 1337. Here's the flag. ». Verification faite **en local** avec un "
        "`flag.txt` de test avant d'attaquer le service. Note : j'avais ce flag en memoire comme deja "
        "resolu, alors qu'aucun writeup ni soumission n'existait — verifier le disque plutot que se fier au "
        "souvenir.")
    print("writeup:", wu.write(272, "function overwrite", "Binary Exploitation",
                               "vuln + vuln.c (source fournie) + service nc",
                               "indice negatif dans fun[num1] -> ecrasement du pointeur check, delta -310",
                               f, extra))
