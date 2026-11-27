import sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
CT = "OHMLFMWCAI"
print("toutes les 312 lectures:")
for a in range(1, 26):
    if a % 2 == 0 or a == 13:
        continue
    ainv = pow(a, -1, 26)
    for b in range(26):
        pt = "".join(chr(((ord(c) - 65 - b) % 26 * ainv) % 26 + 65) for c in CT)
        print(f"{pt}  a={a} b={b}")
