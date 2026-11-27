import sys, zipfile, re, pathlib
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
B = pathlib.Path(r"/tmp/cylab_eps\528_minions.apk")
z = zipfile.ZipFile(B)
LIB = ("abc_", "m3_", "mtrl_", "design_", "notification_", "material_", "preference_", "tooltip",
       "btn_", "ic_", "common_", "browser_", "exo_", "media3_", "sidebar", "nav_", "action_",
       "appbar", "bottom_", "chip_", "color_", "card", "fab_", "switch", "text_", "androidx")
print("=== ressources specifiques a l'app ===")
for n in z.namelist():
    if not n.startswith("res/"):
        continue
    base = n.split("/", 1)[1]
    low = base.lower()
    if any(low.startswith(p) for p in LIB):
        continue
    print("  %-60s %d" % (n, z.getinfo(n).file_size))
