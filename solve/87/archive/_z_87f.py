import sys, re
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
p = r"/tmp/cylab_eps\87_suspicious.dd.sda1"
with open(p, "rb") as f:
    f.seek(2049 * 1024)
    data = f.read(1024)
slack = data[55:]
raw = slack.rstrip(b"\x00")
print("slack len:", len(raw))
txt = raw.decode("utf-16le", "replace")
print("utf16le:", repr(txt))
rev = txt[::-1]
print("inverse:", repr(rev))
m = re.search(r"(?:academy|picoCTF)\{[^}]*\}", rev)
print("FLAG:", m.group(0) if m else None)
