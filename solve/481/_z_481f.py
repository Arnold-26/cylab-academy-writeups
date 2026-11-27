import sys, pathlib, subprocess
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
BASE = pathlib.Path("/tmp/cylab_z/481")
files = sorted(BASE.glob("*.png"))
print("fichiers:", len(files), flush=True)
import re
FLAG = re.compile(r"(?:academy|picoCTF|PICOCTF)\{[^}]*\}")
try:
    import stepic
    from PIL import Image
    Image.MAX_IMAGE_PIXELS = None
    for f in files:
        try:
            im = Image.open(f)
            data = stepic.decode(im)
            if isinstance(data, str):
                txt = data
            else:
                txt = data.decode("utf-8", "ignore")
            if txt.strip():
                print(f"{f.name}: {txt[:200]!r}")
                m = FLAG.search(txt)
                if m:
                    print("FLAG:", m.group(0))
                    break
        except Exception:
            pass
except ImportError:
    print("stepic absent")
