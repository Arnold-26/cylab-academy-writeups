import sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from PIL import Image, ImageChops
import numpy as np
A = Image.open(r"C:\Users\arnol\AppData\Local\Temp\cylab_eps\o141\duck.png").convert("RGB")
B = Image.open(r"C:\Users\arnol\AppData\Local\Temp\cylab_eps\o141\evil_duck.png").convert("RGB")
print("tailles:", A.size, B.size)
if A.size != B.size:
    B = B.resize(A.size)
a = np.asarray(A).astype(int)
b = np.asarray(B).astype(int)
diff = np.abs(a - b).astype(np.uint8)
print("diff max:", diff.max(), "| moyenne:", diff.mean(), "| pixels differents:", int((diff.sum(axis=2) > 0).sum()))
Image.fromarray(diff).save(r"C:\Users\arnol\AppData\Local\Temp\cylab_eps\o141\diff.png")
# amplification
amp = np.clip(diff * 20, 0, 255).astype(np.uint8)
Image.fromarray(amp).save(r"C:\Users\arnol\AppData\Local\Temp\cylab_eps\o141\diff_amp.png")
print("ecrit diff.png et diff_amp.png")
