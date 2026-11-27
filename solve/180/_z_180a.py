import sys, requests, re
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
requests.packages.urllib3.disable_warnings()
B = "http://xebec.cylabacademy.net:46300"
for path in ("/robots.txt", "/index.phps", "/index.php", "/authentication.php.bak", "/cookie.php",
             "/login.phps", "/admin.phps"):
    try:
        r = requests.get(B + path, timeout=15, verify=False, allow_redirects=False)
        print(f"\n=== {path} -> {r.status_code} ({len(r.content)} o) ===")
        print(r.text[:500])
    except Exception as e:
        print(path, "ERR", type(e).__name__)
