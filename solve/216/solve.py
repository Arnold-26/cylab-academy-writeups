# 216 - clutter-overflow  (Binary Exploitation, picoMini by redpwn)
# Flag: picoCTF{c0ntr0ll3d_clutt3r_1n_my_buff3r}
# Write-up: ../../../writeups/binary-exploitation/216-clutter-overflow.md
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


f = "picoCTF{c0ntr0ll3d_clutt3r_1n_my_buff3r}"
already = json.loads(b).get("solved_by_user")
ok = json.loads(b).get("correct") if b.startswith("{") else None
print(f"216 (deja={already}) -> {ok}")
if ok and not already:
    wu.write(216, "clutter-overflow", "Binary Exploitation", "", "buffer overflow -> variable = 0xdeadbeef", f,
             "Le service lit notre entree dans un buffer de 256 octets suivi d'une variable `code` "
             "(8 octets) qu'il compare a `0xdeadbeef`. L'offset est **264** (determine en envoyant "
             "`A`*n + `B`*8 et en lisant la valeur affichee : elle passe a 0x4242424242424242 a n=264). "
             "On envoie donc 264 octets + `p64(0xdeadbeef)`.")
