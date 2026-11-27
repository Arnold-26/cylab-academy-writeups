# 29 - Java Script Kiddie  (Web Exploitation, picoCTF 2019)
# Flag: academy{899f655514ccb5662bac39d1f53ec6bd}
# Write-up: ../../../writeups/web-exploitation/29-java-script-kiddie.md
# This is the script that produced the flag; historical variants are in archive/.
#
import sys, json, re, time, requests, io

# Service : demarrer l'instance depuis la plateforme du challenge, puis passer
# l'hote et le port (ou l'URL) en argument de ce script.
_A = sys.argv[1:]
HOST = _A[0] if len(_A) > 0 else ""
PORT = int(_A[1]) if len(_A) > 1 else 0
url = _A[0] if _A else ""

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

requests.packages.urllib3.disable_warnings()
FLAG = re.compile(r"(?:academy|picoCTF|PICOCTF)\{[^}]*\}")
url = None
for _ in range(15):
    time.sleep(2)
    d = json.loads(b) if b.startswith("{") else {}
    if d.get("status") == "RUNNING":
        desc = d.get("description") or ""
        cands = [c for c in re.findall(r"https?://[A-Za-z0-9.\-]+\.cylabacademy\.net(?::\d+)?", desc) if "challenge-files" not in c]
        if cands:
            url = cands[0]
            break
print("29:", url)
if url:
    base = url.rstrip("/")
    rb = requests.get(base + "/bytes", timeout=15, verify=False)
    bytes_ = [int(x) for x in rb.text.split()]
    N = len(bytes_)
    LEN = 16
    print("N:", N)
    expected = bytes.fromhex("89504e470d0a1a0a0000000d49484452")
    base_key = [None] * LEN
    opts = {}
    for i in range(LEN):
        cands = []
        for s in range(10):
            idx = ((s * LEN) % N) + i
            if idx < N and bytes_[idx] == expected[i]:
                cands.append(s)
        opts[i] = cands
        if len(cands) == 1:
            base_key[i] = cands[0]
    print("options:", opts)
    import itertools
    amb = [i for i in range(LEN) if base_key[i] is None]
    print("ambigus:", amb)
    from PIL import Image
    if not amb:
        combos = [tuple(base_key)]
    else:
        combos = itertools.product(*[opts[i] for i in amb])
    for combo in combos:
        key = base_key[:]
        for i, v in zip(amb, combo):
            key[i] = v
        result = [0] * N
        for i in range(LEN):
            s = key[i]
            for j in range(N // LEN):
                result[(j * LEN) + i] = bytes_[(((j + s) * LEN) % N) + i]
        data = bytes(result)
        try:
            im = Image.open(io.BytesIO(data))
            im.load()
            print("VALID key:", "".join(str(k) for k in key), "size:", im.size)
            out = r"/tmp/cylab_hid\29_valid.png"
            open(out, "wb").write(data)
            print("ecrit:", out)
            break
        except Exception:
            continue
