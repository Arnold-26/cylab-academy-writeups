import sys, re, requests, pathlib
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
requests.packages.urllib3.disable_warnings()
BASE = pathlib.Path(r"C:\Users\arnol\AppData\Local\Temp\cylab_206")
BASE.mkdir(exist_ok=True)
for name, url in (("send.py", "https://challenge-files.cylabacademy.net/picoMini+by+redpwn/Forensics/scrambled-bytes/send.py"),
                  ("capture.pcapng", "https://challenge-files.cylabacademy.net/picoMini+by+redpwn/Forensics/scrambled-bytes/capture.pcapng")):
    try:
        r = requests.get(url, timeout=120, verify=False)
        (BASE / name).write_bytes(r.content)
        print("ok:", name, len(r.content))
    except Exception as e:
        print("err", name, type(e).__name__, e)
p = BASE / "send.py"
if p.exists():
    print("\n=== send.py ===")
    print(p.read_text(encoding="utf-8", errors="replace")[:2000])
