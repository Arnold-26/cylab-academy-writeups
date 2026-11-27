import os, subprocess, sys, json

OUT = r"./_z_496_emls"
os.makedirs(OUT, exist_ok=True)

def run(name, data, show=True):
    p = os.path.join(OUT, name + ".eml")
    with open(p, "w", newline="", encoding="utf-8") as f:
        f.write(data)
    wp = "./_z_496_emls/" + name + ".eml"
    r = subprocess.run(["wsl", "-d", "kali-linux", "--", "bash", "-lc",
                        "node ./_z_496_parse.js " + wp + " 2>/dev/null"],
                       capture_output=True, text=True)
    if show:
        try:
            j = json.loads(r.stdout)
            print("==", name, "->", json.dumps({k: (v[:80] if isinstance(v, str) else v) for k, v in j.items()}))
        except Exception:
            print("==", name, "rc", r.returncode, "out:", r.stdout[:300], "err:", r.stderr[:300])
    return r.stdout

def batch(fn):
    fn()

if __name__ == '__main__':
    pass
