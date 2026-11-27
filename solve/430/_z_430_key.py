import struct
raw = open('/tmp/w300/config.bin','rb').read()
size = struct.unpack('<I', raw[:4])[0]
data = raw[4:]
L = list(data[0:size])          # lettres originales
CT = list(data[size+1:size+1+size])  # flag chiffre
print("L  =", bytes(L))
print("CT =", CT)

def keyof(pt):
    return [CT[i]^pt[i] for i in range(len(pt))]

pt = b"academy{"
K = keyof(pt)
print("K(academy{) =", bytes(K))

# ch0 = 0x61 ; K[j] = ch_{j+1}
chs = [0x61] + K
print("deltas mod26  =", [(chs[j+1]-chs[j]) for j in range(len(K))])
print("deltas%26     =", [(chs[j+1]-chs[j]) % 26 for j in range(len(K))])

def pc(m): return bin(m).count('1')
for j in range(len(K)):
    prev = chs[j]
    v = L[j] - prev + pc(j % 255)
    print(f"j={j} L={chr(L[j])!r} ch_prev={prev:#x}({prev if prev<128 else prev-256}) "
          f"pc={pc(j%255)} v={v} v%26={((v%26)-26 if v%26>13 else v%26)} "
          f"attendu_delta={chs[j+1]-chs[j]}")

# hypothèse alternative : pc calcule sur j (pas j%255)
print("\n-- variantes pc et v --")
def tryf(name, fv, fpc, nrange=1):
    ch = 0x61
    out = []
    for rep in range(nrange):
        for j in range(size):
            pass
    return None

cands = {}
for pename, pe in [('j%255', lambda j: j%255), ('j', lambda j: j),
                   ('j%256', lambda j: j%256), ('j+1', lambda j: j+1)]:
    for vname, vf in [('L-ch+pc', lambda L,ch,p: L-ch+p),
                      ('L-ch-pc', lambda L,ch,p: L-ch-p),
                      ('L+ch+pc', lambda L,ch,p: L+ch+p)]:
        for modkind in ['C', 'py']:
            ch = 0x61
            out = bytearray()
            for j in range(size):
                p = pc(pe(j))
                v = vf(L[j], ch, p)
                d = v % 26 if modkind=='py' else (abs(v)%26)*(1 if v>=0 else -1)
                ch = (ch + d) % 256
                out.append(ch)
            score = sum(1 for i in range(len(K)) if out[i]==K[i])
            print(f"{pename:7s} {vname:8s} {modkind:2s} score={score}/{len(K)} head={bytes(out[:10])!r}")
