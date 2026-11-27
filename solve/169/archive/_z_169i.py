import sys, re, requests, urllib3, hashlib
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
urllib3.disable_warnings()
B = r"/tmp/cylab_eps"
# 1) verifier si l'app propose invite.pdf
for base in ("http://xebec.cylabacademy.net:32679/",):
    try:
        r = requests.get(base, timeout=20)
        print("page:", r.status_code, len(r.text))
        for m in re.finditer(r"href=['\"]([^'\"]*invite[^'\"]*)['\"]", r.text):
            print("  lien invite:", m.group(1))
    except Exception as e:
        print("page ERR", type(e).__name__)
# 2) telecharger les shattered
urls = {
    "shattered-1.pdf": "https://shattered.io/static/shattered-1.pdf",
    "shattered-2.pdf": "https://shattered.io/static/shattered-2.pdf",
}
for n, u in urls.items():
    try:
        r = requests.get(u, timeout=60, verify=False)
        if r.status_code == 200:
            open(B + "\\169_" + n, "wb").write(r.content)
            print(n, len(r.content), hashlib.sha1(r.content).hexdigest()[:16])
        else:
            print(n, r.status_code)
    except Exception as e:
        print(n, "ERR", type(e).__name__)
# 3) invite depuis le repo HHousen
u = "https://raw.githubusercontent.com/HHousen/PicoCTF-2021/master/Cryptography/It%20is%20my%20Birthday%202/invite.pdf"
try:
    r = requests.get(u, timeout=60, verify=False)
    print("invite:", r.status_code, len(r.content), r.content[:4])
    if r.status_code == 200:
        open(B + "\\169_invite.pdf", "wb").write(r.content)
except Exception as e:
    print("invite ERR", type(e).__name__)
