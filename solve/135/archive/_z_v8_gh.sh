#!/bin/bash
mkdir -p /tmp/v8/src
cd /tmp/v8/src
curl -s "https://api.github.com/repos/ir0nstone/cybersec-notes/contents/binexp/browser-exploitation" -o ir0n.json
python3 -c "
import json
d=json.load(open('ir0n.json'))
for x in d: print(x['name'])
"
echo '--- try download raw ---'
for f in picoctf-2021-download-horsepower.md picoctf-2021-turboflan.md picoctf-2021-kit-engine.md; do
  curl -s -o "$f" "https://raw.githubusercontent.com/ir0nstone/cybersec-notes/master/binexp/browser-exploitation/$f"
  echo "$f: $(wc -c < $f)"
done
