#!/bin/bash
cd /tmp/v8/src
curl -s "https://api.github.com/repos/exd0tpy/CTF-browser-challenges/git/trees/main?recursive=1" -o exd.json
python3 - <<'PY'
import json
d=json.load(open('/tmp/v8/src/exd.json'))
for x in d.get('tree',[]):
    p=x['path']
    if 'urbo' in p or 'orse' in p or 'it' in p.lower():
        print(x['type'], x.get('size'), p)
PY
