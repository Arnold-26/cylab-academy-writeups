import sys, re, requests, random, string
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
requests.packages.urllib3.disable_warnings()
A = "http://xebec.cylabacademy.net:47074"
U = "hx" + "".join(random.choices(string.digits, k=4))
P = "Passw0rd!"
s = requests.Session()
s.headers.update({"User-Agent": "Mozilla/5.0"})
r = s.get(A + "/register.php", timeout=20)
print("=== register form ===")
for f in re.findall(r'<(?:input|form)[^>]*>', r.text):
    print("  ", f[:140])
r = s.post(A + "/register.php", data={"username": U, "password": P, "confirm_password": P,
                                      "confirm": P, "email": U + "@t.com"}, timeout=20,
           allow_redirects=True)
print("\nregister ->", r.status_code, len(r.text))
m = re.search(r"(?i)(success[^<]{0,80}|error[^<]{0,80}|invalid[^<]{0,80}|exist[^<]{0,80})", r.text)
print("msg:", m.group(1)[:100] if m else "(aucun)")
r = s.post(A + "/login.php", data={"username": U, "password": P}, timeout=20, allow_redirects=True)
print("\nlogin ->", r.status_code, len(r.text), "url:", r.url)
body = r.text
print(body[:1200])
f = re.search(r"(?:academy|picoCTF)\{[^}]*\}", body)
if f:
    print("FLAG:", f.group(0))
print("\nUSER:", U, P)
