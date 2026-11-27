import sys, datetime
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
rows = []
for line in open("/tmp/tl721.txt", encoding="utf-8", errors="replace"):
    p = line.rstrip("\n").split("|")
    if len(p) < 11:
        continue
    try:
        mt, at, ct, cr = int(p[7]), int(p[8]), int(p[9]), int(p[10])
    except ValueError:
        continue
    rows.append((mt, p[1], p[3], int(p[6]) if p[6].isdigit() else 0, at, ct, cr))
rows.sort(reverse=True)
print("total:", len(rows))
print("=== 30 mtime les plus recents ===")
for mt, path, perms, size, at, ct, cr in rows[:30]:
    print("  %s  %-55s %8d  %s" % (datetime.datetime.utcfromtimestamp(mt).strftime("%Y-%m-%d %H:%M:%S"),
                                   path[:55], size, perms))
