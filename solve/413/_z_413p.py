import sys, os, time, requests, urllib3
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
urllib3.disable_warnings()
B = r"C:\Users\arnol\AppData\Local\Temp\cylab_eps"
dest = os.path.join(B, "413_full.img.gz")
u = "https://challenge-files.cylabacademy.net/library/a25bb84ce58309d7ba5cfe01dd4d6d2ce05e5d4cfd5307216cec07d1eab3267c/disk.flag.img.gz"
for attempt in range(8):
    have = os.path.getsize(dest) if os.path.exists(dest) else 0
    headers = {"Range": "bytes=%d-" % have} if have else {}
    try:
        r = requests.get(u, headers=headers, timeout=60, verify=False, stream=True)
        if r.status_code == 416:
            print("deja complet")
            break
        mode = "ab" if have and r.status_code == 206 else "wb"
        if mode == "wb":
            have = 0
        with open(dest, mode) as f:
            for chunk in r.iter_content(1 << 20):
                f.write(chunk)
                have += len(chunk)
        print("tentative %d: %d octets (status %d)" % (attempt + 1, have, r.status_code), flush=True)
    except Exception as e:
        print("tentative %d ERR %s (total %d)" % (attempt + 1, type(e).__name__, have), flush=True)
        time.sleep(5)
print("taille finale:", os.path.getsize(dest) if os.path.exists(dest) else 0)
