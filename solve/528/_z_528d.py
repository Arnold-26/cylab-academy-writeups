import sys, zipfile, re, pathlib
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
B = pathlib.Path(r"C:\Users\arnol\AppData\Local\Temp\cylab_eps\528_minions.apk")
z = zipfile.ZipFile(B)
for dex in ("classes3.dex", "classes2.dex"):
    data = z.read(dex)
    print("=== %s (%d o) : chaines ===" % (dex, len(data)))
    strs = [s.decode("utf-8", "replace") for s in re.findall(rb"[ -~]{4,80}", data)]
    # filtrer le bruit
    keep = [s for s in strs if not s.startswith(("Landroid", "Ljava", "Lkotlin", "Lcom/google"))]
    for s in keep[:70]:
        print("   ", s)
    print()
