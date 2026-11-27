import sys, re
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
img = "/tmp/t413full.img"
d = open(img, "rb").read()
needle = b"innocuous-file.txt"
offs = []
i = 0
while True:
    i = d.find(needle, i)
    if i < 0:
        break
    offs.append(i)
    i += 1
# les entrees de repertoire ext2/ext4 : inode(4) rec_len(2) name_len(1) file_type(1) name
print("=== noms complets apres innocuous-file.txt ===")
frags = []
for k, o in enumerate(offs):
    end = o + len(needle)
    # chercher le debut de l'entree suivante : on lit 4+2+1+1 puis le nom
    seg = d[end:end + 200]
    # la prochaine entree commence souvent par l'inode sur 4 octets ; on cherche une suite imprimable
    m = re.match(rb"[\x00-\xff]{0,8}?([ -~]{3,40})", seg)
    txt = re.sub(rb"[^\x20-\x7e]", b".", seg[:80]).decode("latin-1")
    print("#%-2d %s" % (k, txt))
