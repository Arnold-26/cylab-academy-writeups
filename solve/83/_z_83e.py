import sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
enc = open(r"D:\ctf-index\t83_encoded.bmp", "rb").read() if False else open("/tmp/enc83.bmp", "rb").read()
