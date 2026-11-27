import sys, zipfile, re, pathlib
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
B = pathlib.Path(r"/tmp/cylab_eps")
z = zipfile.ZipFile(B / "385_Virtual-Machine-0.zip")
name = z.namelist()[0]
data = z.read(name).decode("utf-8", "replace")
print("taille:", len(data))
# noms de noeuds
names = re.findall(r'<node[^>]*name="([^"]+)"', data)
print("noeuds:", names[:20])
# ids de geometrie
geos = re.findall(r'<geometry[^>]*id="([^"]+)"', data)
print("geometries:", geos[:20])
# compter les segments/mesh
meshes = re.findall(r'<mesh>', data)
print("meshes:", len(meshes))
# chercher des nombres de dents dans les noms
for kw in ("gear", "tooth", "teeth", "Gear"):
    hits = [n for n in names if kw.lower() in n.lower()]
    if hits:
        print(kw, ":", hits[:10])
