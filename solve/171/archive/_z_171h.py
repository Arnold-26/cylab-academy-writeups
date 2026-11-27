import sys, hashlib
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
target = "861836f13e3d627dfa375bdb8389214e"
cands = [
    "reverseengineericanbarelyforward",
    "reverseengineericanbarelyforward\n",
    "drawrofylerabnacireenigneesrever",
    "academy",
    "gogo",
    "psociety",
    "unhashed",
    "unhashedkey",
    "theunhashedkey",
    "reverse",
]
b2 = bytes.fromhex("4a53475d414503545d025a0a5357450d05005d555410010e4155574b45504601")
cands.append(b2.decode("latin-1"))
cands.append(b2.hex())
for c in cands:
    h = hashlib.md5(c.encode("latin-1", "replace")).hexdigest()
    mark = " <== MATCH" if h == target else ""
    print("%-36r %s%s" % (c[:34], h, mark))
