import sys, subprocess, re
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
out = subprocess.run(["wsl", "-d", "kali-linux", "--", "bash", "-c",
                      "cd /mnt/c/Users/arnol/AppData/Local/Temp/cylab_eps && "
                      "tshark -r 311_torrent.pcap -Y 'bt-dht' -T fields -e frame.number -e data.data 2>/dev/null"],
                     capture_output=True, text=True).stdout
lines = out.splitlines()
print("trames bt-dht:", len(lines))
found = 0
for line in lines[:200]:
    p = line.split("\t")
    if len(p) < 2:
        continue
    raw = bytes.fromhex(p[1].replace(":", ""))
    if b"d1:" in raw or b"1:y" in raw:
        txt = raw.decode("latin-1", "replace")
        if found < 8:
            print("frame %s: %r" % (p[0], txt[:220]))
        found += 1
        m = re.search(r"(?:academy|picoCTF)\{[^}]*\}", txt)
        if m:
            print(">>> FLAG:", m.group(0))
print("messages bencode:", found)
