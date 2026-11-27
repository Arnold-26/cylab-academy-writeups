import sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from PIL import Image
im = Image.open("/mnt/c/Users/arnol/AppData/Local/Temp/cylab_cr/dec.png").convert("RGB")
w, h = im.size
print("taille:", im.size)
# recadrer la zone du texte (approx y 320-430, x 120-1750)
crop = im.crop((100, 300, 1800, 450))
crop = crop.resize((crop.width * 2, crop.height * 2), Image.LANCZOS)
crop.save("/mnt/c/Users/arnol/AppData/Local/Temp/cylab_cr/zoom.png")
print("zoom ecrit:", crop.size)
# variante : normaliser les blocs (renforcer le contraste)
import numpy as np
a = np.array(im)
print("shape:", a.shape)
