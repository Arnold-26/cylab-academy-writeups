#!/bin/bash
cd /tmp
curl -sL -o /tmp/bl_deprecated.rs https://raw.githubusercontent.com/solana-labs/solana/v1.8.11/programs/bpf_loader/src/deprecated.rs
echo "size $(stat -c%s /tmp/bl_deprecated.rs)"
grep -n "fn finalize" -A 70 /tmp/bl_deprecated.rs | head -100
