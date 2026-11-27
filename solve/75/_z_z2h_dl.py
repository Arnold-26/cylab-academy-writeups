import requests, sys, os, time
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
requests.packages.urllib3.disable_warnings()

BASE = "https://challenge-files.cylabacademy.net/library/382c5b96d01225092147c478e5e99157a70b4918c8a000845ea02c4b197eea8a/"
for name, out in (("libc.so.6", r"./_z_z2h_libc.so.6"),
                  ("ld-2.29.so", r"./_z_z2h_ld-2.29.so")):
    url = BASE + name
    try:
        h = requests.head(url, timeout=30, verify=False)
        total = int(h.headers.get("Content-Length", 0))
    except Exception:
        total = 0
    have = os.path.getsize(out) if os.path.exists(out) else 0
    print(name, "size", total, "have", have, flush=True)
    if have == total and total:
        print("  already complete", flush=True)
        continue
    t0 = time.time()
    while True:
        if total and have >= total:
            break
        try:
            r = requests.get(url, headers={"Range": "bytes=%d-" % have}, timeout=60, stream=True, verify=False)
            if r.status_code not in (200, 206):
                print("  bad status", r.status_code, flush=True)
                break
            with open(out, "ab") as f:
                for chunk in r.iter_content(65536):
                    if chunk:
                        f.write(chunk)
                        have += len(chunk)
            if not total:
                total = have
                break
        except Exception as e:
            print("  retry", type(e).__name__, "have", have, flush=True)
            time.sleep(2)
            have = os.path.getsize(out) if os.path.exists(out) else 0
            if total and have >= total:
                break
            if time.time() - t0 > 240:
                break
    print("  done", os.path.getsize(out) if os.path.exists(out) else 0, flush=True)
