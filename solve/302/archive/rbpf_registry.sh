#!/bin/bash
D=~/.cargo/registry/src/index.crates.io-1949cf8c6b5b557f/solana_rbpf-0.2.19
sed -n '110,200p' "$D/src/vm.rs"
echo "=== Default / register fns"
grep -n "impl Default for SyscallRegistry" -A 30 "$D/src/vm.rs"
grep -n "fn register_syscall" -A 20 "$D/src/vm.rs" | head -60
