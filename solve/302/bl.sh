#!/bin/bash
cd /tmp
B=https://raw.githubusercontent.com/solana-labs/solana/v1.8.11/programs/bpf_loader/src
for f in lib.rs serialization.rs syscalls.rs; do
  curl -sL -o /tmp/bl_$f "$B/$f"
  echo "=== $f $(stat -c%s /tmp/bl_$f)"
done
echo "##### regions in lib.rs"
grep -n "MemoryRegion\|vm_addr\|MAX_PERMITTED_DATA_INCREASE\|regions" /tmp/bl_lib.rs | head -40
echo "##### serialization.rs key parts"
grep -n "MAX_PERMITTED_DATA_INCREASE" -B3 -A12 /tmp/bl_serialization.rs | head -80
