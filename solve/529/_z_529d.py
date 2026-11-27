import sys, requests
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
requests.packages.urllib3.disable_warnings()
B = "http://chatelaine.cylabacademy.net:48796"
cands = ["/download/app.apk", "/download/picobank.apk", "/download/PicoBank.apk", "/download/pico_bank.apk",
         "/download/bank.apk", "/app.apk", "/picobank.apk", "/download/", "/download/app-release.apk",
         "/download/pico-bank.apk", "/download/application.apk", "/download/img/icon.png"]
for c in cands:
    try:
        r = requests.head(B + c, timeout=15, allow_redirects=True)
        print("%-38s %s  %s" % (c, r.status_code, r.headers.get("Content-Length", "-")))
    except Exception as e:
        print("%-38s ERR %s" % (c, type(e).__name__))
