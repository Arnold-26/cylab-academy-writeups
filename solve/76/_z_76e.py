import sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from PIL import Image, ImageOps, ImageEnhance
import numpy as np

p = "/mnt/c/Users/arnol/AppData/Local/Temp/cylab_cr/dec_skip0.png"
im = Image.open(p).convert("RGB")
# la ligne de texte est vers y=390
crop = im.crop((150, 350, 1750, 440))
a = np.array(crop).astype(np.float32)
# normaliser par colonne pour retirer le bruit de fond
g = a.mean(axis=2)
# contraste
lo, hi = np.percentile(g, 5), np.percentile(g, 95)
g2 = np.clip((g - lo) / max(hi - lo, 1) * 255, 0, 255).astype(np.uint8)
out = Image.fromarray(g2)
out = out.resize((out.width * 2, out.height * 2), Image.LANCZOS)
out.save("/mnt/c/Users/arnol/AppData/Local/Temp/cylab_cr/text_enh.png")
print("ecrit:", out.size)
# version seuillee
thr = (g2 > g2.mean()).astype(np.uint8) * 255
Image.fromarray(thr).resize((out.width, out.height), Image.LANCZOS).save("/mnt/c/Users/arnol/AppData/Local/Temp/cylab_cr/text_thr.png")
print("seuille ecrit")
