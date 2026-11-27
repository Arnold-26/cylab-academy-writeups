import sys, json
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r"D:\ctf-index")
from cylab2 import CyLab
import wu

cy = CyLab(delay=1.2)
cy.login()
for f in ("7e5bf24636955536f27a26c1e423f18a", "e5bf24636955536f27a26c1e423f18a"):
    st, b = cy.req("POST", "/api/submissions/", {"source": "library", "challenge": 143, "flag": f})
    try:
        ok = json.loads(b).get("correct")
    except Exception:
        ok = None
    print("143 %-34s -> %s" % (f, ok))
    if ok:
        wu.write(143, "Binary Gauntlet 2", "Binary Exploitation",
                 "nc chatelaine.cylabacademy.net <port>",
                 "format string pour fuiter la pile + shellcode sur pile RWE (pas de %p fourni)", f,
                 "Meme binaire que Gauntlet 1 mais **la fuite d'adresse a ete retiree** : le programme "
                 "n'affiche plus `%p`, donc l'ASLR de la pile empeche un saut direct vers la shellcode. "
                 "La parade est que le premier `fgets` est imprime par `printf(heap_buf)` — c'est une "
                 "**format string** exploitable : envoyer 40 `%p` fuit toute la pile, dont plusieurs "
                 "adresses `0x7fff...`. La premiere valeur de type pile (index 0 parmi les valeurs "
                 "filtrees) est a un **delta constant de 0x198** au-dessus du buffer (`rbp-0x70`), delta "
                 "mesure localement sous gdb (`buf=0x7fffffffde40` vs fuite `0x7fffffffdfd8`). Exploit : "
                 "`%p.%p....` puis, sur la deuxieme entree, "
                 "`shellcode(23o) + '\\x90'*(0x70-23) + 'B'*8 + p64(fuite - 0x198)`. La pile reste **RWE** "
                 "(`GNU_STACK RWE`) donc la shellcode s'execute. `cat flag.txt` renvoie un flag sans "
                 "wrapper `academy{}`. Reussi au premier essai avec idx=0 et delta=0x198.")
        break
