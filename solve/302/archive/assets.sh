#!/bin/bash
echo "=== what did we download"
cat /tmp/spd.bin; echo
echo "=== release assets for v1.10.31"
curl -s "https://api.github.com/repos/solana-labs/solana/releases/tags/v1.10.31" | python3 -c "
import json,sys
d=json.load(sys.stdin)
print('name:', d.get('name'), 'tag:', d.get('tag_name'))
for a in d.get('assets',[]):
    print(f\"{a['name']:60s} {a['size']/1e6:8.1f} MB  {a['browser_download_url']}\")
" 2>&1 | head -30
