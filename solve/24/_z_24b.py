import sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
start = 0x3b9aca00
add = 0x499602d2
print("start:", start, "add:", add)
vals = []
v = start
for k in range(1, 20):
    v = (v + add) & 0xFFFFFFFF
    sv = v - 2 ** 32 if v >= 2 ** 31 else v
    vals.append((k, v, sv))
    print(k, "unsigned:", v, "signed:", sv)
target = 4175074816
print("\n4175074816 dans la sequence:", any(v == target for _, v, _ in vals))
