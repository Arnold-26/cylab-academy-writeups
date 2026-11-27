#!/bin/bash
D=$(ls -d /root/.cargo/registry/src/*/solana_rbpf-0.2.19 2>/dev/null || ls -d ~/.cargo/registry/src/*/solana_rbpf-0.2.19)
echo "crate dir: $D"
grep -rn "pub struct SyscallRegistry\|pub struct Config" "$D/src" | head
echo "--- lib.rs exports"
grep -n "pub mod\|pub use" "$D/src/lib.rs" | head -30
