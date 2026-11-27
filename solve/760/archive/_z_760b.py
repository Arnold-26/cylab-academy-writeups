import sys, requests, pathlib, re
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
requests.packages.urllib3.disable_warnings()
B = pathlib.Path(r"/tmp/cylab_eps")
files = {
    "760_IntOverflowBank.sol": "https://challenge-files.cylabacademy.net/library/42fdf938c25aa01fabfedf48630ec171d19acfd1bf2d9abd130ff86ad51a9068/IntOverflowBank.sol",
    "723_AccessControl.sol": "https://challenge-files.cylabacademy.net/library/4ace2f9c4b176be6fd783cffab3351b8de943d802146d3d77adaa487d93ed78a/AccessControl.sol",
}
for name, u in files.items():
    dest = B / name
    if not (dest.exists() and dest.stat().st_size > 10):
        try:
            r = requests.get(u, timeout=30, verify=False)
            dest.write_bytes(r.content)
        except Exception as e:
            print("err", name, type(e).__name__)
            continue
    print("=== %s (%d o) ===" % (name, dest.stat().st_size))
    print(dest.read_text(errors="replace")[:1500])
    print()
for port in (29641, 22404):
    try:
        r = requests.get(f"http://xebec.cylabacademy.net:{port}/", timeout=25, verify=False)
        t = re.sub(r"<[^>]+>", " ", r.text)
        t = re.sub(r"\s+", " ", t)
        print(f"=== details :{port} -> {r.status_code} ===")
        print(t[:700])
    except Exception as e:
        print(port, "ERR", type(e).__name__)
    print()
