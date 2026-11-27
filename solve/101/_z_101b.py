import sys, re, pathlib, zipfile
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
FLAGB = re.compile(rb"(?:academy|picoCTF|PICOCTF)\{[^}]*\}")
p = pathlib.Path(r"C:\Users\arnol\AppData\Local\Temp\cylab_wf\weird.docm")
z = zipfile.ZipFile(p)
for n in z.namelist():
    data = z.read(n)
    m = FLAGB.search(data)
    if m:
        print("FLAG dans", n, ":", m.group(0).decode())
vba = z.read("word/vbaProject.bin")
out = pathlib.Path(r"C:\Users\arnol\AppData\Local\Temp\cylab_wf\vbaProject.bin")
out.write_bytes(vba)
print("vbaProject.bin:", len(vba), "octets")
# strings lisibles dans la macro
txt = "".join(chr(b) if 32 <= b < 127 else "." for b in vba)
for kw in ("flag", "academy", "pico", "Shell", "CreateObject"):
    i = txt.lower().find(kw.lower())
    if i >= 0:
        print(f"{kw}: ...{txt[max(0,i-100):i+200]}...")
