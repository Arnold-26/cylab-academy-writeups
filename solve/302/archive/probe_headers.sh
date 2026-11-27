#!/bin/bash
# Probe which ref/path hosts the Solana C SDK headers
set -u
BASE="https://raw.githubusercontent.com/solana-labs/solana"
for ref in v1.10.0 v1.13.0 v1.14.0 v1.16.0 master; do
  for path in sdk/sbf/c/inc/sol sdk/bpf/c/inc/sol; do
    code=$(curl -s -o /dev/null -w "%{http_code}" --max-time 20 "$BASE/$ref/$path/types.h")
    echo "$ref  $path/types.h -> $code"
  done
done
