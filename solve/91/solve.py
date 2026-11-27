# 91 - Nothing Up My Sleeve  (General Skills, picoCTF 2020 Mini-Competition)
# Flag: academy{c0ngr4ts_0n_y0ur_s4n1ty}
# Write-up: ../../../writeups/general-skills/91-nothing-up-my-sleeve.md
# This is the script that produced the flag; historical variants are in archive/.
#
import sys, json, re, requests, subprocess, pathlib
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
import wu

# Service : demarrer l'instance depuis la plateforme du challenge, puis passer
# l'hote et le port (ou l'URL) en argument de ce script.
_A = sys.argv[1:]
HOST = _A[0] if len(_A) > 0 else ""
PORT = int(_A[1]) if len(_A) > 1 else 0
url = _A[0] if _A else ""


requests.packages.urllib3.disable_warnings()
FLAG = re.compile(r"(?:academy|picoCTF|PICOCTF)\{[^}]*\}")
url = "https://challenge-files.cylabacademy.net/library/7a2d73afcf61879089df15c526cb7c833947dd7fa6aeb074eeacf4eb6a5ce096/flag.txt"
r = requests.get(url, timeout=60, verify=False)
print("contenu:", r.text[:500])
m = FLAG.search(r.text)
if m:
    f = m.group(0)
    print("FLAG:", f)
    already = json.loads(b).get("solved_by_user")
    ok = json.loads(b).get("correct") if b.startswith("{") else None
    print("91 ->", ok)
    if ok and not already:
        wu.write(91, "Nothing Up My Sleeve", "General Skills", "", "telechargement direct", f,
                 "Le fichier `flag.txt` est servi en clair sur le CDN : il suffit de le telecharger.")
