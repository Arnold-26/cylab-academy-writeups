import sys, subprocess, re, random, json
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

PCAP = "/tmp/cylab_206/capture.pcapng"
# extraire les paquets : sport, payload (1 octet), timestamp
r = subprocess.run(["tshark", "-r", PCAP, "-Y", "udp", "-T", "fields",
                    "-e", "frame.time_epoch", "-e", "udp.srcport", "-e", "udp.payload", "-e", "ip.src"],
                   capture_output=True, text=True, timeout=600)
lines = [l for l in (r.stdout or "").splitlines() if l.strip()]
print("paquets udp:", len(lines))
packets = []
for line in lines:
    parts = line.split("\t")
    if len(parts) < 4:
        continue
    try:
        ts = float(parts[0])
        sport = int(parts[1])
        payload = bytes.fromhex(parts[2].strip())
    except Exception:
        continue
    if len(payload) != 1:
        continue
    packets.append((ts, sport, payload[0], parts[3]))
print("paquets 1 octet:", len(packets))
if not packets:
    sys.exit(1)
t0 = packets[0][0]
print("t0:", t0, "premier sport:", packets[0][1], "src:", packets[0][3])
N = len(packets)
# chercher le seed
found = None
for seed in range(int(t0) - 300, int(t0) + 60):
    rnd = random.Random(seed)
    # simuler le shuffle
    order = list(range(N))
    ok = True
    js = []
    for i in range(N - 1, 0, -1):
        j = rnd.randrange(i + 1)
        js.append(j)
        order[i], order[j] = order[j], order[i]
    # verifier les ports
    good = True
    for i in range(min(8, N)):
        p = rnd.randrange(65536)
        if p != packets[i][1]:
            good = False
            break
        rnd.randrange(256)
    if good:
        found = (seed, js)
        print("SEED TROUVE:", seed)
        break
print("seed:", found[0] if found else None)
if found:
    seed, js = found
    rnd = random.Random(seed)
    for i in range(N - 1, 0, -1):
        rnd.randrange(i + 1)
    data = []
    for i in range(N):
        rnd.randrange(65536)
        rb = rnd.randrange(256)
        data.append(packets[i][2] ^ rb)
    # inverser le shuffle : on a l'ordre melange -> remettre en place
    out = list(data)
    for idx in range(len(js) - 1, -1, -1):
        i = idx + 1
        j = js[idx]
        out[i], out[j] = out[j], out[i]
    res = bytes(out)
    open("/tmp/cylab_206/recovered.bin", "wb").write(res)
    print("recovered:", len(res))
    print("debut:", res[:200])
