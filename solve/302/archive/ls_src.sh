#!/bin/bash
for p in program-runtime/src programs/bpf_loader/src; do
  echo "=== $p @v1.8.11"
  curl -s "https://api.github.com/repos/solana-labs/solana/contents/$p?ref=v1.8.11" | python3 -c "
import json,sys
try:
    d=json.load(sys.stdin)
    for e in d: print(' ', e['name'])
except Exception as ex: print('ERR',ex)
"
done
