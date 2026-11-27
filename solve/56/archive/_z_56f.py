import sys, zipfile, struct, pathlib, re
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
B = pathlib.Path(r"/tmp/cylab_eps")
z = zipfile.ZipFile(B / "56_b1g_mac.zip")


def ntfs_times(extra):
    """retourne (mtime, atime, ctime) FILETIME depuis l'extra field 0x000a"""
    i = 0
    out = []
    while i + 4 <= len(extra):
        hid, hsz = struct.unpack_from("<HH", extra, i)
        body = extra[i + 4:i + 4 + hsz]
        if hid == 0x000A:
            # 4 octets reserves puis tag 0x0001, size 24
            j = 4
            while j + 4 <= len(body):
                tag, tsz = struct.unpack_from("<HH", body, j)
                if tag == 0x0001 and tsz >= 24:
                    m, a, c = struct.unpack_from("<QQQ", body, j + 4)
                    out.append((m, a, c))
                j += 4 + tsz
        i += 4 + hsz
    return out


names = sorted(z.namelist())
print("=== entrees avec extra fields ===")
for n in names:
    if n.endswith("/"):
        continue
    info = z.getinfo(n)
    times = ntfs_times(info.extra)
    print("%-28s extra=%3d o  ntfs=%s" % (n, len(info.extra), bool(times)))
    for (m, a, c) in times:
        print("     M=%d A=%d C=%d" % (m, a, c))
