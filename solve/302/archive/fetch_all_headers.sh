#!/bin/bash
set -u
REF=v1.10.0
DEST=./_z_302/c/inc
mkdir -p "$DEST/sol"
python3 - "$REF" "$DEST" <<'PY'
import json,sys,urllib.request,os
ref,dest=sys.argv[1],sys.argv[2]
url=f"https://api.github.com/repos/solana-labs/solana/contents/sdk/bpf/c/inc/sol?ref={ref}"
req=urllib.request.Request(url,headers={"User-Agent":"x"})
data=json.load(urllib.request.urlopen(req,timeout=40))
base=f"https://raw.githubusercontent.com/solana-labs/solana/{ref}/sdk/bpf/c/inc/sol/"
for e in data:
    if e["type"]!="file": continue
    name=e["name"]
    try:
        raw=urllib.request.urlopen(urllib.request.Request(base+name,headers={"User-Agent":"x"}),timeout=40).read()
        open(os.path.join(dest,"sol",name),"wb").write(raw)
        print("ok",name,len(raw))
    except Exception as ex:
        print("FAIL",name,ex)
PY
echo "=== present"
ls "$DEST/sol"
