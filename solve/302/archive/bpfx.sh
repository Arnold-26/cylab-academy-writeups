#!/bin/bash
# How does the runtime map account data regions? (determines the off-by-one behaviour)
cd /tmp
for ref in v1.8.11 v1.8.14; do
  curl -sL -o /tmp/bpfx_$ref.rs "https://raw.githubusercontent.com/solana-labs/solana/$ref/program-runtime/src/bpf_executor.rs"
  echo "=== $ref size $(stat -c%s /tmp/bpfx_$ref.rs)"
done
F=/tmp/bpfx_v1.8.11.rs
grep -n "MAX_PERMITTED_DATA_INCREASE\|MemoryRegion\|region" $F | head -50
echo "=== serialize_parameters_aligned"
grep -n "fn serialize_parameters" -A 60 $F | head -90
