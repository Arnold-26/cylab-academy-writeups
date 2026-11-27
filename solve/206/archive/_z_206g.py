import sys, subprocess, random
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

PCAP = "/tmp/cylab_206/capture.pcapng"
r = subprocess.run(["tshark", "-r", PCAP, "-Y", "udp", "-T", "fields",
                    "-e", "frame.number", "-e", "frame.time_epoch", "-e", "udp.srcport", "-e", "udp.payload", "-e", "eth.src"],
                   capture_output=True, text=True, timeout=900)
rows = []
for line in (r.stdout or "").splitlines():
    parts = line.split("\t")
    if len(parts) < 4:
        continue
    try:
        ts = float(parts[1]); sport = int(parts[2]); payload = bytes.fromhex(parts[3].strip())
    except Exception:
        continue
    if len(payload) == 1:
        rows.append((parts[0], ts, sport, payload[0], parts[4] if len(parts) > 4 else ""))
print("total:", len(rows))
# dedupliquer : garder une seule copie par (sport, payload) consecutif
uniq = []
prev = None
for row in rows:
    key = (row[2], row[3])
    if key == prev:
        continue
    uniq.append(row)
    prev = key
print("uniques:", len(uniq))
N = len(uniq)
print("premiers:", [(u[2], u[3]) for u in uniq[:6]])
target_ports = [u[2] for u in uniq[:6]]
lo, hi = int(uniq[0][1]) - 7200, int(uniq[0][1]) + 120
found = None
for seed in range(lo, hi):
    rnd = random.Random(seed)
    for i in range(N - 1, 0, -1):
        rnd.randrange(i + 1)
    ok = True
    for k in range(6):
        if rnd.randrange(65536) != target_ports[k]:
            ok = False
            break
        rnd.randrange(256)
    if ok:
        found = seed
        break
print("SEED:", found)
if found:
    rnd = random.Random(found)
    js = []
    for i in range(N - 1, 0, -1):
        js.append(rnd.randrange(i + 1))
    data = []
    for i in range(N):
        rnd.randrange(65536)
        rb = rnd.randrange(256)
        data.append(uniq[i][3] ^ rb)
    out = list(data)
    for idx in range(len(js) - 1, -1, -1):
        i = idx + 1
        j = js[idx]
        out[i], out[j] = out[j], out[i]
    res = bytes(out)
    open("/tmp/cylab_206/recovered.bin", "wb").write(res)
    print("recovered:", len(res))
    print("debut:", res[:300])
