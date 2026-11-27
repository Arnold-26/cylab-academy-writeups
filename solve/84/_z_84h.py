import sys, collections
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
import subprocess
out = subprocess.run(["wsl", "-d", "kali-linux", "--", "bash", "-c",
                      "cd /tmp/cylab_eps && "
                      "tshark -r 84_shark-on-wire-2-capture.pcap -Y udp -T fields "
                      "-e frame.number -e ip.src -e udp.srcport -e udp.dstport 2>/dev/null"],
                     capture_output=True, text=True).stdout
rows = []
for line in out.splitlines():
    p = line.split("\t")
    if len(p) < 4:
        continue
    fn, src, sp, dp = p[:4]
    try:
        rows.append((int(fn), src, int(sp) if sp else 0, int(dp) if dp else 0))
    except Exception:
        continue
print("paquets UDP:", len(rows))
by_src = collections.Counter(r[1] for r in rows)
print("sources:", by_src)
for src in by_src:
    ports = [r[2] for r in rows if r[1] == src]
    uniq = len(set(ports))
    print("%-18s ports uniques: %d | min %d max %d" % (src, uniq, min(ports), max(ports)))
# pour chaque source, tenter char = srcport - 5000
for src in by_src:
    seq = []
    for fn, s, sp, dp in rows:
        if s != src:
            continue
        v = sp - 5000
        if 32 <= v < 127:
            seq.append(chr(v))
    if seq:
        txt = "".join(seq)
        print("\n[%s] => %r" % (src, txt[:200]))
