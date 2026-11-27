import sys, zipfile, pathlib
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
src = pathlib.Path(r"C:\Users\arnol\AppData\Local\Temp\cylab_y\suspicious.zip")
print("taille zip:", src.stat().st_size)
try:
    z = zipfile.ZipFile(src)
    print("noms:", z.namelist())
    for n in z.namelist():
        info = z.getinfo(n)
        print(n, "compress:", info.compress_type, "size:", info.file_size)
        data = z.read(n)
        print("lu:", len(data), "octets")
        out = pathlib.Path(r"C:\Users\arnol\AppData\Local\Temp\cylab_y") / "exe.bin"
        out.write_bytes(data)
        print("ecrit:", out, len(data))
except Exception as e:
    print("err:", type(e).__name__, e)
