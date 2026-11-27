import sys, re, requests, pathlib
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
requests.packages.urllib3.disable_warnings()
B = pathlib.Path(r"C:\Users\arnol\AppData\Local\Temp\cylab_eps")
for url, name in (
    ("https://challenge-files.cylabacademy.net/library/8fde883b8eb340c0eb1a1b754cbcb89e4ac5793b2db335218dadb6e750e58060/game", "345_game"),
    ("https://challenge-files.cylabacademy.net/library/a58b5ad9d6b7d25c303b279a792b7cc78780fc93b11734c87c45b6fa256809f3/game", "346_game"),
):
    dest = B / name
    if dest.exists() and dest.stat().st_size > 1000:
        print("deja", name, dest.stat().st_size)
        continue
    try:
        r = requests.get(url, timeout=90, verify=False)
        dest.write_bytes(r.content)
        print("ok", name, len(r.content))
    except Exception as e:
        print("err", name, type(e).__name__)
