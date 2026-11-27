import sys, subprocess, re
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
out = subprocess.run(["wsl", "-d", "kali-linux", "--", "bash", "-c",
                      "cd /mnt/c/Users/arnol/AppData/Local/Temp/cylab_eps && "
                      "tshark -r 311_torrent.pcap -Y udp -T fields -e frame.number -e ip.src -e udp.srcport -e udp.payload 2>/dev/null"],
                     capture_output=True, text=True).stdout
lines = out.splitlines()
print("trames udp:", len(lines))
hits = 0
seen = set()
for line in lines:
    p = line.split("\t")
    if len(p) < 4:
        continue
    try:
        raw = bytes.fromhex(p[3].replace(":", ""))
    except Exception:
        continue
    if not raw:
        continue
    if raw[:1] == b"d":
        txt = raw.decode("latin-1", "replace")
        if hits < 10:
            print("frame %-6s %-14s %-6s %r" % (p[0], p[1], p[2], txt[:180]))
        hits += 1
        for m in re.finditer(r"(?:academy|picoCTF)\{[^}]*\}", txt):
            print(">>> FLAG:", m.group(0))
print("payloads bencode:", hits)
