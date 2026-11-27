import sys, json
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r"D:\ctf-index")
from cylab2 import CyLab
import wu

cy = CyLab(delay=1.2)
cy.login()
f = "academy{r0p_y0u_l1k3_4_hurr1c4n3_99c099b7facb4875}"
st, b = cy.req("GET", "/api/challenges/90/")
already = json.loads(b).get("solved_by_user")
st, b = cy.req("POST", "/api/submissions/", {"source": "library", "challenge": 90, "flag": f})
ok = json.loads(b).get("correct") if b.startswith("{") else None
print(f"90 Guessing Game 1 (deja={already}) -> {ok}")
if ok and not already:
    wu.write(90, "Guessing Game 1", "Binary Exploitation", "nc xebec.cylabacademy.net <port>",
             "rand() sans srand + ROP syscall execve sur binaire statique", f,
             "Le binaire **statique** `guessing-game-1-vuln` (non-PIE) utilise `rand() % 100 + 1` **sans "
             "`srand`** : la graine par defaut est 1, donc `rand()` vaut 1804289383 et la reponse est "
             "toujours **84**. `win()` a un buffer de 112 octets a `rbp-0x70` et fait "
             "`fgets(winner, 360, stdin)` : debordement de 248 octets, et surtout **aucun canari** dans "
             "cette fonction (contrairement a ce que laissait croire la presence de `__stack_chk_fail` "
             "dans le binaire, qui ne protege que `main`). Le binaire etant statique, pas de ret2libc : on "
             "construit un ROP en syscalls directs. Gadgets trouves par scan d'octets (ROPgadget ne "
             "renvoie rien sur ce binaire) : `pop rdi; ret` 0x40206f, `pop rsi; ret` 0x40a0de, "
             "`pop rdx; pop rbx; ret` 0x486bbb, `pop rax; ret` 0x4518e7, `syscall; ret` 0x41b406. Chaine : "
             "`read(0, bss=0x4c9360, 16)` puis `execve(bss, 0, 0)` (rax=59). On envoie ensuite `/bin/sh` "
             "pour que le read l'ecrive en .bss, et le shell tombe. Offset vers le retour : 112 + 8 = 120.")
