import sys, requests, pathlib, time
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
requests.packages.urllib3.disable_warnings()
url = "https://challenge-files.cylabacademy.net/picoMini+by+redpwn/Forensics/scrambled-bytes/capture.pcapng"
dest = pathlib.Path(r"C:\Users\arnol\AppData\Local\Temp\cylab_206\capture.pcapng")
dest.parent.mkdir(parents=True, exist_ok=True)
total = None
try:
    r = requests.get(url, headers={"Range": "bytes=0-0"}, timeout=60, verify=False, stream=True)
    cr = r.headers.get("content-range")
    if cr and "/" in cr:
        total = int(cr.split("/")[-1])
    r.close()
except Exception as e:
    print("head err", e)
print("total:", total, flush=True)
have = dest.stat().st_size if dest.exists() else 0
att = 0
while (total is None or have < total) and att < 80:
    att += 1
    try:
        with requests.get(url, headers={"Range": f"bytes={have}-"}, timeout=(20, 120), verify=False, stream=True) as r:
            if r.status_code not in (200, 206):
                print("status", r.status_code)
                break
            with open(dest, "ab") as f:
                for chunk in r.iter_content(1 << 20):
                    if chunk:
                        f.write(chunk)
                        have += len(chunk)
        print(f"{att}: {have}/{total}", flush=True)
    except Exception as e:
        print(f"{att} err {type(e).__name__}", flush=True)
        time.sleep(1)
print("final:", have, "/", total, flush=True)
