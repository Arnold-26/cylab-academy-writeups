import sys, zipfile, struct, pathlib, binascii
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
B = pathlib.Path(r"C:\Users\arnol\AppData\Local\Temp\cylab_eps")
z = zipfile.ZipFile(B / "56_b1g_mac.zip")


def ntfs(extra):
    i = 0
    while i + 4 <= len(extra):
        hid, hsz = struct.unpack_from("<HH", extra, i)
        body = extra[i + 4:i + 4 + hsz]
        if hid == 0x000A:
            j = 4
            while j + 4 <= len(body):
                tag, tsz = struct.unpack_from("<HH", body, j)
                if tag == 0x0001 and tsz >= 24:
                    return struct.unpack_from("<QQQ", body, j + 4)
                j += 4 + tsz
        i += 4 + hsz
    return None


copies, originals = [], []
for n in sorted(z.namelist()):
    if n.endswith("/"):
        continue
    t = ntfs(z.getinfo(n).extra)
    if not t:
        continue
    if " - Copy" in n:
        copies.append((n, t))
    else:
        originals.append((n, t))

print("copies:", len(copies))
for n, (m, a, c) in copies:
    print("  %-26s M%%65536=%5d  M%%1000000=%06d  (M hex bas: %s)" %
          (n.split("/")[-1], m % 65536, m % 1000000, hex(m)[-4:]))

for which, label in ((0, "M"), (1, "A"), (2, "C")):
    for mod, ml in ((65536, "16 bits"), (1000000, "1e6")):
        out = b""
        for n, t in copies:
            v = t[which] % mod
            out += v.to_bytes(2, "big") if mod == 65536 else b""
        if out:
            print(f"\n[{label} {ml}] {out!r}")
        else:
            s = "".join(str(t[which] % mod).zfill(6) for n, t in copies)
            print(f"\n[{label} {ml}] {s}")
