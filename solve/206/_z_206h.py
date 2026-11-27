import sys, subprocess, random
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# test de l'inversion
N = 20
orig = list(range(N))
rnd = random.Random(12345)
x = orig[:]
js = []
for i in range(N - 1, 0, -1):
    j = rnd.randrange(i + 1)
    js.append(j)
    x[i], x[j] = x[j], x[i]
y = x[:]
for idx in range(len(js) - 1, -1, -1):
    i = N - 1 - idx
    j = js[idx]
    y[i], y[j] = y[j], y[i]
print("test inversion OK:", y == orig)

PCAP = "/mnt/c/Users/arnol/AppData/Local/Temp/cylab_206/capture.pcapng"
r = subprocess.run(["tshark", "-r", PCAP, "-Y", "udp", "-T", "fields",
                    "-e", "frame.time_epoch", "-e", "udp.srcport", "-e", "udp.payload"],
                   capture_output=True, text=True, timeout=900)
rows = []
for line in (r.stdout or "").splitlines():
    parts = line.split("\t")
    if len(parts) < 3:
        continue
    try:
        ts = float(parts[0]); sport = int(parts[1]); payload = bytes.fromhex(parts[2].strip())
    except Exception:
        continue
    if len(payload) == 1:
        rows.append((ts, sport, payload[0]))
uniq = []
prev = None
for row in rows:
    key = (row[1], row[2])
    if key == prev:
        continue
    uniq.append(row)
    prev = key
N = len(uniq)
print("paquets uniques:", N)
target = [u[1] for u in uniq[:6]]
seed_found = None
for seed in range(int(uniq[0][0]) - 7200, int(uniq[0][0]) + 120):
    rnd = random.Random(seed)
    for i in range(N - 1, 0, -1):
        rnd.randrange(i + 1)
    ok = True
    for k in range(6):
        if rnd.randrange(65536) != target[k]:
            ok = False
            break
        rnd.randrange(256)
    if ok:
        seed_found = seed
        break
print("seed:", seed_found)
if seed_found:
    rnd = random.Random(seed_found)
    js = []
    for i in range(N - 1, 0, -1):
        js.append(rnd.randrange(i + 1))
    data = []
    for i in range(N):
        rnd.randrange(65536)
        rb = rnd.randrange(256)
        data.append(uniq[i][2] ^ rb)
    out = list(data)
    for idx in range(len(js) - 1, -1, -1):
        i = N - 1 - idx
        j = js[idx]
        out[i], out[j] = out[j], out[i]
    res = bytes(out)
    open("/mnt/c/Users/arnol/AppData/Local/Temp/cylab_206/recovered.bin", "wb").write(res)
    print("taille:", len(res))
    print("debut:", res[:200])
    import re
    m = re.search(rb"(?:academy|picoCTF)\{[^}]*\}", res)
    if m:
        print("FLAG:", m.group(0).decode())
