# 23 - droids3  (Reverse Engineering, picoCTF 2019)
# Flag: academy{tis.but.a.scratch}
# Write-up: ../../../writeups/reverse-engineering/23-droids3.md
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


f = "academy{tis.but.a.scratch}"
already = json.loads(b).get("solved_by_user")
ok = json.loads(b).get("correct") if b.startswith("{") else None
print(f"23 (deja={already}) -> {ok}")
if ok and not already:
    wu.write(23, "droids3", "Reverse Engineering", "", "deobfuscation native : XOR répétitif dans sumac()", f,
             "APK decompile avec apktool ; `FlagstaffHill.cilantro(String)` est natif et renvoie "
             "`sumac()` (le flag) si `dill(input)` est vrai. `sumac` fait "
             "`unscramble(str2, 26, strdup(str1), strlen(str1))` ou `unscramble` est un **XOR "
             "repetitif** : `out[i] ^= key[i % keylen]`. Cle a 0x1a0d = `againmissing`, donnees a "
             "0x1a85 (26 octets) -> `academy{tis.but.a.scratch}`. Le mot de passe attendu cote app est "
             "`don't wanna`. La lib est compilee pour Bionic (exige la version symbole `LIBC`), donc "
             "le `dlopen` sous glibc echoue : il faut decoder statiquement (neutraliser "
             "`.gnu.version`/`vn_cnt` ne suffit pas).")
