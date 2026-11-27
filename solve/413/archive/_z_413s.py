import sys, re
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
img = "/tmp/t413full.img"
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
for k, o in enumerate(offs):
    ctx = d[max(0, o - 70):o + len(needle) + 70]
    print("--- #%d offset %d ---" % (k, o))
    print("   ", re.sub(rb"[^\x20-\x7e]", b".", ctx).decode("latin-1"))
