import sys, base64, itertools, re, subprocess
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
FLAG = re.compile(rb"(?:academy|picoCTF|PICOCTF)\{[^}]*\}")
r = subprocess.run(["wsl", "-d", "kali-linux", "--", "bash", "-lc",
                    "tshark -r /tmp/tl/rogue_tower.pcap -Y 'ip.dst==198.51.100.177' -T fields -e frame.number -e data.data 2>/dev/null"],
                   capture_output=True, text=True)
chunks = []
for line in r.stdout.splitlines():
    p = line.split("\t")
    if len(p) < 2:
        continue
    h = p[1].strip()
    if not h:
        continue
    try:
        chunks.append(bytes.fromhex(h).decode("latin-1"))
    except Exception:
        pass
print("chunks:", chunks)
raw = "".join(chunks)
print("raw:", raw, "len", len(raw))
try:
    d = base64.b64decode(raw + "=" * (-len(raw) % 4))
    print("decode:", d, d.hex())
except Exception as e:
    print("err:", e)
    d = b""
if d:
    for k in (b"94309", b"310410743419304", b"310410", b"23104", b"network", b"carrier"):
        x = bytes(b ^ k[i % len(k)] for i, b in enumerate(d))
        if FLAG.search(x):
            print("FLAG xor", k, FLAG.search(x).group(0))
        print(k, x[:40])
