# 489 - hash-only-2  (Binary Exploitation, picoCTF 2025)
# Flag: academy{Co-@utH0r_Of_Sy5tem_b!n@riEs_bf204e06}
# Write-up: ../../../writeups/binary-exploitation/489-hash-only-2.md
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


f = "academy{Co-@utH0r_Of_Sy5tem_b!n@riEs_bf204e06}"
already = json.loads(b).get("solved_by_user")
ok = json.loads(b).get("correct") if b.startswith("{") else None
print(f"489 hash-only-2 (deja={already}) -> {ok}")
if ok and not already:
    wu.write(489, "hash-only-2", "Binary Exploitation", "ssh ctf-player@chatelaine.cylabacademy.net -p <port>",
             "contournement de rbash par invocation explicite de bash + PATH hijack", f,
             "Meme cible que hash-only-1 (un `flaghasher` setuid root qui appelle `md5sum` sur "
             "/root/flag.txt), mais la session SSH est cette fois un **rbash** (shell restreint) : `PATH` "
             "est en lecture seule, les redirections sont refusees et les `/` sont interdits dans les noms "
             "de commandes, ce qui bloque le detournement direct. Le contournement est simple : `rbash` "
             "n'applique ses restrictions qu'au shell invoque sous ce nom. En passant une commande "
             "explicite `bash -c \"...\"` a ssh, on obtient un bash **non restreint** (uid=1001, PATH "
             "modifiable). On recree alors le faux `md5sum` dans $HOME, on le met en tete de PATH et on "
             "lance `flaghasher` : il s'execute en euid root (id renvoie uid=0) et affiche le flag. "
             "`flaghasher` seul se contente de renvoyer l'empreinte MD5 "
             "7e43bc81db2ecf3d242aa1574a92f8c3.")
