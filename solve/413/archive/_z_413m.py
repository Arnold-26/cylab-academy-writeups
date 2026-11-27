import sys, re
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
p = r"/tmp/cylab_eps/t413_dummy"
img = "/tmp/t413.img"
d = open(img, "rb").read()
needle = b"innocuous-file.txt"
offs = []
i = 0
while True:
    i = d.find(needle, i)
    if i < 0:
        break
    offs.append(i)
    i += 1
print("occurrences:", len(offs))
for o in offs:
    ctx = d[max(0, o - 40):o + len(needle) + 40]
    print("--- offset", o, "---")
    print("   ", re.sub(rb"[^\x20-\x7e]", b".", ctx).decode("latin-1"))
