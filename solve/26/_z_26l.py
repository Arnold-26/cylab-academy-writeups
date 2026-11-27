import sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from PIL import Image
p = "/mnt/c/Users/arnol/AppData/Local/Temp/cylab_m00n/spec26.png"
im = Image.open(p)
print("taille:", im.size)
im.thumbnail((1600, 900))
out = "/mnt/c/Users/arnol/AppData/Local/Temp/cylab_m00n/spec26_small.png"
im.convert("RGB").save(out)
print("ok:", out, im.size)
