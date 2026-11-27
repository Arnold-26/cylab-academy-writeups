import sys, subprocess, random
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

PCAP = "/tmp/cylab_206/capture.pcapng"
r = subprocess.run(["tshark", "-r", PCAP, "-Y", "udp", "-T", "fields",
                    "-e", "frame.time_epoch", "-e", "udp.srcport", "-e", "udp.payload"],
                   capture_output=True, text=True, timeout=900)
packets = []
for line in (r.stdout or "").splitlines():
    parts = line.split("\t")
    if len(parts) < 3:
        continue
    try:
        ts = float(parts[0]); sport = int(parts[1]); payload = bytes.fromhex(parts[2].strip())
    except Exception:
        continue
    if len(payload) == 1:
        packets.append((ts, sport, payload[0]))
print("paquets:", len(packets))
N = len(packets)
t0 = packets[0][0]
print("t0:", t0)
target_ports = [p[1] for p in packets[:5]]
print("ports cibles:", target_ports)

found = None
lo, hi = int(t0) - 7200, int(t0) + 120
print("recherche seeds", lo, "->", hi)
for seed in range(lo, hi):
    rnd = random.Random(seed)
    for i in range(N - 1, 0, -1):
        rnd.randrange(i + 1)
    ok = True
    for k in range(5):
        if rnd.randrange(65536) != target_ports[k]:
            ok = False
            break
        rnd.randrange(256)
    if ok:
        found = seed
        print("SEED:", seed)
        break
print("resultat:", found)
