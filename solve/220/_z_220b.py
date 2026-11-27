import sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
a = open("/tmp/cylab_eps/220_breadth.v1", "rb").read()
b = open("/tmp/cylab_eps/220_breadth.v2", "rb").read()
print("tailles:", len(a), len(b))
diffs = []
n = min(len(a), len(b))
for i in range(n):
    if a[i] != b[i]:
        diffs.append(i)
print("octets differents:", len(diffs))
if diffs:
    print("premier:", hex(diffs[0]), "dernier:", hex(diffs[-1]))
    # regrouper en plages
    ranges = []
    start = prev = diffs[0]
    for i in diffs[1:]:
        if i == prev + 1:
            prev = i
        else:
            ranges.append((start, prev))
            start = prev = i
    ranges.append((start, prev))
    print("plages:", len(ranges))
    for s, e in ranges[:20]:
        print(f"  0x{s:x}-0x{e:x} ({e-s+1} o)")
        print(f"    v1: {a[s:e+1].hex()}")
        print(f"    v2: {b[s:e+1].hex()}")
