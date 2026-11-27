import sys, requests, urllib3, re
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
urllib3.disable_warnings()
BASE = "http://chatelaine.cylabacademy.net:19299/"
s = requests.Session()
s.post(BASE + "register.php", data={"user": "fuzzer9", "pass": "pass9"}, timeout=15)
r = s.post(BASE + "index.php", data={"username": "fuzzer9", "password": "pass9"}, timeout=15)
print("=== formulaires et champs apres login ===")
for m in re.finditer(r"<form[^>]*>|<input[^>]*>|<a [^>]*href=\"[^\"]*\"", r.text):
    print("  ", m.group(0)[:150])
print("\n=== extrait du corps ===")
txt = re.sub(r"<[^>]+>", " ", r.text)
print(re.sub(r"\s+", " ", txt)[:600])
