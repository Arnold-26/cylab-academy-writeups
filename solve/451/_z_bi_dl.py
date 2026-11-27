import requests, zipfile, io, os, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
requests.packages.urllib3.disable_warnings()

jobs = [
    ("https://challenge-files.cylabacademy.net/library/b707862077450010bce3c050b139b7c00762859eb94eea5db8eded717a6318d0/bininst1.zip", "_z_bi1"),
    ("https://challenge-files.cylabacademy.net/library/ce8f745beda824c87d5482c853c90b7758b9a95d9b05db0c74fb2b0678f8115b/bininst2.zip", "_z_bi2"),
]
for url, out in jobs:
    r = requests.get(url, timeout=180, verify=False)
    print(out, len(r.content), r.status_code)
    z = zipfile.ZipFile(io.BytesIO(r.content))
    os.makedirs(r"./%s" % out, exist_ok=True)
    for i in z.infolist():
        if i.is_dir():
            continue
        data = z.read(i.filename, pwd=b"academy")
        p = os.path.join(r"./%s" % out, os.path.basename(i.filename))
        open(p, "wb").write(data)
        print("   ", p, len(data))
