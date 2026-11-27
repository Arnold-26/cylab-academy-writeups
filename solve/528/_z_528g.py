import sys, zipfile, pathlib
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
B = pathlib.Path(r"C:\Users\arnol\AppData\Local\Temp\cylab_eps\528_minions.apk")
z = zipfile.ZipFile(B)
LIB = ("abc_", "m3_", "mtrl_", "design_", "notification_", "material_", "preference_", "tooltip",
       "btn_", "ic_", "common_", "browser_", "exo_", "media3_", "sidebar", "nav_", "action_",
       "appbar", "bottom_", "chip_", "color_", "card_", "fab_", "switch", "text_", "androidx",
       "test_", "layout_", "mtrl")
out = []
for n in z.namelist():
    if not n.startswith("res/"):
        continue
    base = n.rsplit("/", 1)[-1].lower()
    if any(base.startswith(p) for p in LIB):
        continue
    out.append((n, z.getinfo(n).file_size))
print("=== %d fichiers propres a l'app ===" % len(out))
for n, s in out:
    print("  %-60s %d" % (n, s))
