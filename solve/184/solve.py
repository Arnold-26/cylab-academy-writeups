# 184 - filtered-shellcode  (Binary Exploitation, picoCTF 2021)
# Flag: academy{th4t_w4s_fun_0f1be5fd2eb499cd}
# Write-up: ../../../writeups/binary-exploitation/184-filtered-shellcode.md
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


f = "academy{th4t_w4s_fun_0f1be5fd2eb499cd}"
try:
    ok = json.loads(b).get("correct")
except Exception:
    ok = None
print("184 filtered-shellcode ->", ok)
if ok:
    wu.write(184, "filtered-shellcode", "Binary Exploitation", "nc xebec.cylabacademy.net <port>",
             "shellcode 32 bits en instructions de 2 octets, filtre i%4 insere des NOP", f,
             "Binaire **32 bits non-PIE**. `main` lit jusqu'a 0x3e7 octets avec `fgetc`, ajoute un NOP "
             "si la longueur est impaire, puis `execute(buf,len)`. `execute` alloue `2*len` octets sur "
             "la pile, recopie l'entree avec un **filtre** : pour chaque index i, si `i % 4 <= 1` "
             "l'octet d'entree est copie, sinon la sortie recoit **0x90 (NOP)** ; un 0xC3 (ret) est "
             "ajoute a la fin et le buffer est appele (`call eax`) — la pile est executable. Deux "
             "decouvertes decisives : (1) le compteur de lecture est **separe** de l'index d'ecriture "
             "et n'incremente que sur les copies, donc l'entree est consommee de facon **compacte** : "
             "il ne faut PAS entrelacer de remplissage (mon premier essai inserait des 'AA' qui se "
             "retrouvaient executes) ; (2) il faut donc une shellcode dont **chaque instruction tient "
             "sur exactement 2 octets**, puisque le filtre insere `90 90` toutes les 2 instructions. "
             "Construction : `mov edi,esp` puis, pour chaque caractere de `//bin/sh`, "
             "`mov al,imm8` (b0 xx) suivi de `stosb` (aa 90) — surtout PAS `push imm8`, qui pousse "
             "**4 octets** et casse la contiguite de la chaine. On termine par `xor eax,eax` + `stosb` "
             "(terminateur), `mov ebx,esp`, `push eax` / `push ebx` / `mov ecx,esp` pour argv, "
             "`xor edx,edx` (envp — sans quoi execve echoue), `mov al,11` et `int 0x80`. Verifie en "
             "local sous gdb (`executing new program: /usr/bin/dash`) puis en distant.")
