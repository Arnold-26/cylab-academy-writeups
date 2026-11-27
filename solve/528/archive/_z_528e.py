import sys, zipfile, re, pathlib
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
B = pathlib.Path(r"/tmp/cylab_eps\528_minions.apk")
z = zipfile.ZipFile(B)
print("=== res/ ===")
for n in z.namelist():
    if n.startswith("res/"):
        print("  %-55s %d" % (n, z.getinfo(n).file_size))
print("\n=== resources.arsc : chaines lisibles ===")
data = z.read("resources.arsc")
strs = [s.decode("utf-8", "replace") for s in re.findall(rb"[ -~]{5,90}", data)]
for s in strs[:60]:
    print("   ", s)
